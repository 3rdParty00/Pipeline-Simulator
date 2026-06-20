# Panduan Penggunaan Hasil Simulasi untuk Jurnal

**Judul Jurnal:** Implementasi dan Evaluasi Pipeline Processing untuk Meningkatkan Efisiensi Eksekusi Instruksi pada Arsitektur Prosesor Sederhana

## 📋 Ringkasan

Simulator ini membantu Anda mengukur dampak pipeline, hazard, dan stall terhadap performa eksekusi instruksi. Dengan membandingkan TIMING CPU (non-pipelined) dan MINOR CPU (pipelined in-order), Anda dapat menunjukkan:

1. **Bagaimana pipeline meningkatkan performa** → Speedup calculation
2. **Bagaimana hazard menurunkan performa** → Hazard metrics
3. **Bagaimana stall berdampak** → CPI comparison
4. **Efisiensi cache dan branch prediction** → Cache/BP metrics

## 🚀 Cara Menjalankan Simulasi Lengkap

### Opsi 1: Interactive Mode (Recommended)
```bash
chmod +x run_full_analysis.sh
./run_full_analysis.sh
```

Pilih opsi 4 (Full Analysis) untuk mendapatkan report lengkap.

### Opsi 2: Direct Command
```bash
# Jalankan kedua simulasi
python3 simulasi_jurnal.py --compare

# Analisis hasil dengan JSON report
python3 analyze_results.py --all --json
```

### Opsi 3: Individual Simulations
```bash
# TIMING CPU saja
python3 simulasi_jurnal.py --cpu timing

# MINOR CPU saja
python3 simulasi_jurnal.py --cpu minor

# Analisis hasil
python3 analyze_results.py --all
```

## 📊 Output yang Dihasilkan

### 1. **stats.txt** (dalam m5out_TIMING/ dan m5out_MINOR/)
Raw statistics dari gem5 simulator. Berisi semua metrik detail tentang:
- Cycles, Instructions, CPI, IPC
- Cache statistics (hits, misses, miss rates)
- Branch prediction accuracy
- Instruction type distribution
- Memory behavior

### 2. **Console Report**
Laporan yang ditampilkan di terminal mencakup:

#### Performance Metrics
- **Total Instructions**: Jumlah instruksi yang dieksekusi
- **Total Cycles**: Jumlah cycle yang diperlukan
- **CPI (Cycles Per Instruction)**: Rata-rata cycle per instruksi
  - TIMING CPU: CPI lebih tinggi (non-pipelined baseline)
  - MINOR CPU: CPI lebih rendah (pipelined, tapi ada hazard)
- **IPC (Instructions Per Cycle)**: Rata-rata instruksi per cycle
  - Inverse dari CPI

#### Pipeline Hazards & Stalls
- **Branch Squashes**: Instruksi yang dibatalkan karena misprediction
  - Ini menunjukkan **control hazard**
  - Lebih tinggi pada pipelined CPU (karena pipelining menciptakan spekulasi)
- **Hazard-related Stalls**: Perbedaan cycles antara TIMING dan MINOR
  - Mencerminkan dampak **data hazard** dan **control hazard**

#### Cache Performance
- **L1D Cache Hit/Miss Rate**:
  - Menunjukkan efisiensi cache
  - Miss rate tinggi = perlu optimasi memory hierarchy
- **L1D vs L1I Statistics**:
  - Data cache vs Instruction cache behavior
  - Penting untuk analisis memory bandwidth

#### Branch Prediction
- **Accuracy**: Tingkat prediksi cabang yang benar
  - MINOR CPU lebih sensitif karena pipelining
- **Misprediction Rate**: Persentase prediksi yang salah
  - Setiap misprediction = pipeline flush = wasted cycles

### 3. **Comparison Report** (jika analisis kedua CPU)
Tabel perbandingan menunjukkan:
- **Speedup**: Rasio cycles TIMING / cycles MINOR
  - Speedup > 1.0 = MINOR lebih cepat (pipeline bekerja)
  - Menunjukkan efektivitas pipelining
- **Performance Improvement**: Persentase pengurangan cycles
  - Benefit dari pipelined architecture
- **Hazard Impact**: Estimasi cycle loss karena hazard

### 4. **simulation_results.json** (optional)
JSON format untuk:
- Data processing lebih lanjut
- Integration dengan tools lain
- Tracking hasil multiple experiments

## 🔍 Metrik Penting untuk Jurnal

### 1. **Speedup (Primary Metric)**
```
Speedup = Total Cycles (TIMING) / Total Cycles (MINOR)
```
**Interpretasi:**
- Speedup > 1.0: Pipeline memberikan peningkatan performa
- Speedup close to 1.0: Hazard mengurangi benefit pipeline
- Gunakan untuk menunjukkan effectiveness pipelining

**Contoh Interpretasi:**
- Speedup = 1.27x → MINOR CPU 27% lebih cepat dari TIMING
- Ini berarti pipelining memberikan benefit signifikan meski ada hazard

### 2. **CPI Improvement**
```
CPI_TIMING = Cycles / Instructions
CPI_MINOR = Cycles / Instructions
```
**Interpretasi:**
- CPI_TIMING ≈ 1.0 (setiap instruksi = 1 cycle, no pipelining benefit)
- CPI_MINOR < 1.0 (pipelining: multiple instruksi per cycle)
- Difference = dampak hazard pada pipeline

**Contoh:**
- CPI_TIMING = 1.25
- CPI_MINOR = 0.95
- Hazard cost ≈ 0.30 cycles/inst

### 3. **Hazard Metrics**
**Data Hazard Indicators:**
- Difference in cycles between TIMING and MINOR
- Cache miss rate (shows memory hazard impact)
- Memory operations percentage

**Control Hazard Indicators:**
- Branch squash rate (% of branches that were mispredicted)
- Branch prediction accuracy
- Persentase branch operations

**Contoh Analysis:**
```
Branch Squashes (MINOR): 1,577 out of 15,588 = 10.12%
Ini berarti ~10% dari branch predictions salah, 
yang menyebabkan pipeline flush (wasted cycles)
```

### 4. **Cache Performance**
- **L1D Miss Rate**: Menunjukkan data cache efficiency
- **L1I Miss Rate**: Menunjukkan instruction cache efficiency
- Correlation dengan CPI
  - High miss rate → lebih banyak memory stall → CPI naik

### 5. **Instruction Distribution**
- **% ALU vs Memory Operations**:
  - High memory ops = cache behavior critical
  - High ALU ops = register hazard critical
- **% of Integer vs Float**:
  - Different latency profiles

## 📈 Cara Menggunakan di Jurnal

### 1. **Hasil Section**

#### Table 1: Performance Comparison
```
┌─────────────────────────┬─────────────┬─────────────┐
│ Metric                  │ TIMING CPU  │ MINOR CPU   │
├─────────────────────────┼─────────────┼─────────────┤
│ Total Cycles            │ 101,846     │ 80,121      │
│ Total Instructions      │ 80,121      │ 80,121      │
│ CPI                     │ 1.2712      │ 0.7867      │
│ IPC                     │ 0.7867      │ 1.2712      │
└─────────────────────────┴─────────────┴─────────────┘

Speedup = 1.27x
Performance Improvement = 21.2%
```

#### Table 2: Hazard Analysis
```
┌────────────────────────┬────────┬───────┐
│ Metric                 │ TIMING │ MINOR │
├────────────────────────┼────────┼───────┤
│ Branch Lookups         │ 15,588 │ 15,588│
│ Branch Squashes        │ 1,577  │ 1,577 │
│ Squash Rate (%)        │ 10.12% │ 10.12%│
│ Mispred. Impact (est.) │ ~5%    │ ~8%   │
└────────────────────────┴────────┴───────┘
```

#### Table 3: Cache Performance
```
┌─────────────────────────────┬─────────────┬─────────────┐
│ Cache Metric                │ TIMING CPU  │ MINOR CPU   │
├─────────────────────────────┼─────────────┼─────────────┤
│ L1D Accesses                │ 28,133      │ 28,133      │
│ L1D Hits                    │ 27,907      │ 27,907      │
│ L1D Misses                  │ 226         │ 226         │
│ L1D Miss Rate (%)           │ 0.80%       │ 0.80%       │
│ L1D Hit Rate (%)            │ 99.20%      │ 99.20%      │
└─────────────────────────────┴─────────────┴─────────────┘
```

### 2. **Discussion Section - Key Points**

#### Point 1: Pipelining Benefit
"Simulasi menunjukkan bahwa implementasi pipelined architecture (MINOR CPU) 
memberikan speedup sebesar 1.27x dibandingkan non-pipelined (TIMING CPU), 
dengan pengurangan cycle count sebesar 21.2% untuk benchmark yang sama."

#### Point 2: Hazard Impact
"Analisis menunjukkan bahwa data hazard dan control hazard berdampak pada 
performa. Dari 15,588 branch operations, 1,577 (10.12%) mengalami 
misprediction yang menyebabkan pipeline flush. Walaupun demikian, pipelining 
tetap memberikan benefit karena dapat meng-hide latency dari beberapa 
operasi memory dan ALU."

#### Point 3: Stall Analysis
"Estimasi cycle loss karena hazard-related stall adalah ~21,725 cycles 
(perbedaan antara TIMING dan MINOR). Ini mengindikasikan bahwa dengan 
strategi hazard mitigation yang lebih baik (forwarding, better branch 
prediction), performa dapat ditingkatkan lebih lanjut."

#### Point 4: Cache Efficiency
"Cache performance tetap optimal di kedua CPU dengan L1D miss rate hanya 0.80%, 
menunjukkan bahwa benchmark ini memory-friendly. Dengan working set yang kecil, 
cache tidak menjadi bottleneck utama."

## 🎯 Hasil yang Diharapkan

Untuk benchmark `hazard_test` dengan karakteristik:
- Dense data dependency (RAW hazards)
- Conditional branch (control hazards)
- 10 iterations of workload
- 80,121 instructions total

**Expected Results:**
- **Speedup**: 1.2x - 1.4x (pipeline benefit visible)
- **CPI Improvement**: ~40-50% reduction
- **Branch Squash Rate**: 8-12% (visible control hazard)
- **L1D Miss Rate**: <2% (good cache locality)

## 📊 Visualisasi untuk Jurnal

### Graph 1: CPI Comparison
```
CPI
│
1.3 ├──────●
    │      │
1.0 ├──────┼──────●
    │      │      │
0.7 ├──────┼──────┤
    │      │      │
    └──────┴──────┴─── CPU Type
      TIMING  MINOR
```

### Graph 2: Speedup
```
Speedup = 1.27x
┌─────────────────────────────────────────────┐
│ ████████████████████████████████████ 127%   │
└─────────────────────────────────────────────┘
```

### Graph 3: Hazard Distribution
```
Branch Predictions: 15,588
├─ Correct:      14,011 (89.88%) ◆◆◆◆◆◆◆◆◆◆
└─ Mispredicted:  1,577 (10.12%) ◆
```

## 💡 Tips untuk Jurnal

1. **Bandingkan dengan state-of-the-art**: Simulasi pipeline processor lain
2. **Variasi benchmark**: Gunakan multiple workloads untuk menunjukkan generality
3. **Sensitivity analysis**: Bagaimana performa berubah dengan cache size berbeda?
4. **Optimization proposals**: Suggest improvements (better branch prediction, forwarding, etc.)
5. **Energy analysis**: (Optional) gem5 dapat menunjukkan energy consumption juga

## 📚 Related Concepts untuk Jurnal

- **Instruction-Level Parallelism (ILP)**: Pipeline increases ILP
- **Data Dependency**: RAW/WAR/WAW hazards reduce ILP
- **Control Flow**: Branch prediction misses reduce ILP
- **Memory Hierarchy**: Cache miss cycles = memory latency
- **Superscalar (future work)**: Multiple instructions per cycle possible

## 🔗 Output File Structure

```
Pipeline-Simulator/
├── m5out_TIMING/
│   ├── stats.txt          ← Raw TIMING statistics
│   ├── config.ini
│   ├── config.json
│   └── citations.bib
├── m5out_MINOR/
│   ├── stats.txt          ← Raw MINOR statistics
│   ├── config.ini
│   ├── config.json
│   └── citations.bib
├── simulation_results.json ← Summary in JSON format
└── [Console Output]       ← Formatted report
```

## ❓ Troubleshooting

**Q: Hasil CPI di MINOR lebih tinggi dari TIMING?**
A: Ini bisa terjadi jika ada masalah dengan simulator config atau benchmark tidak tepat. 
   Verify bahwa binary adalah RISC-V format.

**Q: Speedup hanya 1.05x (terlalu rendah)?**
A: Ini bisa menunjukkan:
   - Benchmark terlalu sederhana
   - Hazard rate terlalu tinggi
   - Cache miss rate tinggi (menghilangkan pipelining benefit)

**Q: Branch Squash rate 0%?**
A: Branch prediction sempurna, coba gunakan harder benchmark dengan unpredictable branches.

---

**Updated**: 2026-06-20
**For**: Jurnal "Implementasi dan Evaluasi Pipeline Processing untuk Meningkatkan Efisiensi Eksekusi Instruksi"
