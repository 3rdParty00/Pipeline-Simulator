import argparse
import os
import shutil
import json
from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.private_l1_cache_hierarchy import PrivateL1CacheHierarchy
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.processors.cpu_types import CPUTypes
from gem5.isas import ISA
from gem5.resources.resource import BinaryResource
from gem5.simulate.simulator import Simulator

def run_simulation(cpu_type, cpu_name, output_dir):
    """
    Menjalankan simulasi gem5 dengan tipe CPU tertentu.
    
    Args:
        cpu_type: CPUTypes.TIMING atau CPUTypes.MINOR
        cpu_name: String nama CPU untuk output ('TIMING' atau 'MINOR')
        output_dir: Direktori untuk menyimpan hasil simulasi
    
    Returns:
        Path ke stats.txt dari simulasi
    """
    print(f"\n{'='*60}")
    print(f"Mulai Simulasi gem5 dengan CPU: {cpu_name}")
    print(f"Tipe CPU: {'Non-Pipelined (Sequential)' if cpu_name == 'TIMING' else 'Pipelined (In-Order)'}")
    print(f"Output Directory: {output_dir}")
    print(f"{'='*60}\n")
    
    # Setup Komponen Hardware
    processor = SimpleProcessor(cpu_type=cpu_type, num_cores=1, isa=ISA.RISCV)
    memory = SingleChannelDDR3_1600(size="512MB")
    cache_hierarchy = PrivateL1CacheHierarchy(l1d_size="16kB", l1i_size="16kB")
    
    board = SimpleBoard(
        clk_freq="1GHz",
        processor=processor,
        memory=memory,
        cache_hierarchy=cache_hierarchy
    )
    
    # Load Program Benchmark
    binary = BinaryResource(local_path="./hazard_test")
    board.set_se_binary_workload(binary)
    
    # Jalankan Simulasi
    simulator = Simulator(board=board, output_dir=output_dir)
    simulator.run()
    
    print(f"\n{'='*60}")
    print(f"Simulasi {cpu_name} Selesai!")
    print(f"{'='*60}\n")
    
    return os.path.join(output_dir, "stats.txt")

def main():
    parser = argparse.ArgumentParser(
        description="Simulasi Pipeline Prosesor RISC-V: Hazard, Stall, dan Speedup Analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Contoh penggunaan:
  python3 simulasi_jurnal.py --cpu timing      # Simulasi TIMING CPU saja
  python3 simulasi_jurnal.py --cpu minor       # Simulasi MINOR CPU saja
  python3 simulasi_jurnal.py --compare         # Jalankan keduanya dan bandingkan
  python3 simulasi_jurnal.py --all             # Analisis lengkap dengan report
        """
    )
    
    parser.add_argument(
        "--cpu", 
        type=str, 
        choices=["timing", "minor"],
        help="Pilih tipe CPU: timing (Non-Pipeline) atau minor (Pipelined)"
    )
    parser.add_argument(
        "--compare",
        action="store_true",
        help="Jalankan kedua tipe CPU dan bandingkan hasilnya"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Jalankan simulasi lengkap dengan analisis dan report untuk jurnal"
    )
    
    args = parser.parse_args()
    
    # Jika tidak ada argument, jalankan mode default (MINOR)
    if not args.cpu and not args.compare and not args.all:
        args.cpu = "minor"
    
    # Mode 1: Jalankan CPU tertentu
    if args.cpu:
        cpu_type = CPUTypes.TIMING if args.cpu == "timing" else CPUTypes.MINOR
        cpu_name = args.cpu.upper()
        output_dir = f"m5out_{cpu_name}"
        
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.makedirs(output_dir, exist_ok=True)
        
        stats_file = run_simulation(cpu_type, cpu_name, output_dir)
        print(f"\n✓ Hasil simulasi tersimpan di: {output_dir}/")
    
    # Mode 2: Compare TIMING vs MINOR
    elif args.compare:
        print("\n" + "="*60)
        print("MODE: PERBANDINGAN TIMING vs MINOR CPU")
        print("="*60)
        
        timing_dir = "m5out_TIMING"
        minor_dir = "m5out_MINOR"
        
        # Bersihkan direktori lama
        for d in [timing_dir, minor_dir]:
            if os.path.exists(d):
                shutil.rmtree(d)
            os.makedirs(d, exist_ok=True)
        
        # Jalankan kedua simulasi
        timing_stats = run_simulation(CPUTypes.TIMING, "TIMING", timing_dir)
        minor_stats = run_simulation(CPUTypes.MINOR, "MINOR", minor_dir)
        
        print(f"\n✓ Kedua simulasi selesai!")
        print(f"  TIMING: {timing_dir}/")
        print(f"  MINOR:  {minor_dir}/")
    
    # Mode 3: Analisis lengkap untuk jurnal
    elif args.all:
        print("\n" + "="*60)
        print("MODE: ANALISIS LENGKAP UNTUK JURNAL")
        print("="*60)
        
        timing_dir = "m5out_TIMING"
        minor_dir = "m5out_MINOR"
        
        # Bersihkan direktori lama
        for d in [timing_dir, minor_dir]:
            if os.path.exists(d):
                shutil.rmtree(d)
            os.makedirs(d, exist_ok=True)
        
        # Jalankan kedua simulasi
        timing_stats = run_simulation(CPUTypes.TIMING, "TIMING", timing_dir)
        minor_stats = run_simulation(CPUTypes.MINOR, "MINOR", minor_dir)
        
        print(f"\n✓ Simulasi selesai! Melakukan analisis...\n")

if __name__ == "__main__":
    main()