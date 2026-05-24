"""
=============================================================
TOPIK 7 - Smart Traffic Simulation & Signal Optimization
ELT60213 Algoritma dan Struktur Data | TA 2025/2026
=============================================================
MODUL 1: Graph Jaringan Jalan
- Graf berbobot (jarak meter) menggunakan adjacency list berbasis Linked List
- Mendukung: tambah_persimpangan, tambah_jalan (dua arah/satu arah)
- tetangga(u), degree(u)
- DFS untuk deteksi persimpangan terisolasi
- Big-O: add_edge O(1), neighbors O(deg)
=============================================================
"""

import numpy as np
import random

# Seed tetap sesuai spesifikasi — JANGAN diubah
np.random.seed(17)
random.seed(17)


# ──────────────────────────────────────────────
# NODE untuk Linked List (adjacency list)
# ──────────────────────────────────────────────
class EdgeNode:
    """
    Simpul dalam linked list adjacency list.
    Menyimpan: tujuan, bobot (jarak meter), pointer next.
    """
    def __init__(self, tujuan: str, bobot: float):
        self.tujuan = tujuan        # nama persimpangan tujuan
        self.bobot  = bobot         # jarak dalam meter
        self.next   = None          # pointer ke edge berikutnya


# ──────────────────────────────────────────────
# ADJACENCY LIST berbasis Linked List
# ──────────────────────────────────────────────
class AdjList:
    """
    Adjacency list satu persimpangan (linked list sederhana).
    Head → EdgeNode → EdgeNode → ... → None
    """
    def __init__(self):
        self.head  = None           # kepala linked list
        self.ukuran = 0             # jumlah edge

    def tambah_edge(self, tujuan: str, bobot: float):
        """
        Tambah edge ke depan linked list.
        Big-O: O(1)
        """
        node       = EdgeNode(tujuan, bobot)
        node.next  = self.head
        self.head  = node
        self.ukuran += 1

    def hapus_edge(self, tujuan: str) -> bool:
        """
        Hapus edge menuju 'tujuan'.
        Big-O: O(deg)
        """
        prev, curr = None, self.head
        while curr:
            if curr.tujuan == tujuan:
                if prev:
                    prev.next = curr.next
                else:
                    self.head = curr.next
                self.ukuran -= 1
                return True
            prev, curr = curr, curr.next
        return False

    def cari_edge(self, tujuan: str):
        """
        Cari edge menuju 'tujuan'. Return EdgeNode atau None.
        Big-O: O(deg)
        """
        curr = self.head
        while curr:
            if curr.tujuan == tujuan:
                return curr
            curr = curr.next
        return None

    def daftar_tetangga(self) -> list:
        """
        Kembalikan list (tujuan, bobot) semua tetangga.
        Big-O: O(deg)
        """
        hasil, curr = [], self.head
        while curr:
            hasil.append((curr.tujuan, curr.bobot))
            curr = curr.next
        return hasil


# ──────────────────────────────────────────────
# GRAPH JARINGAN JALAN
# ──────────────────────────────────────────────
class TrafficGraph:
    """
    Graf berbobot menggunakan dictionary of AdjList.
    Mendukung graf berarah dan tidak berarah.

    Atribut:
        adj   : dict[str, AdjList] — adjacency list tiap node
        nodes : dict[str, dict]   — metadata persimpangan
    """

    def __init__(self):
        self.adj   = {}             # {nama_persimpangan: AdjList}
        self._nodes = {}             # {nama_persimpangan: {lat, lon, ...}}
        self._jumlah_edge = 0

    # ── OPERASI PERSIMPANGAN ──────────────────

    def tambah_persimpangan(self, nama: str, **meta) -> bool:
        """
        Tambah persimpangan (node) baru ke graf.
        Big-O: O(1)
        Return False jika sudah ada.
        """
        if nama in self.adj:
            return False
        self.adj[nama]   = AdjList()
        self._nodes[nama] = meta
        return True

    def hapus_persimpangan(self, nama: str) -> bool:
        """
        Hapus persimpangan beserta semua edge yang terhubung.
        Big-O: O(V + E)
        """
        if nama not in self.adj:
            return False
        # Hapus semua edge masuk dari node lain
        for src in self.adj:
            if src != nama:
                self.adj[src].hapus_edge(nama)
        del self.adj[nama]
        del self._nodes[nama]
        return True

    def ada_persimpangan(self, nama: str) -> bool:
        """Big-O: O(1)"""
        return nama in self.adj

    # ── OPERASI JALAN (EDGE) ─────────────────

    def tambah_jalan(self, asal: str, tujuan: str, bobot: float,
                     dua_arah: bool = True) -> bool:
        """
        Tambah jalan antara dua persimpangan.
        Big-O: O(1)
        """
        if asal not in self.adj or tujuan not in self.adj:
            return False
        if bobot <= 0:
            return False
        self.adj[asal].tambah_edge(tujuan, bobot)
        self._jumlah_edge += 1
        if dua_arah:
            self.adj[tujuan].tambah_edge(asal, bobot)
            self._jumlah_edge += 1
        return True

    def hapus_jalan(self, asal: str, tujuan: str,
                    dua_arah: bool = True) -> bool:
        """
        Hapus jalan antara dua persimpangan.
        Big-O: O(deg)
        """
        if asal not in self.adj or tujuan not in self.adj:
            return False
        ok = self.adj[asal].hapus_edge(tujuan)
        if ok:
            self._jumlah_edge -= 1
        if dua_arah:
            ok2 = self.adj[tujuan].hapus_edge(asal)
            if ok2:
                self._jumlah_edge -= 1
        return ok

    def bobot_jalan(self, asal: str, tujuan: str):
        """
        Kembalikan bobot jalan asal→tujuan.
        Return None jika tidak ada.
        Big-O: O(deg)
        """
        if asal not in self.adj:
            return None
        edge = self.adj[asal].cari_edge(tujuan)
        return edge.bobot if edge else None

    # ── QUERY TETANGGA & DEGREE ──────────────

    def tetangga(self, nama: str) -> list:
        """
        Kembalikan list (tujuan, bobot) tetangga persimpangan.
        Big-O: O(deg)
        """
        if nama not in self.adj:
            return []
        return self.adj[nama].daftar_tetangga()

    def degree(self, nama: str) -> int:
        """
        Kembalikan jumlah edge keluar dari persimpangan.
        Big-O: O(1)
        """
        if nama not in self.adj:
            return 0
        return self.adj[nama].ukuran

    # ── STATISTIK GRAF ───────────────────────

    @property
    def jumlah_persimpangan(self) -> int:
        return len(self.adj)

    @property
    def jumlah_jalan(self) -> int:
        return self._jumlah_edge

    @property
    def nodes(self):
        return list(self.adj.keys())

    # ── DFS — DETEKSI PERSIMPANGAN TERISOLASI ─

    def _dfs(self, mulai: str, dikunjungi: set):
        """
        DFS iteratif menggunakan stack manual (list Python).
        Big-O: O(V + E)
        """
        stack = [mulai]
        while stack:
            v = stack.pop()
            if v in dikunjungi:
                continue
            dikunjungi.add(v)
            for tetangga, _ in self.tetangga(v):
                if tetangga not in dikunjungi:
                    stack.append(tetangga)

    def deteksi_terisolasi(self) -> list:
        """
        Deteksi persimpangan yang tidak terhubung ke komponen utama.
        - Jalankan DFS dari persimpangan pertama
        - Persimpangan yang tidak dikunjungi = terisolasi
        Big-O: O(V + E)
        Return: list nama persimpangan terisolasi
        """
        if not self.adj:
            return []
        dikunjungi = set()
        mulai = next(iter(self.adj))
        self._dfs(mulai, dikunjungi)
        terisolasi = [v for v in self.adj if v not in dikunjungi]
        return terisolasi

    def komponen_terhubung(self) -> list:
        """
        Temukan semua komponen terhubung dalam graf.
        Big-O: O(V + E)
        Return: list of list (setiap sublist = satu komponen)
        """
        dikunjungi = set()
        komponen   = []
        for v in self.adj:
            if v not in dikunjungi:
                komp = set()
                self._dfs(v, komp)
                dikunjungi |= komp
                komponen.append(sorted(komp))
        return komponen

    def bfs(self, mulai: str) -> list:
        """
        BFS dari persimpangan 'mulai'.
        Menggunakan circular queue manual sederhana.
        Big-O: O(V + E)
        Return: list node urutan BFS
        """
        if mulai not in self.adj:
            return []
        dikunjungi = set([mulai])
        queue      = [mulai]                 # manual queue (array)
        head_idx   = 0
        urutan     = []
        while head_idx < len(queue):
            v = queue[head_idx]
            head_idx += 1
            urutan.append(v)
            for tetangga, _ in self.tetangga(v):
                if tetangga not in dikunjungi:
                    dikunjungi.add(tetangga)
                    queue.append(tetangga)
        return urutan

    # ── TAMPILAN ─────────────────────────────

    def tampilkan_graf(self, maks_tampil: int = 10):
        """Tampilkan adjacency list (maks_tampil node pertama)."""
        print("\n" + "="*60)
        print("  GRAPH JARINGAN JALAN — ADJACENCY LIST")
        print(f"  Persimpangan: {self.jumlah_persimpangan} | "
              f"Jalan (edge): {self.jumlah_jalan}")
        print("="*60)
        for i, (nama, adj) in enumerate(self.adj.items()):
            if i >= maks_tampil:
                print(f"  ... (dan {self.jumlah_persimpangan - maks_tampil} lainnya)")
                break
            tetangga_str = " → ".join(
                f"{t}({b:.0f}m)" for t, b in adj.daftar_tetangga()
            )
            print(f"  [{nama}]  deg={adj.ukuran}  |  {tetangga_str or '(kosong)'}")
        print("="*60)

    def info_persimpangan(self, nama: str):
        """Tampilkan detail satu persimpangan."""
        if nama not in self.adj:
            print(f"  ✗ Persimpangan '{nama}' tidak ditemukan.")
            return
        print(f"\n  Persimpangan : {nama}")
        print(f"  Degree       : {self.degree(nama)}")
        print(f"  Metadata     : {self._nodes.get(nama, {})}")
        print(f"  Tetangga     :")
        for t, b in self.tetangga(nama):
            print(f"    → {t}  ({b:.0f} m)")


# ──────────────────────────────────────────────
# FACTORY — Bangun Graf 25 Persimpangan
# ──────────────────────────────────────────────

NAMA_PERSIMPANGAN = [
    "Malioboro",    "Tugu",         "Kraton",       "Prawirotaman",
    "Kotagede",     "Kaliurang",    "Sleman",       "Godean",
    "Bantul",       "Wonosari",     "Wates",        "Prambanan",
    "Kalasan",      "Depok",        "Seturan",      "Condongcatur",
    "Maguwoharjo",  "Ngaglik",      "Gamping",      "Sewon",
    "Kasihan",      "Pleret",       "Piyungan",     "Jetis",
    "Gondokusuman"
]


def build_traffic_graph(seed=17) -> TrafficGraph:
    """
    Membangun graf kota Yogyakarta simulatif dengan:
    - 25 persimpangan (node)
    - ~40 edge berbobot acak 200–2000 meter
    - Seed = 17 (np.random.seed(17)) agar topologi TETAP

    Big-O keseluruhan: O(V + E)
    """
    random.seed(seed)
    np.random.seed(seed)
    g = TrafficGraph()

    # Tambah semua persimpangan
    for nama in NAMA_PERSIMPANGAN:
        g.tambah_persimpangan(nama)

    # Bangun spanning tree dulu (agar semua terhubung)
    nodes = NAMA_PERSIMPANGAN.copy()
    rng_py = random.Random(17)
    rng_py.shuffle(nodes)

    for i in range(1, len(nodes)):
        bobot = float(np.random.randint(300, 1500))
        g.tambah_jalan(nodes[i-1], nodes[i], bobot, dua_arah=True)

    # Tambah edge tambahan hingga ±40 total undirected edges
    target_edge_undir = 40
    percobaan = 0
    while (g.jumlah_jalan // 2) < target_edge_undir and percobaan < 500:
        percobaan += 1
        u = rng_py.choice(NAMA_PERSIMPANGAN)
        v = rng_py.choice(NAMA_PERSIMPANGAN)
        if u == v:
            continue
        if g.adj[u].cari_edge(v) is not None:   # sudah ada
            continue
        bobot = float(np.random.randint(200, 2000))
        g.tambah_jalan(u, v, bobot, dua_arah=True)

    return g


# ──────────────────────────────────────────────
# DEMO / TEST MANDIRI
# ──────────────────────────────────────────────

def demo_modul_1():
    print("\n" + "█"*60)
    print("  MODUL 1 — Graph Jaringan Jalan")
    print("  ELT60213 Algoritma dan Struktur Data | Topik 7")
    print("█"*60)

    g = build_traffic_graph()
    g.tampilkan_graf(maks_tampil=8)

    # Info satu persimpangan
    g.info_persimpangan("Malioboro")

    # Deteksi terisolasi
    terisolasi = g.deteksi_terisolasi()
    print(f"\n  Persimpangan terisolasi : "
          f"{terisolasi if terisolasi else 'Tidak ada (semua terhubung)'}")

    # Komponen terhubung
    komp = g.komponen_terhubung()
    print(f"  Jumlah komponen terhubung: {len(komp)}")

    # BFS dari Malioboro
    bfs_hasil = g.bfs("Malioboro")
    print(f"\n  BFS dari Malioboro ({len(bfs_hasil)} node dikunjungi):")
    print("  " + " → ".join(bfs_hasil[:10]) + " ...")

    # Ringkasan Big-O
    print("\n  ╔══════════════════════════════════════════╗")
    print("  ║           RINGKASAN BIG-O MODUL 1        ║")
    print("  ╠══════════════════════════════════════════╣")
    print("  ║  tambah_persimpangan     : O(1)           ║")
    print("  ║  tambah_jalan (add_edge) : O(1)           ║")
    print("  ║  tetangga (neighbors)    : O(deg)         ║")
    print("  ║  degree                  : O(1)           ║")
    print("  ║  DFS deteksi terisolasi  : O(V + E)       ║")
    print("  ║  BFS traversal           : O(V + E)       ║")
    print("  ║  hapus_persimpangan      : O(V + E)       ║")
    print("  ╚══════════════════════════════════════════╝")

    return g


if __name__ == "__main__":
    demo_modul_1()