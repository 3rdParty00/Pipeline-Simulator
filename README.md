# Pipeline-Simulator

A gem5-based CPU pipeline simulator designed to demonstrate and analyze pipeline hazards, stalls, and their effects on instruction execution in both non-pipelined and pipelined processors using RISC-V ISA.

## 🎯 Overview

This project simulates CPU pipeline behavior using gem5, focusing on:
- **Data Hazards** (Read After Write - RAW dependencies)
- **Control Hazards** (Branch prediction and misprediction)
- **Pipeline Stalls** and their performance impact

The simulator allows comparison between two CPU models:
- **TIMING**: Non-pipelined processor (sequential execution)
- **MINOR**: Pipelined processor with in-order execution (exhibits stalls on hazards)

## 📋 Project Structure

```
Pipeline-Simulator/
├── README.md                 # Project documentation
├── simulasi_jurnal.py        # Main simulator script using gem5
├── benchmark_jurnal.c        # Custom microbenchmark for testing hazards
├── hazard_test              # Compiled binary (RISC-V executable)
└── .git/                    # Version control
```

## 🔧 Dependencies

- **gem5**: CPU simulator and system simulator
- **Python 3.x**: For running the simulator script
- **RISC-V Toolchain**: For compiling the benchmark (riscv64-unknown-elf-gcc)
- **GCC**: For compilation

### Installation

1. Build gem5 with RISC-V ISA support:
```bash
cd gem5
scons build/RISCV/gem5.opt -j4
```

2. Ensure the RISC-V toolchain is installed:
```bash
# Ubuntu/Debian
sudo apt-get install gcc-riscv64-unknown-elf

# macOS
brew install riscv-tools
```

## 📝 File Descriptions

### `simulasi_jurnal.py`
Main simulator script that:
- Sets up gem5 simulation environment
- Configures CPU type (TIMING or MINOR) via command-line arguments
- Creates hardware components:
  - Single-core processor with RISC-V ISA
  - 512 MB DDR3-1600 memory
  - Private 16KB L1 instruction and data caches
- Loads and executes the compiled benchmark binary
- Measures performance metrics

### `benchmark_jurnal.c`
Custom microbenchmark that triggers:

**Data Hazards** (RAW dependencies):
```c
x = a + b;  // Write to x
y = x * c;  // Read x - Hazard!
z = y - d;  // Read y - Hazard!
```

**Control Hazards** (Branch prediction):
- 500-iteration loop with alternating branch pattern
- Tests branch predictor accuracy
- Demonstrates pipeline flushes on misprediction

## 🚀 Usage

### Step 1: Compile the Benchmark
```bash
riscv64-unknown-elf-gcc -o hazard_test benchmark_jurnal.c
```

### Step 2: Run the Simulator

**With Non-Pipelined CPU (TIMING):**
```bash
python3 simulasi_jurnal.py --cpu timing
```

**With Pipelined CPU (MINOR):**
```bash
python3 simulasi_jurnal.py --cpu minor
```

**Default (uses MINOR):**
```bash
python3 simulasi_jurnal.py
```

## 📊 Expected Output

The simulator will:
1. Display simulation start message with CPU type
2. Execute the benchmark program
3. Show simulation statistics including:
   - Number of cycles executed
   - Number of instructions committed
   - CPI (Cycles Per Instruction)
   - Cache statistics (hits/misses)
   - Pipeline stalls (for MINOR CPU)
   - Branch prediction statistics

## 🔍 Key Findings

- **TIMING CPU**: Executes instructions sequentially, no stalls (baseline performance)
- **MINOR CPU**: Exhibits stalls when data hazards and control hazards occur
- The difference in cycle counts demonstrates the impact of pipeline hazards
- Branch prediction accuracy affects overall performance

## 📚 Concepts Demonstrated

| Concept | Explanation | Test Case |
|---------|-------------|-----------|
| **Data Hazard (RAW)** | Instruction depends on result of previous instruction | `y = x * c` depends on `x = a + b` |
| **Control Hazard** | Branch prediction affects instruction fetch | 500-iteration conditional loop |
| **Pipeline Stall** | Pipeline pauses due to hazard dependencies | Observable in MINOR CPU simulation |
| **ILP** | Instruction-Level Parallelism reduced by hazards | Comparing TIMING vs MINOR cycle counts |

## 📖 References

- [gem5 Documentation](http://www.gem5.org/)
- [RISC-V ISA Specification](https://riscv.org/)
- Computer Architecture: Pipeline concepts and hazard handling

## ✏️ Notes

- Output statistics are logged by gem5 in `m5out/` directory
- Simulation results vary based on gem5 version and build configuration
- For detailed statistics, examine m5out/stats.txt after simulation

## 📄 License

Project-specific license information here (if applicable)

---

**Author**: Your Name  
**Last Updated**: 2026-06-19
