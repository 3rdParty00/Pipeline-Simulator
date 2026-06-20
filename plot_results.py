#!/usr/bin/env python3
"""
Visualisasi hasil simulasi untuk publikasi jurnal
Menghasilkan figures berkualitas publication-ready

Requirements:
  pip install matplotlib pandas numpy
"""

import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
import sys

class SimulationVisualizer:
    """Generate publication-quality figures from simulation results"""
    
    def __init__(self, json_file: str = "simulation_results.json"):
        self.json_file = json_file
        self.data = None
        self.load_data()
        
        # Publication style settings
        plt.style.use('seaborn-v0_8-darkgrid')
        self.colors = {
            'timing': '#1f77b4',  # Blue
            'minor': '#ff7f0e',   # Orange
            'good': '#2ca02c',    # Green
            'bad': '#d62728'      # Red
        }
    
    def load_data(self):
        """Load JSON results"""
        if not Path(self.json_file).exists():
            print(f"❌ File {self.json_file} tidak ditemukan!")
            print("Jalankan: python3 analyze_results.py --all --json")
            sys.exit(1)
        
        with open(self.json_file, 'r') as f:
            self.data = json.load(f)
    
    def plot_cpi_comparison(self):
        """Figure 1: CPI Comparison"""
        timing_cpi = self.data['timing_results']['cpi']
        minor_cpi = self.data['minor_results']['cpi']
        
        fig, ax = plt.subplots(figsize=(8, 6))
        
        cpus = ['TIMING\n(Non-Pipelined)', 'MINOR\n(Pipelined In-Order)']
        cpis = [timing_cpi, minor_cpi]
        colors_list = [self.colors['timing'], self.colors['minor']]
        
        bars = ax.bar(cpus, cpis, color=colors_list, edgecolor='black', linewidth=1.5)
        
        # Add value labels on bars
        for bar, cpi in zip(bars, cpis):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{cpi:.4f}',
                   ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        ax.set_ylabel('Cycles Per Instruction (CPI)', fontsize=12, fontweight='bold')
        ax.set_title('CPI Comparison: TIMING vs MINOR CPU', fontsize=14, fontweight='bold')
        ax.set_ylim(0, max(cpis) * 1.2)
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        return fig, 'figure_01_cpi_comparison.png'
    
    def plot_ipc_comparison(self):
        """Figure 2: IPC Comparison"""
        timing_ipc = self.data['timing_results']['ipc']
        minor_ipc = self.data['minor_results']['ipc']
        
        fig, ax = plt.subplots(figsize=(8, 6))
        
        cpus = ['TIMING\n(Non-Pipelined)', 'MINOR\n(Pipelined In-Order)']
        ipcs = [timing_ipc, minor_ipc]
        colors_list = [self.colors['timing'], self.colors['minor']]
        
        bars = ax.bar(cpus, ipcs, color=colors_list, edgecolor='black', linewidth=1.5)
        
        # Add value labels on bars
        for bar, ipc in zip(bars, ipcs):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{ipc:.4f}',
                   ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        ax.set_ylabel('Instructions Per Cycle (IPC)', fontsize=12, fontweight='bold')
        ax.set_title('IPC Comparison: TIMING vs MINOR CPU', fontsize=14, fontweight='bold')
        ax.set_ylim(0, max(ipcs) * 1.2)
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        return fig, 'figure_02_ipc_comparison.png'
    
    def plot_cycle_comparison(self):
        """Figure 3: Total Cycles Comparison"""
        timing_cycles = self.data['timing_results']['numCycles']
        minor_cycles = self.data['minor_results']['numCycles']
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        cpus = ['TIMING\n(Non-Pipelined)', 'MINOR\n(Pipelined In-Order)']
        cycles = [timing_cycles, minor_cycles]
        colors_list = [self.colors['timing'], self.colors['minor']]
        
        bars = ax.bar(cpus, cycles, color=colors_list, edgecolor='black', linewidth=1.5)
        
        # Add value labels on bars
        for bar, cyc in zip(bars, cycles):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(cyc):,}',
                   ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        # Add difference annotation
        diff = timing_cycles - minor_cycles
        improvement = (diff / timing_cycles) * 100
        ax.text(0.5, max(cycles) * 0.5, 
               f'Reduction: {int(diff):,} cycles\n({improvement:.1f}%)',
               ha='center', fontsize=11, 
               bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
        
        ax.set_ylabel('Total CPU Cycles', fontsize=12, fontweight='bold')
        ax.set_title('Total Cycles Comparison: TIMING vs MINOR CPU', fontsize=14, fontweight='bold')
        ax.set_ylim(0, max(cycles) * 1.3)
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        return fig, 'figure_03_cycle_comparison.png'
    
    def plot_speedup(self):
        """Figure 4: Speedup and Performance Improvement"""
        speedup = self.data['comparison']['speedup']
        improvement = self.data['comparison']['improvement_percentage']
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
        
        # Speedup gauge
        ax1.barh(['Speedup'], [speedup], color=self.colors['good'], 
                edgecolor='black', linewidth=2, height=0.3)
        ax1.text(speedup/2, 0, f'{speedup:.3f}x', 
                ha='center', va='center', fontsize=14, fontweight='bold', color='white')
        ax1.set_xlim(0, max(2, speedup*1.3))
        ax1.set_xlabel('Speedup Factor', fontsize=12, fontweight='bold')
        ax1.set_title('Pipeline Speedup (MINOR/TIMING)', fontsize=13, fontweight='bold')
        ax1.grid(axis='x', alpha=0.3)
        
        # Performance improvement
        ax2.barh(['Improvement'], [improvement], color=self.colors['good'],
                edgecolor='black', linewidth=2, height=0.3)
        ax2.text(improvement/2, 0, f'{improvement:.1f}%', 
                ha='center', va='center', fontsize=14, fontweight='bold', color='white')
        ax2.set_xlim(0, 100)
        ax2.set_xlabel('Performance Improvement (%)', fontsize=12, fontweight='bold')
        ax2.set_title('Cycle Count Reduction', fontsize=13, fontweight='bold')
        ax2.grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        return fig, 'figure_04_speedup.png'
    
    def plot_cache_performance(self):
        """Figure 5: Cache Performance Comparison"""
        timing_miss_rate = self.data['timing_results']['l1d_miss_rate'] * 100
        minor_miss_rate = self.data['minor_results']['l1d_miss_rate'] * 100
        
        timing_hit_rate = 100 - timing_miss_rate
        minor_hit_rate = 100 - minor_miss_rate
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        x = range(2)
        width = 0.35
        
        hits = [timing_hit_rate, minor_hit_rate]
        misses = [timing_miss_rate, minor_miss_rate]
        
        bars1 = ax.bar([i - width/2 for i in x], hits, width, 
                       label='Hit Rate', color=self.colors['good'], 
                       edgecolor='black', linewidth=1.5)
        bars2 = ax.bar([i + width/2 for i in x], misses, width,
                       label='Miss Rate', color=self.colors['bad'],
                       edgecolor='black', linewidth=1.5)
        
        # Add value labels
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.2f}%',
                       ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        ax.set_ylabel('Percentage (%)', fontsize=12, fontweight='bold')
        ax.set_title('L1D Cache Performance: Hit vs Miss Rate', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(['TIMING', 'MINOR'])
        ax.set_ylim(0, 105)
        ax.legend(fontsize=11, loc='lower right')
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        return fig, 'figure_05_cache_performance.png'
    
    def plot_branch_prediction(self):
        """Figure 6: Branch Prediction Accuracy"""
        timing_lookups = self.data['timing_results']['branch_lookups']
        timing_squashes = self.data['timing_results']['branch_squashes']
        minor_lookups = self.data['minor_results']['branch_lookups']
        minor_squashes = self.data['minor_results']['branch_squashes']
        
        timing_accuracy = ((timing_lookups - timing_squashes) / timing_lookups * 100) if timing_lookups > 0 else 0
        minor_accuracy = ((minor_lookups - minor_squashes) / minor_lookups * 100) if minor_lookups > 0 else 0
        
        timing_mispred = 100 - timing_accuracy
        minor_mispred = 100 - minor_accuracy
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        x = range(2)
        width = 0.35
        
        accurate = [timing_accuracy, minor_accuracy]
        mispredicted = [timing_mispred, minor_mispred]
        
        bars1 = ax.bar([i - width/2 for i in x], accurate, width,
                       label='Correct Predictions', color=self.colors['good'],
                       edgecolor='black', linewidth=1.5)
        bars2 = ax.bar([i + width/2 for i in x], mispredicted, width,
                       label='Mispredictions', color=self.colors['bad'],
                       edgecolor='black', linewidth=1.5)
        
        # Add value labels
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                           f'{height:.2f}%',
                           ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        ax.set_ylabel('Percentage (%)', fontsize=12, fontweight='bold')
        ax.set_title('Branch Prediction Accuracy', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(['TIMING', 'MINOR'])
        ax.set_ylim(0, 105)
        ax.legend(fontsize=11, loc='lower right')
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        return fig, 'figure_06_branch_prediction.png'
    
    def plot_instruction_distribution(self):
        """Figure 7: Instruction Type Distribution"""
        int_alu = self.data['minor_results']['int_alu']
        mem_read = self.data['minor_results']['mem_read']
        mem_write = self.data['minor_results']['mem_write']
        mult_div = self.data['minor_results']['int_mult_div']
        
        total = int_alu + mem_read + mem_write + mult_div
        
        sizes = [int_alu, mem_read, mem_write, mult_div]
        labels = ['Integer ALU\n({:.1f}%)'.format(int_alu/total*100),
                 'Memory Read\n({:.1f}%)'.format(mem_read/total*100),
                 'Memory Write\n({:.1f}%)'.format(mem_write/total*100),
                 'Mult/Div\n({:.1f}%)'.format(mult_div/total*100)]
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors,
                                           autopct='%1.1f%%', startangle=90,
                                           textprops={'fontsize': 11, 'fontweight': 'bold'},
                                           wedgeprops=dict(edgecolor='black', linewidth=1.5))
        
        ax.set_title('Instruction Distribution (MINOR CPU)', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        return fig, 'figure_07_instruction_distribution.png'
    
    def generate_all(self):
        """Generate all figures"""
        print("\n" + "="*70)
        print("MENGHASILKAN VISUALISASI UNTUK PUBLIKASI")
        print("="*70 + "\n")
        
        figures = [
            ('CPI Comparison', self.plot_cpi_comparison),
            ('IPC Comparison', self.plot_ipc_comparison),
            ('Cycle Comparison', self.plot_cycle_comparison),
            ('Speedup Analysis', self.plot_speedup),
            ('Cache Performance', self.plot_cache_performance),
            ('Branch Prediction', self.plot_branch_prediction),
            ('Instruction Distribution', self.plot_instruction_distribution),
        ]
        
        for title, func in figures:
            try:
                print(f"Generating: {title}...", end=' ')
                fig, filename = func()
                plt.savefig(filename, dpi=300, bbox_inches='tight')
                print(f"✓ Saved as {filename}")
                plt.close(fig)
            except Exception as e:
                print(f"❌ Error: {str(e)}")
        
        print("\n" + "="*70)
        print("✓ Semua visualisasi berhasil dihasilkan!")
        print("="*70)
        print("\nFile-file yang dihasilkan:")
        print("  figure_01_cpi_comparison.png")
        print("  figure_02_ipc_comparison.png")
        print("  figure_03_cycle_comparison.png")
        print("  figure_04_speedup.png")
        print("  figure_05_cache_performance.png")
        print("  figure_06_branch_prediction.png")
        print("  figure_07_instruction_distribution.png")
        print("\nGunakan file-file ini dalam dokumen jurnal Anda.")
        print("="*70 + "\n")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate publication-quality figures from simulation results",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Contoh penggunaan:
  python3 plot_results.py --all              # Generate semua figures
  python3 plot_results.py --cpi              # Generate CPI figure only
  python3 plot_results.py --json results.json # Gunakan JSON file lain
        """
    )
    
    parser.add_argument('--all', action='store_true', help='Generate semua figures')
    parser.add_argument('--cpi', action='store_true', help='Generate CPI comparison')
    parser.add_argument('--ipc', action='store_true', help='Generate IPC comparison')
    parser.add_argument('--cycles', action='store_true', help='Generate cycle comparison')
    parser.add_argument('--speedup', action='store_true', help='Generate speedup analysis')
    parser.add_argument('--cache', action='store_true', help='Generate cache performance')
    parser.add_argument('--branch', action='store_true', help='Generate branch prediction')
    parser.add_argument('--instructions', action='store_true', help='Generate instruction distribution')
    parser.add_argument('--json', default='simulation_results.json', help='JSON results file')
    
    args = parser.parse_args()
    
    visualizer = SimulationVisualizer(args.json)
    
    if args.all or not any([args.cpi, args.ipc, args.cycles, args.speedup, args.cache, args.branch, args.instructions]):
        visualizer.generate_all()
    else:
        if args.cpi:
            fig, name = visualizer.plot_cpi_comparison()
            plt.savefig(name, dpi=300, bbox_inches='tight')
            print(f"✓ Saved: {name}")
        if args.ipc:
            fig, name = visualizer.plot_ipc_comparison()
            plt.savefig(name, dpi=300, bbox_inches='tight')
            print(f"✓ Saved: {name}")
        if args.cycles:
            fig, name = visualizer.plot_cycle_comparison()
            plt.savefig(name, dpi=300, bbox_inches='tight')
            print(f"✓ Saved: {name}")
        if args.speedup:
            fig, name = visualizer.plot_speedup()
            plt.savefig(name, dpi=300, bbox_inches='tight')
            print(f"✓ Saved: {name}")
        if args.cache:
            fig, name = visualizer.plot_cache_performance()
            plt.savefig(name, dpi=300, bbox_inches='tight')
            print(f"✓ Saved: {name}")
        if args.branch:
            fig, name = visualizer.plot_branch_prediction()
            plt.savefig(name, dpi=300, bbox_inches='tight')
            print(f"✓ Saved: {name}")
        if args.instructions:
            fig, name = visualizer.plot_instruction_distribution()
            plt.savefig(name, dpi=300, bbox_inches='tight')
            print(f"✓ Saved: {name}")

if __name__ == "__main__":
    main()
