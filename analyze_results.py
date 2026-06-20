#!/usr/bin/env python3
"""
Analisis hasil simulasi gem5 untuk jurnal:
Implementasi dan Evaluasi Pipeline Processing untuk Meningkatkan Efisiensi Eksekusi Instruksi

Metrik yang diekstrak:
- Performance Metrics (Cycles, Instructions, CPI, IPC)
- Pipeline Hazards dan Stalls
- Cache Performance
- Branch Prediction Accuracy
- Speedup Calculation
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Tuple, Optional

class StatsParser:
    """Parser untuk file stats.txt dari gem5"""
    
    def __init__(self, stats_file: str):
        self.stats_file = stats_file
        self.stats_dict = {}
        self.parse()
    
    def parse(self):
        """Parse file stats.txt"""
        if not os.path.exists(self.stats_file):
            raise FileNotFoundError(f"File {self.stats_file} tidak ditemukan")
        
        with open(self.stats_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#') or line.startswith('-'):
                    continue
                
                # Parse format: metric_name value # description
                parts = line.split('#')
                if len(parts) >= 1:
                    metric_line = parts[0].strip()
                    
                    # Pisahkan metric name dan value
                    match = re.match(r'(\S+)\s+(.*?)$', metric_line)
                    if match:
                        metric_name = match.group(1)
                        value_str = match.group(2).strip()
                        
                        # Convert nilai ke appropriate type
                        try:
                            if '.' in value_str:
                                value = float(value_str)
                            else:
                                value = int(value_str)
                        except ValueError:
                            value = value_str
                        
                        self.stats_dict[metric_name] = value
    
    def get(self, metric: str, default=None):
        """Ambil nilai metrik"""
        return self.stats_dict.get(metric, default)
    
    def get_float(self, metric: str, default=0.0) -> float:
        """Ambil nilai sebagai float"""
        val = self.get(metric, default)
        try:
            return float(val)
        except (ValueError, TypeError):
            return default

class SimulationAnalyzer:
    """Menganalisis hasil simulasi untuk jurnal"""
    
    def __init__(self, timing_stats_dir: Optional[str] = None, minor_stats_dir: Optional[str] = None):
        self.timing_parser = None
        self.minor_parser = None
        self.results = {}
        
        if timing_stats_dir:
            stats_file = os.path.join(timing_stats_dir, "stats.txt")
            self.timing_parser = StatsParser(stats_file)
        
        if minor_stats_dir:
            stats_file = os.path.join(minor_stats_dir, "stats.txt")
            self.minor_parser = StatsParser(stats_file)
    
    def extract_metrics(self, parser: StatsParser, cpu_type: str) -> Dict:
        """Ekstrak metrik penting dari parser"""
        metrics = {}
        
        # Performance Metrics
        metrics['simInsts'] = parser.get('simInsts', 0)
        metrics['simOps'] = parser.get('simOps', 0)
        metrics['simTicks'] = parser.get('simTicks', 0)
        metrics['numCycles'] = parser.get_float('board.processor.cores.core.numCycles', 0)
        metrics['cpi'] = parser.get_float('board.processor.cores.core.cpi', 0)
        metrics['ipc'] = parser.get_float('board.processor.cores.core.ipc', 0)
        
        # Cache Metrics - L1 Data Cache
        metrics['l1d_hits'] = parser.get('board.cache_hierarchy.l1dcaches.demandHits::total', 0)
        metrics['l1d_misses'] = parser.get('board.cache_hierarchy.l1dcaches.demandMisses::total', 0)
        metrics['l1d_accesses'] = parser.get('board.cache_hierarchy.l1dcaches.demandAccesses::total', 0)
        metrics['l1d_miss_rate'] = parser.get_float('board.cache_hierarchy.l1dcaches.demandMissRate::total', 0)
        
        # Cache Metrics - L1 Instruction Cache
        metrics['l1i_hits'] = parser.get('board.cache_hierarchy.l1icaches.demandHits::total', 0)
        metrics['l1i_misses'] = parser.get('board.cache_hierarchy.l1icaches.demandMisses::total', 0)
        metrics['l1i_accesses'] = parser.get('board.cache_hierarchy.l1icaches.demandAccesses::total', 0)
        metrics['l1i_miss_rate'] = parser.get_float('board.cache_hierarchy.l1icaches.demandMissRate::total', 0)
        
        # Branch Prediction Metrics
        metrics['branch_lookups'] = parser.get('board.processor.cores.core.branchPred.lookups_0::total', 0)
        metrics['branch_squashes'] = parser.get('board.processor.cores.core.branchPred.squashes_0::total', 0)
        
        # Instruction Types
        metrics['int_alu'] = parser.get('board.processor.cores.core.issuedInstType_0::IntAlu', 0)
        metrics['int_mult_div'] = parser.get('board.processor.cores.core.issuedInstType_0::IntMult', 0) + \
                                  parser.get('board.processor.cores.core.issuedInstType_0::IntDiv', 0)
        metrics['mem_read'] = parser.get('board.processor.cores.core.issuedInstType_0::MemRead', 0)
        metrics['mem_write'] = parser.get('board.processor.cores.core.issuedInstType_0::MemWrite', 0)
        
        return metrics
    
    def analyze(self):
        """Lakukan analisis lengkap"""
        print("\n" + "="*70)
        print("ANALISIS HASIL SIMULASI PIPELINE")
        print("="*70)
        
        # Ekstrak metrik
        if self.timing_parser:
            print("\n[1] Menganalisis TIMING CPU (Non-Pipelined)...")
            self.results['timing'] = self.extract_metrics(self.timing_parser, 'TIMING')
        
        if self.minor_parser:
            print("[2] Menganalisis MINOR CPU (Pipelined)...")
            self.results['minor'] = self.extract_metrics(self.minor_parser, 'MINOR')
        
        print("[3] Menghitung komparasi dan metrik tambahan...")
        
        # Hitung Speedup jika ada kedua CPU
        if 'timing' in self.results and 'minor' in self.results:
            timing_cycles = self.results['timing']['numCycles']
            minor_cycles = self.results['minor']['numCycles']
            
            if timing_cycles > 0 and minor_cycles > 0:
                speedup = timing_cycles / minor_cycles
                self.results['speedup'] = speedup
                self.results['improvement'] = ((timing_cycles - minor_cycles) / timing_cycles) * 100
        
        print("✓ Analisis selesai!\n")
    
    def print_single_cpu_report(self, cpu_type: str):
        """Print laporan untuk satu CPU"""
        if cpu_type not in self.results:
            return
        
        metrics = self.results[cpu_type]
        cpu_name = "TIMING (Non-Pipelined)" if cpu_type == "timing" else "MINOR (Pipelined In-Order)"
        
        print(f"\n{'='*70}")
        print(f"LAPORAN SIMULASI: {cpu_name}")
        print(f"{'='*70}")
        
        # Performance Metrics
        print(f"\n📊 PERFORMANCE METRICS")
        print(f"{'-'*70}")
        print(f"  Total Instructions Executed    : {metrics['simInsts']:>15,} insts")
        print(f"  Total Operations              : {metrics['simOps']:>15,} ops")
        print(f"  Total CPU Cycles              : {metrics['numCycles']:>15,.0f} cycles")
        print(f"  Cycles Per Instruction (CPI)  : {metrics['cpi']:>15.4f} cycles/inst")
        print(f"  Instructions Per Cycle (IPC)  : {metrics['ipc']:>15.4f} inst/cycle")
        print(f"  Simulation Ticks              : {metrics['simTicks']:>15,} ticks")
        
        # Cache Performance
        print(f"\n💾 CACHE PERFORMANCE - L1 DATA CACHE")
        print(f"{'-'*70}")
        print(f"  Cache Hits                    : {metrics['l1d_hits']:>15,} accesses")
        print(f"  Cache Misses                  : {metrics['l1d_misses']:>15,} accesses")
        print(f"  Total Accesses                : {metrics['l1d_accesses']:>15,} accesses")
        print(f"  Miss Rate                     : {metrics['l1d_miss_rate']*100:>14.2f}%")
        hit_rate = 100.0 - (metrics['l1d_miss_rate']*100) if metrics['l1d_accesses'] > 0 else 0
        print(f"  Hit Rate                      : {hit_rate:>14.2f}%")
        
        # Branch Prediction
        print(f"\n🎯 BRANCH PREDICTION")
        print(f"{'-'*70}")
        print(f"  Branch Lookups                : {metrics['branch_lookups']:>15,} branches")
        print(f"  Branch Squashes (Mispred.)    : {metrics['branch_squashes']:>15,} branches")
        
        if metrics['branch_lookups'] > 0:
            branch_accuracy = ((metrics['branch_lookups'] - metrics['branch_squashes']) / 
                              metrics['branch_lookups']) * 100
            mispred_rate = (metrics['branch_squashes'] / metrics['branch_lookups']) * 100
            print(f"  Branch Accuracy               : {branch_accuracy:>14.2f}%")
            print(f"  Misprediction Rate            : {mispred_rate:>14.2f}%")
        
        # Instruction Distribution
        print(f"\n📈 INSTRUCTION DISTRIBUTION")
        print(f"{'-'*70}")
        total_issued = (metrics['int_alu'] + metrics['int_mult_div'] + 
                       metrics['mem_read'] + metrics['mem_write'])
        
        if total_issued > 0:
            print(f"  Integer ALU Operations        : {metrics['int_alu']:>15,} ({metrics['int_alu']/total_issued*100:.2f}%)")
            print(f"  Mult/Div Operations           : {metrics['int_mult_div']:>15,} ({metrics['int_mult_div']/total_issued*100:.2f}%)")
            print(f"  Memory Read Operations        : {metrics['mem_read']:>15,} ({metrics['mem_read']/total_issued*100:.2f}%)")
            print(f"  Memory Write Operations       : {metrics['mem_write']:>15,} ({metrics['mem_write']/total_issued*100:.2f}%)")
    
    def print_comparison_report(self):
        """Print laporan perbandingan TIMING vs MINOR"""
        if 'timing' not in self.results or 'minor' not in self.results:
            print("\n⚠️  Tidak dapat membuat perbandingan: data TIMING atau MINOR tidak lengkap")
            return
        
        timing = self.results['timing']
        minor = self.results['minor']
        
        print(f"\n{'='*70}")
        print(f"LAPORAN PERBANDINGAN: TIMING vs MINOR CPU")
        print(f"{'='*70}")
        
        # Tabel Perbandingan
        print(f"\n{'METRIK':<40} {'TIMING':>12} {'MINOR':>12} {'DIFF':>12}")
        print(f"{'-'*70}")
        
        # Cycles
        timing_cyc = timing['numCycles']
        minor_cyc = minor['numCycles']
        diff_cyc = timing_cyc - minor_cyc
        print(f"{'Total Cycles':<40} {timing_cyc:>12,.0f} {minor_cyc:>12,.0f} {diff_cyc:>12,.0f}")
        
        # Instructions
        timing_inst = timing['simInsts']
        minor_inst = minor['simInsts']
        print(f"{'Total Instructions':<40} {timing_inst:>12,} {minor_inst:>12,} {0:>12}")
        
        # CPI
        print(f"{'CPI (Cycles/Instruction)':<40} {timing['cpi']:>12.4f} {minor['cpi']:>12.4f} {timing['cpi']-minor['cpi']:>12.4f}")
        
        # IPC
        print(f"{'IPC (Instructions/Cycle)':<40} {timing['ipc']:>12.4f} {minor['ipc']:>12.4f} {minor['ipc']-timing['ipc']:>12.4f}")
        
        # Cache Miss Rates
        print(f"{'L1D Cache Miss Rate (%)':<40} {timing['l1d_miss_rate']*100:>11.2f}% {minor['l1d_miss_rate']*100:>11.2f}%")
        
        # Branch Prediction
        if timing['branch_lookups'] > 0:
            timing_bp_acc = (timing['branch_lookups'] - timing['branch_squashes']) / timing['branch_lookups'] * 100
        else:
            timing_bp_acc = 0
        
        if minor['branch_lookups'] > 0:
            minor_bp_acc = (minor['branch_lookups'] - minor['branch_squashes']) / minor['branch_lookups'] * 100
        else:
            minor_bp_acc = 0
        
        print(f"{'Branch Prediction Accuracy (%)':<40} {timing_bp_acc:>11.2f}% {minor_bp_acc:>11.2f}%")
        
        # Speedup Analysis
        print(f"\n{'='*70}")
        print(f"ANALISIS SPEEDUP DAN EFISIENSI")
        print(f"{'-'*70}")
        
        if 'speedup' in self.results:
            speedup = self.results['speedup']
            improvement = self.results['improvement']
            
            print(f"\n  Speedup (TIMING cycles / MINOR cycles): {speedup:.4f}x")
            print(f"  Performance Improvement: {improvement:.2f}%")
            print(f"  Cycle Reduction: {abs(diff_cyc):,} cycles")
            
            # Analisis Hazard Impact
            print(f"\n  🔴 ANALISIS DAMPAK HAZARD & STALL:")
            print(f"  {'-'*66}")
            
            # Estimasi hazard cycles (asumsi: perbedaan cycles sebanding dengan stalls)
            hazard_cycles = diff_cyc
            if minor['simInsts'] > 0:
                avg_hazard_per_inst = hazard_cycles / minor['simInsts']
                print(f"    Estimated Hazard-related Stalls: {hazard_cycles:,.0f} cycles")
                print(f"    Average Stall per Instruction: {avg_hazard_per_inst:.4f} cycles")
                
                # Estimasi hazard percentage
                if timing_cyc > 0:
                    hazard_percentage = (hazard_cycles / timing_cyc) * 100
                    print(f"    Hazard Impact on Performance: {hazard_percentage:.2f}%")
        
        # Cache Analysis
        print(f"\n  💾 CACHE PERFORMANCE IMPACT:")
        print(f"  {'-'*66}")
        timing_hit_rate = 100 - (timing['l1d_miss_rate']*100)
        minor_hit_rate = 100 - (minor['l1d_miss_rate']*100)
        print(f"    TIMING L1D Hit Rate: {timing_hit_rate:.2f}%")
        print(f"    MINOR L1D Hit Rate: {minor_hit_rate:.2f}%")
        
        # Branch Prediction Impact
        print(f"\n  🎯 BRANCH PREDICTION IMPACT:")
        print(f"  {'-'*66}")
        print(f"    TIMING BP Accuracy: {timing_bp_acc:.2f}%")
        print(f"    MINOR BP Accuracy: {minor_bp_acc:.2f}%")
        
        if timing['branch_lookups'] > 0:
            timing_squash_rate = (timing['branch_squashes'] / timing['branch_lookups']) * 100
            print(f"    TIMING Squash Rate: {timing_squash_rate:.2f}%")
        
        if minor['branch_lookups'] > 0:
            minor_squash_rate = (minor['branch_squashes'] / minor['branch_lookups']) * 100
            print(f"    MINOR Squash Rate: {minor_squash_rate:.2f}%")
    
    def generate_json_report(self, output_file: str = "simulation_results.json"):
        """Generate laporan dalam format JSON untuk publikasi"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'benchmark': 'hazard_test',
            'isa': 'RISC-V',
            'timing_results': self.results.get('timing', {}),
            'minor_results': self.results.get('minor', {}),
            'comparison': {
                'speedup': self.results.get('speedup', None),
                'improvement_percentage': self.results.get('improvement', None)
            }
        }
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n✓ JSON Report disimpan: {output_file}")
        return output_file
    
    def print_full_report(self):
        """Print laporan lengkap"""
        if self.timing_parser:
            self.print_single_cpu_report('timing')
        
        if self.minor_parser:
            self.print_single_cpu_report('minor')
        
        if self.timing_parser and self.minor_parser:
            self.print_comparison_report()
        
        print(f"\n{'='*70}\n")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Analisis hasil simulasi gem5 untuk jurnal",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Contoh penggunaan:
  python3 analyze_results.py --all              # Analisis kedua CPU dan generate report
  python3 analyze_results.py --timing           # Analisis TIMING CPU saja
  python3 analyze_results.py --minor            # Analisis MINOR CPU saja
  python3 analyze_results.py --json             # Generate JSON report
        """
    )
    
    parser.add_argument('--timing', action='store_true', help='Analisis TIMING CPU')
    parser.add_argument('--minor', action='store_true', help='Analisis MINOR CPU')
    parser.add_argument('--all', action='store_true', help='Analisis kedua CPU')
    parser.add_argument('--json', action='store_true', help='Generate JSON report')
    parser.add_argument('--timing-dir', default='m5out_TIMING', help='Direktori hasil TIMING')
    parser.add_argument('--minor-dir', default='m5out_MINOR', help='Direktori hasil MINOR')
    
    args = parser.parse_args()
    
    # Default: analisis yang ada
    if not any([args.timing, args.minor, args.all]):
        args.all = True
    
    # Tentukan direktori yang akan dianalisis
    timing_dir = args.timing_dir if (args.timing or args.all) else None
    minor_dir = args.minor_dir if (args.minor or args.all) else None
    
    # Create analyzer
    analyzer = SimulationAnalyzer(timing_dir, minor_dir)
    analyzer.analyze()
    analyzer.print_full_report()
    
    # Generate JSON jika diminta
    if args.json or args.all:
        analyzer.generate_json_report()

if __name__ == "__main__":
    main()
