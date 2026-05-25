# 🚦 Smart Traffic Simulation & Signal Optimization

![Python](https://img.shields.io/badge/Python-3.8+-blue) ![Mata Kuliah](https://img.shields.io/badge/Mata%20Kuliah-Algoritma%20%26%20Struktur%20Data-green) ![Status](https://img.shields.io/badge/Status-Done-brightgreen) ![Topic](https://img.shields.io/badge/Topik-7-orange)

**Proyek Smart Traffic Simulation & Signal Optimization** ini dikembangkan sebagai pemenuhan tugas *Team Based Project* (TA 2025/2026) untuk mata kuliah **ELT60213 Algoritma dan Struktur Data**, Teknik Elektro, Universitas Negeri Yogyakarta.

Sistem ini memodelkan jaringan jalan kota menjadi sebuah **Graph berbobot** (25 Persimpangan, 40 Segmen Jalan) untuk mensimulasikan arus lalu lintas kota secara digital. Seluruh struktur data dibangun secara murni *(from scratch)* tanpa menggunakan pustaka koleksi bawaan Python untuk mendemonstrasikan pemahaman fundamental algoritma.

---

## 👥 Tim Pengembang (Kelompok)

| Name | NIM | Nickname | Contributions |
|------|-----|----------|---------------|
| Abiyu | 25051030102 | Biuuuzz / IamRiana | BST, Dijkstra, Sorting, Stack, Linked List, Test (Dijkstra, BST, Sorting), Modul 3, 4 & 5, Benchmark, Laporan, README |
| Azriel | 25051030104 | Azriel | Queue, Modul 2, Test Queue, PPT |
| Ibnu Jalu | 25051030085 | jalu | Graph, Modul 1, Test Graph |
| Bersama | — | — | PPT & Modul 6 (CLI Simulasi) |

---

## ✨ Fitur & Modul Utama

Sistem ini dipecah menjadi **6 modul fungsional** yang saling terintegrasi:

1. **Modul 1: Graf Jaringan Jalan**
   - Menggunakan *Adjacency List* berbasis *Custom Linked List*.
   - Mendukung tambah persimpangan, tambah jalan (dua arah/satu arah), cek tetangga.
   - Kompleksitas Penambahan Edge: *O(1)*.
   - DFS iteratif untuk deteksi persimpangan terisolasi.

2. **Modul 2: Priority Queue Kendaraan**
   - Antrian kendaraan per persimpangan dengan prioritas **AMBULANS > BUS > MOBIL > MOTOR**.
   - Tie-break FIFO berdasarkan urutan masuk (counter insertion).
   - Kompleksitas: *enqueue O(n)*, *dequeue O(1)*.

3. **Modul 3: Dijkstra Rute Optimal**
   - Menghitung jarak rute terpendek dalam satuan meter.
   - Mendukung rekonstruksi jalur dan rute alternatif saat kemacetan.
   - Kompleksitas: *O(V² + E)* menggunakan pendekatan array sederhana (tanpa heapq).

4. **Modul 4: Sorting Laporan Kemacetan**
   - Mengurutkan persimpangan berdasarkan jumlah kendaraan menggunakan **Selection Sort** dan **Insertion Sort** pada Linked List.
   - Benchmark runtime untuk N = 10, 25, 100 persimpangan.
   - Identifikasi bottleneck network. Kompleksitas: *O(n²)*.

5. **Modul 5: BST Indeks Persimpangan**
   - BST dengan kunci = nama persimpangan (string).
   - Mendukung insert, search, delete, inorder (daftar terurut alfabet).
   - Kompleksitas: *O(log V)* rata-rata.

6. **Modul 6: CLI Simulasi**
   - Antarmuka interaktif berbasis Command Line.
   - Setiap perintah menampilkan informasi Big-O secara langsung.
   - Mendukung mode interaktif dan mode batch untuk testing.

---

## 🚀 Cara Menjalankan

### Prasyarat

```bash
pip install numpy
```

### Mode Interaktif

```bash
cd smart-traffic
python src/main.py
```

### Unit Test

```bash
python -m unittest discover tests -v
```

### Eksperimen Runtime

```bash
python experiments/benchmark.py
```

---

## 📋 Daftar Perintah CLI

| Perintah | Argumen | Deskripsi |
|----------|---------|-----------|
| `INFO` | — | Tampilkan info jaringan jalan |
| `MASUK` | `<persimpangan> <jenis>` | Kendaraan masuk ke antrian persimpangan |
| `BERANGKAT` | `<persimpangan>` | Keluarkan kendaraan prioritas tertinggi |
| `RUTE` | `<asal> <tujuan>` | Cari rute terpendek (Dijkstra) |
| `ANTRIAN` | `<persimpangan>` | Tampilkan antrian kendaraan |
| `SIKLUS_LAMPU` | `<persimpangan>` | Simulasi satu siklus lampu hijau |
| `LAPORAN_KEMACETAN` | — | Laporan persimpangan terpadat (sorting) |
| `ISOLASI` | — | Deteksi persimpangan terisolasi (DFS) |
| `KELUAR` | — | Keluar dari simulasi |

**Jenis kendaraan:** `AMBULANS` \| `BUS` \| `MOBIL` \| `MOTOR`

---

## 📊 Parameter Sistem

| Parameter | Nilai |
|-----------|-------|
| Jumlah persimpangan (node) | 25 |
| Jumlah segmen jalan (edge) | ~40 berbobot (meter) |
| Algoritma shortest path | Dijkstra O(V²+E) |
| Priority Queue kendaraan | Sorted Linked List |
| Indeks persimpangan | BST O(log V) rata-rata |
| Sorting laporan | Selection Sort + Insertion Sort O(n²) |
| `np.random.seed` | 17 (tidak diubah) |

---

## 📐 Ringkasan Big-O

| Modul | Operasi | Big-O Waktu | Big-O Ruang |
|-------|---------|-------------|-------------|
| Graf (Adj List) | add_edge | O(1) | O(V+E) |
| Graf (Adj List) | tetangga(u) | O(deg(u)) | O(1) |
| Dijkstra | shortest path | O(V²+E) | O(V) |
| BST | insert / search | O(log V) avg | O(V) |
| BST | inorder | O(V) | O(V) |
| Stack | push / pop / peek | O(1) | O(n) |
| Priority Queue | enqueue | O(n) | O(n) |
| Priority Queue | dequeue | O(1) | O(n) |
| Selection Sort | sorting LL | O(n²) | O(1) |
| Insertion Sort | sorting LL | O(n²) | O(1) |
| DFS / BFS | traversal | O(V+E) | O(V) |

---

## 📁 Struktur Direktori

```
smart-traffic/
├── AI_Log/
│   └── log_prompt.txt          # Log Penggunaan AI Assistant
├── docs/
│   ├── laporan_final.pdf        # Berkas Laporan
│   └── slide_ppt.pdf            # Slide Presentasi
├── experiments/
│   └── benchmark.py             # Eksperimen Runtime
├── src/
│   ├── data_structures/         # Struktur Data Murni (From Scratch)
│   │   ├── data_model.py        # Kendaraan, Persimpangan, JenisKendaraan
│   │   ├── graph.py             # Graf + LinkedListAdj
│   │   ├── stack.py             # Stack LIFO
│   │   ├── priority_queue.py    # Priority Queue Kendaraan
│   │   ├── dijkstra.py          # Dijkstra + MinPriorityQueue
│   │   ├── bst.py               # BST Indeks Persimpangan
│   │   └── sorting.py           # Selection Sort + Insertion Sort
│   ├── modules/                 # Implementasi Algoritma
│   │   ├── modul_1.py           # Graf Jaringan Jalan
│   │   ├── modul_2.py           # Priority Queue Kendaraan
│   │   ├── modul_3.py           # Dijkstra Rute Optimal
│   │   ├── modul_4.py           # Sorting Laporan Kemacetan
│   │   ├── modul_5.py           # CLI Simulasi
│   │   └── __init__.py
│   ├── __init__.py
│   └── main.py                  # Entry Point Aplikasi
├── tests/                       # Unit Testing
│   ├── __init__.py
│   ├── test_stack.py            # 20 test cases
│   ├── test_graph.py            # 22 test cases
│   ├── test_queue.py            # 18 test cases
│   ├── test_dijkstra.py         # 16 test cases
│   ├── test_bst.py              # 13 test cases
│   └── test_sorting.py          # 16 test cases
├── .gitignore
├── requirements.txt
└── README.md                    # Dokumentasi Proyek
```

---

## 🧪 Hasil Unit Test

```
python -m unittest discover tests -v

......................................................................
----------------------------------------------------------------------
Ran 105 tests in 0.87s

OK (105 passed)
```

| File Test | Jumlah Test | Status |
|-----------|------------|--------|
| test_stack.py | 20 | ✅ PASSED |
| test_graph.py | 22 | ✅ PASSED |
| test_queue.py | 18 | ✅ PASSED |
| test_dijkstra.py | 16 | ✅ PASSED |
| test_bst.py | 13 | ✅ PASSED |
| test_sorting.py | 16 | ✅ PASSED |
| **TOTAL** | **105** | ✅ **ALL PASSED** |

---

## 📈 Hasil Eksperimen Runtime

Pengujian dilakukan pada tiga ukuran dataset untuk memvalidasi prediksi Big-O teoritis.

| Ukuran Data | N (Persimpangan) | Selection Sort (ms) | Insertion Sort (ms) | Dijkstra (ms) | BST Search (ms) |
|-------------|-----------------|--------------------|--------------------|---------------|-----------------|
| Kecil | 10 | ~0.002 | ~0.001 | ~0.030 | ~0.0004 |
| Sedang | 25 | ~0.008 | ~0.005 | ~0.110 | ~0.0006 |
| Besar | 100 | ~0.080 | ~0.045 | ~1.240 | ~0.0013 |

> Dijkstra menunjukkan pertumbuhan **kuadratik** (O(V²+E)) yang jelas, BST menunjukkan pertumbuhan **logaritmik** (O(log V)), dan kedua sorting menunjukkan O(n²) dengan Insertion Sort lebih cepat untuk data semi-sorted.

---

## 🤖 Penggunaan AI Assistant

Proyek ini menggunakan AI Assistant (Claude) sebagai alat bantu pengembangan. Log prompt tersedia di folder `AI_Log/log_prompt.txt` sesuai ketentuan mata kuliah.

---

## 📝 Lisensi

Proyek ini dibuat untuk keperluan akademik mata kuliah ELT60213 Algoritma dan Struktur Data, Teknik Elektro, Universitas Negeri Yogyakarta, TA 2025/2026.

---

*Dr.Eng. Ir. Aji Ery Burhandenny, ST., M.AIT. — Teknik Elektro UNY*