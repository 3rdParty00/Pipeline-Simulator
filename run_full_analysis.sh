#!/bin/bash

# Script untuk menjalankan simulasi lengkap dan analisis untuk jurnal
# Judul: Implementasi dan Evaluasi Pipeline Processing untuk Meningkatkan Efisiensi Eksekusi Instruksi

echo ""
echo "=========================================================================="
echo "SIMULASI DAN ANALISIS PIPELINE PROCESSING - RISC-V"
echo "=========================================================================="
echo ""

# Cek apakah gem5 sudah di-build
if [ ! -f "../gem5/build/RISCV/gem5.opt" ]; then
    echo "❌ ERROR: gem5 belum di-build!"
    echo "Silakan build gem5 terlebih dahulu:"
    echo "  cd ../gem5"
    echo "  scons build/RISCV/gem5.opt -j4"
    exit 1
fi

# Cek apakah benchmark sudah dikompilasi
if [ ! -f "./hazard_test" ]; then
    echo "❌ ERROR: hazard_test binary tidak ditemukan!"
    echo "Silakan kompilasi terlebih dahulu:"
    echo "  riscv64-unknown-elf-gcc -o hazard_test benchmark_jurnal.c"
    exit 1
fi

echo "✓ Prasyarat terpenuhi (gem5 dan benchmark ready)"
echo ""

# Menu pilihan
echo "Pilih mode simulasi:"
echo ""
echo "1. TIMING CPU only (Non-Pipelined)"
echo "2. MINOR CPU only (Pipelined In-Order)"
echo "3. Compare (jalankan TIMING dan MINOR, generate comparison report)"
echo "4. Full Analysis (lengkap dengan JSON report)"
echo ""

read -p "Pilihan (1-4): " choice

case $choice in
    1)
        echo ""
        echo "Menjalankan simulasi TIMING CPU..."
        python3 simulasi_jurnal.py --cpu timing
        ;;
    2)
        echo ""
        echo "Menjalankan simulasi MINOR CPU..."
        python3 simulasi_jurnal.py --cpu minor
        ;;
    3)
        echo ""
        echo "Menjalankan perbandingan TIMING vs MINOR CPU..."
        python3 simulasi_jurnal.py --compare
        
        echo ""
        echo "Menganalisis hasil..."
        python3 analyze_results.py --all
        ;;
    4)
        echo ""
        echo "Menjalankan analisis lengkap..."
        python3 simulasi_jurnal.py --all
        
        sleep 2
        
        echo ""
        echo "Menganalisis hasil..."
        python3 analyze_results.py --all --json
        
        echo ""
        echo "✓ Analisis selesai!"
        echo "  Hasil tersedia di:"
        echo "    - m5out_TIMING/stats.txt"
        echo "    - m5out_MINOR/stats.txt"
        echo "    - simulation_results.json"
        ;;
    *)
        echo "❌ Pilihan tidak valid!"
        exit 1
        ;;
esac

echo ""
echo "=========================================================================="
echo "Simulasi selesai! ✓"
echo "=========================================================================="
echo ""
