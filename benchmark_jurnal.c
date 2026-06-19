#include <stdio.h>

// Fungsi mewakili komputasi intensif (Data Hazard & ILP)
void operasi_matematika() {
    int a = 12, b = 23, c = 34, d = 45;
    int x, y, z;
    
    // Rangkaian RAW (Read After Write) Hazard yang padat
    x = a + b;  // Membutuhkan waktu eksekusi
    y = x * c;  // Hazard: bergantung pada nilai x
    z = y - d;  // Hazard: bergantung pada nilai y
    
    // Supaya kompiler tidak menghapus variabel z
    if (z == 0) printf(" "); 
}

// Fungsi mewakili percabangan (Control Hazard & Branch Prediction)
void operasi_percabangan() {
    int hitung_benar = 0;
    
    // Loop besar untuk melihat pola prediksi cabang
    for (int i = 0; i < 500; i++) {
        // Pola buatan: Selang-seling genap ganjil untuk menantang prediktor dinamis/hybrid
        if (i % 2 == 0) {
            hitung_benar += 2;
        } else {
            hitung_benar -= 1;
        }
    }
}

int main() {
    printf("--- MEMULAI CUSTOM MICROBENCHMARK RISC-V ---\n");
    
    // Jalankan berulang kali agar siklus instruksi di gem5 mencapai ribuan
    for (int i = 0; i < 10; i++) {
        operasi_matematika();
        operasi_percabangan();
    }
    
    printf("--- BENCHMARK SELESAI ---\n");
    return 0;
}