import argparse
from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.private_l1_cache_hierarchy import PrivateL1CacheHierarchy
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.processors.cpu_types import CPUTypes
from gem5.isas import ISA
from gem5.resources.resource import BinaryResource
from gem5.simulate.simulator import Simulator

# 1. Setup Argparse agar kita bisa memilih tipe CPU lewat terminal
parser = argparse.ArgumentParser(description="Simulasi Pipeline, Hazard, dan Stall")
parser.add_argument("--cpu", type=str, choices=["timing", "minor"], default="timing", 
                    help="Pilih tipe CPU: timing (Non-Pipeline) atau minor (Pipelined)")
args = parser.parse_args()

# 2. Tentukan Tipe CPU (Ini inti dari jurnalmu!)
# TIMING = Prosesor sederhana yang mengeksekusi instruksi satu per satu (Non-Pipelined)
# MINOR = Prosesor dengan in-order pipeline (Akan terjadi Stall jika ada Hazard)
if args.cpu == "timing":
    cpu_tipe = CPUTypes.TIMING
elif args.cpu == "minor":
    cpu_tipe = CPUTypes.MINOR

# 3. Rakit Komponen Hardware
# Gunakan ISA RISC-V sesuai dengan target build gem5 kita
processor = SimpleProcessor(cpu_type=cpu_tipe, num_cores=1, isa=ISA.RISCV)
memory = SingleChannelDDR3_1600(size="512MB")
cache_hierarchy = PrivateL1CacheHierarchy(l1d_size="16kB", l1i_size="16kB")

board = SimpleBoard(
    clk_freq="1GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy
)

# 4. Masukkan Program Pemicu Hazard (Workload)
# Pastikan nama file sesuai dengan file hasil kompilasi program C kamu
binary = BinaryResource(local_path="./hazard_test")
board.set_se_binary_workload(binary)

# 5. Jalankan Simulator
print(f"\n==================================================")
print(f"Mulai Simulasi gem5 dengan CPU: {args.cpu.upper()}")
print(f"==================================================\n")

simulator = Simulator(board=board)
simulator.run()

print(f"\n==================================================")
print(f"Simulasi Selesai!")
print(f"==================================================\n")