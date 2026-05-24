"""
src/main.py
═══════════════════════════════════════════════════════
MAIN – Entry Point Utama
Smart Traffic Simulation & Signal Optimization
ELT60213 Algoritma dan Struktur Data | Topik 7
═══════════════════════════════════════════════════════

Cara menjalankan:
    python src/main.py              → CLI interaktif
    python src/main.py --demo       → Demo 10 skenario
    python src/main.py --simulasi   → Simulasi 500 event penuh
    python src/main.py --analisis   → 5 pertanyaan analisis
"""

import sys, os, argparse, time, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data_model import SEED, VEHICLE_TYPES
from src.data_structures.graph import (
    build_traffic_graph
)
from src.data_structures.priority_queue import (
    TrafficQueueManager,
    Vehicle,
    VEHICLE_TYPES
)
from src.data_structures.dijkstra import (
    DijkstraSolver
)
from src.data_structures.bst import (
    build_intersection_bst
)
from src.data_structures.sorting import (
    buat_laporan,
    eksperimen_runtime
)


# ─────────────────────────────────────────────
# Mode: Demo Otomatis
# ─────────────────────────────────────────────

def mode_demo() -> None:
    """Demo 10 skenario otomatis."""
    print("\n" + "="*60)
    print("  DEMO OTOMATIS – Smart Traffic Simulation")
    print("="*60)

    # Setup semua modul
    graf = build_traffic_graph()
    nodes = graf.nodes
    manajer = TrafficQueueManager(nodes)
    solver = DijkstraSolver(graf)
    bst = build_intersection_bst(graf)

    random.seed(SEED)

    print(graf)
    print("Nodes:", graf.nodes)


    print("[2] Simulasi 20 event kendaraan...")
    for i in range(20):
        asal   = random.choice(nodes)
        tujuan = random.choice([n for n in nodes if n != asal])
        jenis  = random.choice(VEHICLE_TYPES)

        vehicle = Vehicle(
            jenis,
            asal,
            tujuan,
            arrival_time=float(i)
        )

        manajer.masuk(asal, vehicle)
    

    print("[3] Cari rute A1 → E5 (Dijkstra)...")
    jarak, jalur = solver.shortest_path("A1", "E5")

    print(f"Jarak : {jarak}")
    print(f"Jalur : {' → '.join(jalur)}")

    print("\n[4] Masukkan AMBULANS ke B3 dan berangkatkan...")
    vehicle = Vehicle(
    "AMBULANS",
    "A1",
    "B3",
    arrival_time=1000.0
)

    manajer.masuk("B3", vehicle)
    manajer.berangkat("B3")

    print("\n[5] Laporan kemacetan top-5...")
    dummy_counts = {}

    for nama in nodes:
        dummy_counts[nama] = manajer.antrian(nama).size()

    laporan = buat_laporan(nodes, dummy_counts)

    laporan.selection_sort()

    print(laporan.to_list()[:5])

    print("[6] Cari data BST...")
    node = bst.search("C3")
    if node:
        print(f"{node.key} → {node.data}")
    else:
        print("Data tidak ditemukan")


    print("\n" + "="*60)
    print("  Demo selesai.")
    print("="*60)


# ─────────────────────────────────────────────
# Mode: Simulasi Penuh 500 Event
# ─────────────────────────────────────────────

def mode_simulasi() -> None:
    """Simulasi 500 event + 50 query Dijkstra + laporan lengkap."""
    print("\n" + "="*60)
    print("  SIMULASI PENUH – 500 Event + 50 Query Dijkstra")
    print("="*60)

    t_global = time.perf_counter()

    graf    = build_traffic_graph()
    nodes = graf.nodes
    manajer = TrafficQueueManager(nodes)
    solver = DijkstraSolver(graf)
    bst = build_intersection_bst(graf)

    # 500 event
    # stats = simulasi_event(manajer, nodes, n_event=500, seed=17)

    # # 50 query Dijkstra
    # hasil_query = jalankan_50_query(solver, nodes)

    # Laporan kemacetan
    dummy_counts = {}

    for nama in nodes:
        dummy_counts[nama] = manajer.antrian(nama).size()

    laporan = buat_laporan(nodes, dummy_counts)

    laporan.selection_sort()

    print(laporan.to_list()[:5])

    # Eksperimen runtime sorting
    eks = eksperimen_runtime([10, 25, 100])
    # tampilkan_benchmark(eks)

    t_total = time.perf_counter() - t_global

    print(f"\n{'═'*60}")
    print(f"  RINGKASAN AKHIR")
    print(f"{'═'*60}")
    # r = stats.ringkasan()
    # print(f"  Total event      : {r['total_event']}")
    # print(f"  Kendaraan masuk  : {r['total_masuk']}")
    # print(f"  Kendaraan berangkat: {r['total_berangkat']}")
    # print(f"  AMBULANS masuk   : {r['total_ambulans']}")
    # print(f"  Query Dijkstra   : {stat_query.get('total_query',0)}")
    # print(f"  Jarak rata-rata  : {stat_query.get('jarak_rata',0):.0f}m")
    print(f"  Waktu total      : {t_total:.3f}s")
    print(f"{'═'*60}")


# ─────────────────────────────────────────────
# Mode: 5 Pertanyaan Analisis
# ─────────────────────────────────────────────

def mode_analisis() -> None:
    """Tampilkan 5 pertanyaan analisis lanjutan trade-off."""
    qa = [
        (
            "1. Mengapa Priority Queue pakai Min-Heap bukan array terurut?",
            "Array terurut butuh O(n) untuk insert (geser elemen). Min-Heap hanya "
            "O(log n). Untuk 500 event kendaraan, ini perbedaan signifikan. "
            "Trade-off: Heap lebih kompleks implementasinya, tapi jauh lebih "
            "efisien untuk data dinamis yang terus berubah."
        ),
        (
            "2. Mengapa Dijkstra pakai Min-Heap bukan matriks jarak O(V²)?",
            "Graf kota bersifat sparse (E << V²). Dengan 25 node dan ~40 edge, "
            "implementasi heap O((V+E) log V) ≈ O(65 × 4.6) ≈ 300 operasi, "
            "sedangkan array O(V²) = 625 operasi. Heap ~40% lebih cepat. "
            "Trade-off: heap lebih sulit di-debug, array lebih mudah dipahami."
        ),
        (
            "3. Apa trade-off Selection Sort vs Insertion Sort pada Linked List?",
            "Selection Sort selalu O(n²) tidak adaptif, namun jumlah swap O(n) "
            "lebih sedikit. Insertion Sort O(n²) worst-case tapi O(n) jika data "
            "hampir terurut. Laporan kemacetan berubah sedikit tiap siklus → "
            "Insertion Sort lebih efisien. Trade-off: Insertion Sort lebih "
            "kompleks pada Linked List karena tidak ada random-access."
        ),
        (
            "4. Mengapa BST bukan Hash Table untuk lookup persimpangan?",
            "Hash Table O(1) average lookup tapi tidak mendukung range query "
            "dan inorder traversal. BST O(log n) lookup tapi mendukung "
            "range_query('B1','C5') dan daftar terurut alami via inorder(). "
            "Untuk sistem yang butuh laporan terurut dan pencarian rentang, "
            "BST lebih fleksibel. Trade-off: BST lebih lambat dari Hash Table "
            "untuk lookup murni."
        ),
        (
            "5. Bottleneck mana yang paling memengaruhi performa simulasi?",
            "Sorting laporan O(n²) adalah bottleneck terbesar untuk n besar "
            "(n=100 → ~10.000 operasi). Dijkstra O((V+E) log V) untuk 50 query. "
            "Untuk skala kota besar (1000+ node): ganti Bubble/Selection Sort "
            "dengan Merge Sort O(n log n), dan Dijkstra bisa dipercepat dengan "
            "A* heuristik. BST bisa diganti AVL Tree untuk O(log n) terjamin."
        ),
    ]

    print("\n" + "="*65)
    print("  5 PERTANYAAN ANALISIS LANJUTAN – TRADE-OFF EFISIENSI")
    print("="*65)
    for q, a in qa:
        print(f"\n  Q: {q}")
        # Wrap jawaban per 60 karakter
        words = a.split()
        line  = "  A: "
        for word in words:
            if len(line) + len(word) > 65:
                print(line)
                line = "     " + word + " "
            else:
                line += word + " "
        print(line)
    print("\n" + "="*65)


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Smart Traffic Simulation & Signal Optimization"
    )
    parser.add_argument("--demo",      action="store_true",
                        help="Demo 10 skenario otomatis")
    parser.add_argument("--simulasi",  action="store_true",
                        help="Simulasi penuh 500 event + 50 query")
    parser.add_argument("--analisis",  action="store_true",
                        help="Tampilkan 5 pertanyaan analisis lanjutan")
    args = parser.parse_args()

    if args.demo:
        mode_demo()
    elif args.simulasi:
        mode_simulasi()
    elif args.analisis:
        mode_analisis()
    else:
        # Default: CLI interaktif
        mode_demo()
        # cli = TrafficCLI(seed=SEED)
        # cli.run()


if __name__ == "__main__":
    main()