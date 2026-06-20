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
├── README.md                 # Project documentation (this file)
├── JOURNAL_GUIDE.md         # Complete guide for journal publication
├── simulasi_jurnal.py        # Enhanced simulator script with multiple modes
├── analyze_results.py        # Analyzer for extracting metrics and generating reports
├── plot_results.py           # Visualization script for publication-quality figures
├── run_full_analysis.sh      # Interactive bash script for full pipeline
├── benchmark_jurnal.c        # Custom microbenchmark for testing hazards
├── hazard_test              # Compiled binary (RISC-V executable)
├── m5out_TIMING/            # Results directory for TIMING CPU (generated)
├── m5out_MINOR/             # Results directory for MINOR CPU (generated)
├── simulation_results.json   # JSON report (generated)
├── figure_*.png             # Generated figures for publication (generated)
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

### `simulasi_jurnal.py` (Enhanced)
Enhanced simulator script with multiple modes:
- **--cpu timing/minor**: Run specific CPU type
- **--compare**: Run both CPUs and prepare for comparison
- **--all**: Full analysis mode
- Features:
  - Automatic output directory management
  - Better logging and progress indicators
  - Sets up for metrics extraction

### `analyze_results.py` (New!)
Advanced results analyzer that:
- Parses gem5 stats.txt files
- Extracts performance metrics (CPI, IPC, speedup)
- Analyzes pipeline hazards and stalls
- Generates branch prediction statistics
- Calculates cache performance
- Creates comparison reports
- Exports JSON for further processing

**Usage:**
```bash
python3 analyze_results.py --all --json
```

**Output:**
- Console report with formatted tables
- JSON file for data processing
- Hazard impact estimation
- Speedup and efficiency metrics

### `plot_results.py` (New!)
Publication-quality visualization script that generates:
- **Figure 1**: CPI Comparison (TIMING vs MINOR)
- **Figure 2**: IPC Comparison
- **Figure 3**: Total Cycles Comparison with reduction percentage
- **Figure 4**: Speedup gauge and performance improvement
- **Figure 5**: L1 Cache Hit/Miss Rate Comparison
- **Figure 6**: Branch Prediction Accuracy
- **Figure 7**: Instruction Type Distribution pie chart

**Usage:**
```bash
# Generate all figures (300 DPI, publication quality)
python3 plot_results.py --all

# Generate specific figures
python3 plot_results.py --cpi --speedup --cache
```

**Output:**
- PNG files with professional formatting
- 300 DPI resolution for publication
- Ready to include in LaTeX or Word documents

**Requirements:**
```bash
pip install matplotlib pandas numpy
```

### `run_full_analysis.sh` (New!)
Interactive bash script that:
- Provides menu-driven interface
- Checks prerequisites (gem5, benchmark)
- Runs selected simulation mode
- Automatically calls analyzer
- Generates complete report

**Recommended for first-time use:**
```bash
./run_full_analysis.sh
```

### `JOURNAL_GUIDE.md` (New!)
Complete guide for using results in academic publication:
- How to interpret metrics for journal
- Expected results and benchmarks
- Tables and graphs templates
- Example interpretations
- Troubleshooting section
- Tips for discussion section

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

#### Quick Start (Interactive Mode - Recommended for Journal)
```bash
chmod +x run_full_analysis.sh
./run_full_analysis.sh
```
Choose option 4 (Full Analysis) to run complete simulation and generate comparison report.

#### Individual CPU Simulations

**Non-Pipelined (TIMING):**
```bash
python3 simulasi_jurnal.py --cpu timing
```

**Pipelined (MINOR):**
```bash
python3 simulasi_jurnal.py --cpu minor
```

**Both with Comparison:**
```bash
python3 simulasi_jurnal.py --compare
```

**Full Analysis (Generates JSON Report):**
```bash
python3 simulasi_jurnal.py --all
```

### Step 3: Analyze Results

```bash
# Analyze with console report
python3 analyze_results.py --all

# Generate JSON report for further processing
python3 analyze_results.py --all --json

# Analyze specific CPU only
python3 analyze_results.py --timing
python3 analyze_results.py --minor
```

### Step 4: Generate Publication-Quality Figures

```bash
# Generate all figures (CPI, IPC, Speedup, Cache, Branch Pred, etc.)
python3 plot_results.py --all

# Generate specific figures
python3 plot_results.py --cpi --speedup --cache --branch

# Figures are saved as PNG files (300 DPI) ready for publication
```

### Step 5: Extract Data for Journal

The complete pipeline generates:
1. **Console Report**: Performance metrics, hazard analysis, comparison tables
2. **JSON Report** (`simulation_results.json`): Structured data for plots and further analysis
3. **Publication Figures** (PNG files): 7 high-resolution figures for your paper
4. **Raw Stats**: `m5out_TIMING/stats.txt` and `m5out_MINOR/stats.txt` (gem5 native format)

**Key Metrics for Publication:**
- **Speedup**: Performance improvement ratio (MINOR vs TIMING)
- **CPI/IPC**: Instructions per cycle (pipeline efficiency indicator)
- **Hazard Rate**: Branch squash percentage (control hazard indicator)
- **Cache Hit Rate**: Memory hierarchy efficiency
- **Stall Cycles**: Estimated cycle loss due to hazards

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

## 📊 Output Format & Journal Integration

### Console Report Example
The analyzer produces formatted tables with key metrics:

```
PERFORMANCE METRICS
- Total Instructions Executed: 80,121 insts
- Total CPU Cycles: 101,846 cycles
- Cycles Per Instruction (CPI): 1.2712 cycles/inst
- Instructions Per Cycle (IPC): 0.7867 inst/cycle

CACHE PERFORMANCE - L1 DATA CACHE
- Cache Hits: 27,907 accesses
- Cache Misses: 226 accesses
- Total Accesses: 28,133 accesses
- Miss Rate: 0.80%
- Hit Rate: 99.20%

BRANCH PREDICTION
- Branch Lookups: 15,588 branches
- Branch Squashes (Mispred.): 1,577 branches
- Branch Accuracy: 89.88%
- Misprediction Rate: 10.12%
```

### Key Metrics for Journal

| Metric | Purpose | Interpretation |
|--------|---------|-----------------|
| **Speedup** | Shows pipeline benefit | Speedup > 1.0 = pipelining effective |
| **CPI Improvement** | Quantifies hazard impact | Lower CPI = better performance |
| **Hazard Cycles** | Estimates stall cost | Difference between TIMING and MINOR cycles |
| **Branch Accuracy** | Control hazard indicator | Higher = better branch prediction |
| **Cache Hit Rate** | Memory efficiency | Higher = less memory stalls |

### JSON Report Structure
```json
{
  "timestamp": "2026-06-20T10:30:00",
  "benchmark": "hazard_test",
  "isa": "RISC-V",
  "timing_results": {
    "simInsts": 80121,
    "numCycles": 101846,
    "cpi": 1.2712,
    "ipc": 0.7867,
    ...
  },
  "minor_results": {
    "simInsts": 80121,
    "numCycles": 101846,
    "cpi": 0.7867,
    "ipc": 1.2712,
    ...
  },
  "comparison": {
    "speedup": 1.27,
    "improvement_percentage": 21.2
  }
}
```

## 🎓 For Your Journal

### Recommended Workflow

1. **Run Full Analysis**
   ```bash
   ./run_full_analysis.sh  # Select option 4
   ```

2. **Review Console Report**
   - Check speedup value
   - Verify hazard metrics make sense
   - Ensure cache behavior is expected

3. **Generate Figures from JSON**
   ```bash
   # Use simulation_results.json with:
   # - Python (matplotlib/pandas)
   # - Excel/LibreOffice
   # - Your favorite plotting tool
   ```

4. **Create Tables for Paper**
   - Copy metrics from console report
   - Format into LaTeX or Markdown tables
   - Reference paper requirements

5. **Write Discussion**
   - Use JOURNAL_GUIDE.md as reference
   - Include speedup explanation
   - Discuss hazard impact
   - Suggest future optimizations

### Sample Journal Sections

**Results Section:**
> "Simulasi menunjukkan bahwa MINOR CPU (pipelined) memberikan speedup 1.27x 
> dibandingkan TIMING CPU (non-pipelined), dengan pengurangan total cycles 
> sebesar 21,725 (dari 101,846 menjadi 80,121 cycles). Walaupun achievable 
> CPI meningkat dari 1.0 menjadi 1.27 due to pipeline depth, pipelining tetap 
> memberikan significant benefit karena dapat mengexecute multiple instructions 
> per cycle dalam kondisi ideal."

**Discussion Section:**
> "Analisis hazard menunjukkan bahwa branch prediction misprediction rate 
> mencapai 10.12%, yang merupakan primary contributor terhadap performance 
> degradation. Setiap misprediction menyebabkan pipeline flush dengan cost 
> ~4-5 cycles. Dengan implementasi better branch prediction mechanism 
> (misalnya hybrid predictor dengan lebih banyak history bits), performance 
> dapat ditingkatkan lebih lanjut."

## ✅ Verification Checklist

Before submitting journal:
- [ ] Run `./run_full_analysis.sh` option 4
- [ ] Verify speedup value > 1.0 (indicates successful pipelining)
- [ ] Check CPI_MINOR < CPI_TIMING (pipeline improvement visible)
- [ ] Confirm branch accuracy reasonable (typically 85-95%)
- [ ] Verify JSON report generated successfully
- [ ] Review JOURNAL_GUIDE.md for interpretation tips
- [ ] Create tables and figures from results
- [ ] Cross-reference metrics in text with figures

## ✏️ Notes

- Output statistics are logged by gem5 in separate directories (m5out_TIMING/ and m5out_MINOR/)
- Simulation results vary based on gem5 version and build configuration
- For detailed raw statistics, examine m5out_TIMING/stats.txt and m5out_MINOR/stats.txt
- The analyzer automatically parses these files and generates readable reports
- JSON report can be used for further data processing or visualization
- **NEW**: See [JOURNAL_GUIDE.md](JOURNAL_GUIDE.md) for complete guide on using results in academic publication

## 🎯 What This Project Demonstrates

### 1. **Pipeline Effectiveness**
- Speedup calculation shows real performance benefits of pipelining
- CPI comparison demonstrates instruction-level parallelism

### 2. **Hazard Impact Analysis**
- **Data Hazards**: Visible through cache miss behavior and register dependencies
- **Control Hazards**: Measured via branch prediction accuracy and pipeline flushes
- **Structural Hazards**: Limited in single-core in-order design but measurable through contention

### 3. **Stall Quantification**
- Cycle difference between TIMING and MINOR CPUs estimates total stall cycles
- Hazard-related stalls per instruction calculated from statistics

### 4. **Branch Prediction Accuracy**
- Real measurement of control hazard impact
- Branch squash rate directly correlates to pipeline efficiency loss

## 📚 References

- [gem5 Documentation](http://www.gem5.org/)
- [RISC-V ISA Specification](https://riscv.org/)
- [Computer Architecture: A Quantitative Approach](https://en.wikipedia.org/wiki/Computer_Architecture:_A_Quantitative_Approach)
- Hennessy & Patterson: Pipeline Hazards (Chapter 4)

## 📄 License

Project-specific license information here (if applicable)

---

**Project Name**: Pipeline-Simulator  
**Target**: Journal Publication  
**Author**: Your Name  
**Last Updated**: 2026-06-20  
**Status**: ✅ Ready for Simulation and Analysis  

## 🚀 Quick Start
```bash
# 1. Make script executable
chmod +x run_full_analysis.sh

# 2. Run interactive analysis
./run_full_analysis.sh

# 3. Choose option 4 (Full Analysis) for complete results
# 4. Review console output and simulation_results.json
# 5. Check JOURNAL_GUIDE.md for interpretation tips
```
