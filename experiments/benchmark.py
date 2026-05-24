"""
experiments/benchmark.py
═══════════════════════════════════════════════════════════════
BENCHMARK – Eksperimen Perbandingan Performa Semua Struktur Data
Smart Traffic Simulation & Signal Optimization
ELT60213 Algoritma dan Struktur Data | Topik 7
═══════════════════════════════════════════════════════════════

Mengukur runtime semua operasi utama pada 3 ukuran dataset:
  N = 10, 25, 100 (simpul/kendaraan simulatif)

Struktur data yang diuji:
  1. Graph (Adjacency List)  — add_edge, neighbors, DFS
  2. Priority Queue (MinHeap) — enqueue, dequeue
  3. Dijkstra               — shortest path query
  4. BST                    — insert, search, inorder
  5. Linked List            — add_front, add_back, find
  6. Stack                  — push, pop
  7. Sorting (3 algoritma)  — bubble, insertion, selection

Output:
  - Tabel runtime per operasi di terminal
  - File hasil: experiments/hasil_benchmark.txt
  - Cocok langsung masuk Bab V Laporan PDF

Jalankan: python experiments/benchmark.py
"""

import sys, os, time, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data_structures.graph          import TrafficGraph, build_traffic_graph
from src.data_structures.priority_queue import MinHeap, IntersectionQueue
from src.data_structures.dijkstra       import DijkstraSolver
from src.data_structures.bst            import IntersectionBST
from src.data_structures.linked_list    import LinkedList
from src.data_structures.stack          import Stack
from src.data_structures.sorting        import CongestionLinkedList
from src.data_structures.data_model                     import SEED, VEHICLE_TYPES

UKURAN = [10, 25, 100]   # tiga ukuran dataset wajib
ULANG  = 5               # rata-rata dari 5 kali pengukuran
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "hasil_benchmark.txt")


# ─────────────────────────────────────────────
# Utilitas
# ─────────────────────────────────────────────

def ukur(fn, ulang: int = ULANG) -> float:
    """Jalankan fn() sebanyak `ulang` kali, kembalikan rata-rata detik."""
    total = 0.0
    for _ in range(ulang):
        t0 = time.perf_counter()
        fn()
        total += time.perf_counter() - t0
    return total / ulang


def buat_nama(n: int) -> list:
    random.seed(SEED)
    return [f"N{i:03d}" for i in range(n)]


def cetak_header(judul: str) -> None:
    print(f"\n{'═'*65}")
    print(f"  {judul}")
    print(f"{'═'*65}")


def cetak_tabel(kolom: list, baris: list) -> str:
    """Cetak tabel dan kembalikan sebagai string untuk disimpan."""
    lebar = [max(len(str(k)), max(len(str(b[i])) for b in baris))
             for i, k in enumerate(kolom)]
    garis = "  " + "─" * (sum(lebar) + len(lebar) * 3 + 1)
    header = "  │ " + " │ ".join(
        str(k).ljust(lebar[i]) for i, k in enumerate(kolom)
    ) + " │"

    lines = [garis, header, garis]
    for b in baris:
        row = "  │ " + " │ ".join(
            str(b[i]).ljust(lebar[i]) for i in range(len(kolom))
        ) + " │"
        lines.append(row)
    lines.append(garis)

    output = "\n".join(lines)
    print(output)
    return output


hasil_global = []   # kumpulkan semua output untuk disimpan


def log(text: str) -> None:
    print(text)
    hasil_global.append(text)


# ═══════════════════════════════════════════════════════════════
# BENCHMARK 1 — GRAPH
# ═══════════════════════════════════════════════════════════════

def bench_graph() -> None:
    cetak_header("BENCHMARK 1 – GRAPH (Adjacency List berbasis Linked List)")
    hasil_global.append("\n" + "="*65)
    hasil_global.append("BENCHMARK 1 – GRAPH")
    hasil_global.append("="*65)

    kolom = ["N (simpul)", "add_edge (s)", "neighbors (s)", "DFS (s)", "Big-O"]
    baris = []

    for n in UKURAN:
        random.seed(SEED)
        nodes = buat_nama(n)

        # add_edge: tambah n*2 edge
        def fn_add():
            g = TrafficGraph()
            for nd in nodes: g.add_intersection(nd)
            for _ in range(n * 2):
                s = random.choice(nodes)
                d = random.choice(nodes)
                g.add_road(s, d, random.randint(100, 1500))

        t_add = ukur(fn_add)

        # Siapkan graf sekali untuk tes berikutnya
        g = TrafficGraph()
        for nd in nodes: g.add_intersection(nd)
        random.seed(SEED)
        for _ in range(n * 2):
            s = random.choice(nodes)
            d = random.choice(nodes)
            g.add_road(s, d, random.randint(100, 1500))

        # neighbors: query semua node
        def fn_nbr():
            for nd in nodes:
                g.neighbors(nd)

        t_nbr = ukur(fn_nbr)

        # DFS dari node pertama
        t_dfs = ukur(lambda: g.dfs(nodes[0]))

        baris.append([
            n,
            f"{t_add:.6f}",
            f"{t_nbr:.6f}",
            f"{t_dfs:.6f}",
            "add O(1) | nbr O(deg) | DFS O(V+E)"
        ])

    tbl = cetak_tabel(kolom, baris)
    hasil_global.append(tbl)


# ═══════════════════════════════════════════════════════════════
# BENCHMARK 2 — PRIORITY QUEUE (Min-Heap)
# ═══════════════════════════════════════════════════════════════

def bench_priority_queue() -> None:
    cetak_header("BENCHMARK 2 – PRIORITY QUEUE (Min-Heap dari nol)")
    hasil_global.append("\n" + "="*65)
    hasil_global.append("BENCHMARK 2 – PRIORITY QUEUE")
    hasil_global.append("="*65)

    kolom = ["N kendaraan", "enqueue (s)", "dequeue (s)", "peek (s)", "Big-O"]
    baris = []

    for n in UKURAN:
        random.seed(SEED)

        from src.data_structures.priority_queue import Vehicle

        vehicles = [
            Vehicle(random.choice(VEHICLE_TYPES), "A", "B",
                    arrival_time=float(i))
            for i in range(n)
        ]

        # enqueue
        def fn_enq():
            q = IntersectionQueue("TEST")
            for v in vehicles:
                q.enqueue(v)

        t_enq = ukur(fn_enq)

        # dequeue (siapkan antrian terisi)
        def fn_deq():
            q = IntersectionQueue("TEST")
            for v in vehicles: q.enqueue(v)
            while not q.is_empty(): q.dequeue()

        t_deq = ukur(fn_deq)

        # peek
        q_peek = IntersectionQueue("PEEK")
        for v in vehicles: q_peek.enqueue(v)
        t_peek = ukur(lambda: q_peek.peek())

        baris.append([
            n,
            f"{t_enq:.6f}",
            f"{t_deq:.6f}",
            f"{t_peek:.6f}",
            "enq O(log n) | deq O(log n) | peek O(1)"
        ])

    tbl = cetak_tabel(kolom, baris)
    hasil_global.append(tbl)


# ═══════════════════════════════════════════════════════════════
# BENCHMARK 3 — DIJKSTRA
# ═══════════════════════════════════════════════════════════════

def bench_dijkstra() -> None:
    cetak_header("BENCHMARK 3 – DIJKSTRA (50 query rute per ukuran)")
    hasil_global.append("\n" + "="*65)
    hasil_global.append("BENCHMARK 3 – DIJKSTRA")
    hasil_global.append("="*65)

    kolom = ["N simpul", "1 query (s)", "50 query (s)", "rata/query (s)", "Big-O"]
    baris = []

    for n in UKURAN:
        random.seed(SEED)
        nodes = buat_nama(n)

        # Bangun graf
        g = TrafficGraph()
        for nd in nodes: g.add_intersection(nd)
        for _ in range(n * 2):
            s = random.choice(nodes)
            d = random.choice(nodes)
            g.add_road(s, d, random.randint(100, 1500))

        solver = DijkstraSolver(g)

        # 1 query
        t1 = ukur(lambda: solver.solve(nodes[0]))

        # 50 query
        random.seed(SEED)
        pairs = []
        while len(pairs) < 50:
            s = random.choice(nodes)
            t = random.choice(nodes)
            if s != t: pairs.append((s, t))

        def fn_50():
            for s, t in pairs:
                solver.shortest_path(s, t)

        t50 = ukur(fn_50)

        baris.append([
            n,
            f"{t1:.6f}",
            f"{t50:.6f}",
            f"{t50/50:.6f}",
            "O((V+E) log V)"
        ])

    tbl = cetak_tabel(kolom, baris)
    hasil_global.append(tbl)


# ═══════════════════════════════════════════════════════════════
# BENCHMARK 4 — BST
# ═══════════════════════════════════════════════════════════════

def bench_bst() -> None:
    cetak_header("BENCHMARK 4 – BST (Binary Search Tree dari nol)")
    hasil_global.append("\n" + "="*65)
    hasil_global.append("BENCHMARK 4 – BST")
    hasil_global.append("="*65)

    kolom = ["N node", "insert (s)", "search (s)", "inorder (s)", "delete (s)", "Big-O"]
    baris = []

    for n in UKURAN:
        random.seed(SEED)
        keys = buat_nama(n)

        # insert
        def fn_ins():
            b = IntersectionBST()
            for k in keys: b.insert(k)

        t_ins = ukur(fn_ins)

        # Siapkan BST terisi
        bst = IntersectionBST()
        for k in keys: bst.insert(k)

        # search semua key
        t_srch = ukur(lambda: [bst.search(k) for k in keys])

        # inorder
        t_inord = ukur(lambda: bst.inorder())

        # delete setengah key
        half = keys[:n//2]
        def fn_del():
            b2 = IntersectionBST()
            for k in keys: b2.insert(k)
            for k in half: b2.delete(k)

        t_del = ukur(fn_del)

        baris.append([
            n,
            f"{t_ins:.6f}",
            f"{t_srch:.6f}",
            f"{t_inord:.6f}",
            f"{t_del:.6f}",
            "ins/srch O(log n) avg | inorder O(n)"
        ])

    tbl = cetak_tabel(kolom, baris)
    hasil_global.append(tbl)


# ═══════════════════════════════════════════════════════════════
# BENCHMARK 5 — LINKED LIST
# ═══════════════════════════════════════════════════════════════

def bench_linked_list() -> None:
    cetak_header("BENCHMARK 5 – LINKED LIST (Singly, dari nol)")
    hasil_global.append("\n" + "="*65)
    hasil_global.append("BENCHMARK 5 – LINKED LIST")
    hasil_global.append("="*65)

    kolom = ["N elemen", "add_front (s)", "add_back (s)", "find (s)", "delete (s)", "Big-O"]
    baris = []

    for n in UKURAN:
        data = list(range(n))

        # add_front
        t_front = ukur(lambda: [LinkedList().add_front(x) for x in data])

        # add_back
        def fn_back():
            ll = LinkedList()
            for x in data: ll.add_back(x)

        t_back = ukur(fn_back)

        # find (worst case: cari elemen terakhir)
        ll_find = LinkedList()
        for x in data: ll_find.add_back(x)
        t_find = ukur(lambda: ll_find.find(data[-1]))

        # delete (semua elemen)
        def fn_del():
            ll2 = LinkedList()
            for x in data: ll2.add_back(x)
            for x in data: ll2.delete(x)

        t_del = ukur(fn_del)

        baris.append([
            n,
            f"{t_front:.6f}",
            f"{t_back:.6f}",
            f"{t_find:.6f}",
            f"{t_del:.6f}",
            "add_front O(1) | add_back O(1)* | find/del O(n)"
        ])

    tbl = cetak_tabel(kolom, baris)
    hasil_global.append(tbl)


# ═══════════════════════════════════════════════════════════════
# BENCHMARK 6 — STACK
# ═══════════════════════════════════════════════════════════════

def bench_stack() -> None:
    cetak_header("BENCHMARK 6 – STACK (LIFO berbasis Linked List)")
    hasil_global.append("\n" + "="*65)
    hasil_global.append("BENCHMARK 6 – STACK")
    hasil_global.append("="*65)

    kolom = ["N elemen", "push (s)", "pop (s)", "peek (s)", "Big-O"]
    baris = []

    for n in UKURAN:
        data = list(range(n))

        # push
        def fn_push():
            s = Stack()
            for x in data: s.push(x)

        t_push = ukur(fn_push)

        # pop
        def fn_pop():
            s = Stack()
            for x in data: s.push(x)
            while not s.is_empty(): s.pop()

        t_pop = ukur(fn_pop)

        # peek
        s_peek = Stack()
        for x in data: s_peek.push(x)
        t_peek = ukur(lambda: s_peek.peek())

        baris.append([
            n,
            f"{t_push:.6f}",
            f"{t_pop:.6f}",
            f"{t_peek:.6f}",
            "push O(1) | pop O(1) | peek O(1)"
        ])

    tbl = cetak_tabel(kolom, baris)
    hasil_global.append(tbl)


# ═══════════════════════════════════════════════════════════════
# BENCHMARK 7 — SORTING (3 Algoritma)
# ═══════════════════════════════════════════════════════════════

def bench_sorting() -> None:
    cetak_header("BENCHMARK 7 – SORTING (Bubble | Insertion | Selection)")
    hasil_global.append("\n" + "="*65)
    hasil_global.append("BENCHMARK 7 – SORTING")
    hasil_global.append("="*65)

    # ── 7a: Data Acak ─────────────────────────────
    log("\n  [7a] Data ACAK (worst/average case):")
    hasil_global.append("\n  [7a] Data ACAK (worst/average case):")
    kolom = ["N", "Bubble (s)", "Insertion (s)", "Selection (s)", "Tercepat"]
    baris = []

    for n in UKURAN:
        random.seed(SEED)
        pairs = [(f"P{i}", random.randint(0, 100)) for i in range(n)]

        def buat_ll():
            ll = CongestionLinkedList()
            for nm, ct in pairs: ll.append(nm, ct)
            return ll

        t_b = ukur(lambda: buat_ll().bubble_sort())
        t_i = ukur(lambda: buat_ll().insertion_sort())
        t_s = ukur(lambda: buat_ll().selection_sort())

        tercepat = min(
            [("Bubble", t_b), ("Insertion", t_i), ("Selection", t_s)],
            key=lambda x: x[1]
        )[0]

        baris.append([
            n,
            f"{t_b:.6f}",
            f"{t_i:.6f}",
            f"{t_s:.6f}",
            tercepat
        ])

    tbl = cetak_tabel(kolom, baris)
    hasil_global.append(tbl)

    # ── 7b: Data Hampir Terurut ───────────────────
    log("\n  [7b] Data HAMPIR TERURUT (best case Insertion Sort):")
    hasil_global.append("\n  [7b] Data HAMPIR TERURUT:")
    baris2 = []

    for n in UKURAN:
        # Data sudah hampir terurut descending (swap 2 elemen saja)
        pairs_sorted = [(f"P{i}", n - i) for i in range(n)]
        # Tukar 2 elemen secara acak
        random.seed(SEED)
        i1, i2 = random.sample(range(n), 2)
        pairs_sorted[i1], pairs_sorted[i2] = pairs_sorted[i2], pairs_sorted[i1]

        def buat_ll_sorted():
            ll = CongestionLinkedList()
            for nm, ct in pairs_sorted: ll.append(nm, ct)
            return ll

        t_b = ukur(lambda: buat_ll_sorted().bubble_sort())
        t_i = ukur(lambda: buat_ll_sorted().insertion_sort())
        t_s = ukur(lambda: buat_ll_sorted().selection_sort())

        tercepat = min(
            [("Bubble", t_b), ("Insertion", t_i), ("Selection", t_s)],
            key=lambda x: x[1]
        )[0]

        baris2.append([
            n,
            f"{t_b:.6f}",
            f"{t_i:.6f}",
            f"{t_s:.6f}",
            tercepat
        ])

    tbl2 = cetak_tabel(kolom, baris2)
    hasil_global.append(tbl2)

    # ── Big-O Summary ─────────────────────────────
    log("\n  Big-O Sorting:")
    log("  Bubble Sort    : O(n²) — stable, early exit jika sudah terurut")
    log("  Insertion Sort : O(n²) worst / O(n) best — adaptif untuk hampir terurut")
    log("  Selection Sort : O(n²) — minimal swap O(n), tidak adaptif")
    hasil_global.append("\n  Big-O: Bubble O(n²) | Insertion O(n²)/O(n)* | Selection O(n²)")


# ═══════════════════════════════════════════════════════════════
# RINGKASAN PERBANDINGAN TEORITIS vs EKSPERIMENTAL
# ═══════════════════════════════════════════════════════════════

def cetak_ringkasan() -> None:
    cetak_header("RINGKASAN – Teoritis vs Eksperimental")
    hasil_global.append("\n" + "="*65)
    hasil_global.append("RINGKASAN TEORITIS vs EKSPERIMENTAL")
    hasil_global.append("="*65)

    data = [
        ["Graph add_edge",    "O(1)",          "Konstan, tidak naik seiring N"],
        ["Graph DFS",         "O(V + E)",       "Naik linear seiring V+E"],
        ["PQ enqueue",        "O(log n)",       "Naik logaritmik"],
        ["PQ dequeue",        "O(log n)",       "Naik logaritmik"],
        ["Dijkstra 1 query",  "O((V+E) log V)", "Naik, tapi lambat (log)"],
        ["BST insert/search", "O(log n) avg",   "Logaritmik, tergantung keseimbangan"],
        ["BST inorder",       "O(n)",           "Naik linear"],
        ["LL add_front",      "O(1)",           "Konstan"],
        ["LL find",           "O(n)",           "Naik linear (scan)"],
        ["Stack push/pop",    "O(1)",           "Konstan selalu"],
        ["Bubble Sort",       "O(n²)",          "Kuadratik, naik tajam N=100"],
        ["Insertion Sort",    "O(n²)/O(n)*",    "Adaptif jika hampir terurut"],
        ["Selection Sort",    "O(n²)",          "Kuadratik, swap minimal"],
    ]

    kolom = ["Operasi", "Big-O Teoritis", "Observasi Eksperimen"]
    tbl = cetak_tabel(kolom, data)
    hasil_global.append(tbl)


# ═══════════════════════════════════════════════════════════════
# SIMPAN HASIL KE FILE
# ═══════════════════════════════════════════════════════════════

def simpan_hasil() -> None:
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("HASIL BENCHMARK – Smart Traffic Simulation\n")
        f.write("ELT60213 Algoritma dan Struktur Data | Topik 7\n")
        f.write("Seed=17 | N=10,25,100 | Rata-rata 5 pengukuran\n")
        f.write("="*65 + "\n\n")
        for line in hasil_global:
            f.write(line + "\n")
    print(f"\n  ✓ Hasil disimpan ke: {OUTPUT_FILE}")


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    print("\n" + "╔" + "═"*63 + "╗")
    print("║  BENCHMARK – Smart Traffic Simulation & Signal Optimization  ║")
    print("║  ELT60213 Algoritma dan Struktur Data | Topik 7              ║")
    print("║  Dataset: N = 10, 25, 100  |  Seed = 17  |  Ulang = 5x      ║")
    print("╚" + "═"*63 + "╝")

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", type=str, default=None,
                        help="Jalankan benchmark tertentu saja "
                             "(graph/queue/dijkstra/bst/linkedlist/stack/sorting)")
    args = parser.parse_args()

    t_total = time.perf_counter()

    benches = {
        "graph"      : bench_graph,
        "queue"      : bench_priority_queue,
        "dijkstra"   : bench_dijkstra,
        "bst"        : bench_bst,
        "linkedlist" : bench_linked_list,
        "stack"      : bench_stack,
        "sorting"    : bench_sorting,
    }

    if args.only:
        key = args.only.lower()
        if key in benches:
            benches[key]()
        else:
            print(f"  ✗ Pilihan tidak valid. Opsi: {list(benches.keys())}")
            return
    else:
        # Jalankan semua
        for fn in benches.values():
            fn()
        cetak_ringkasan()

    elapsed = time.perf_counter() - t_total
    print(f"\n{'═'*65}")
    print(f"  ✓ Semua benchmark selesai dalam {elapsed:.3f} detik")
    print(f"{'═'*65}")

    simpan_hasil()


if __name__ == "__main__":
    main()