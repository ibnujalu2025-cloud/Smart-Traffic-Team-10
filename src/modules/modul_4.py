"""
=============================================================
TOPIK 7 - Smart Traffic Simulation & Signal Optimization
ELT60213 Algoritma dan Struktur Data | TA 2025/2026
=============================================================
MODUL 4: BST Indeks Persimpangan
- BST dengan kunci = nama persimpangan (string)
- Mendukung: insert, search, inorder (daftar terurut)
- Berguna untuk lookup cepat persimpangan dari nama
- Big-O: O(log V) rata-rata untuk insert/search
         O(V) untuk inorder traversal
=============================================================
"""

import time


# ──────────────────────────────────────────────
# NODE BST
# ──────────────────────────────────────────────
class NodeBST:
    """Simpul Binary Search Tree untuk satu persimpangan."""

    def __init__(self, kunci: str, data: dict = None):
        self.kunci  = kunci             # nama persimpangan (string)
        self.data   = data or {}        # metadata tambahan
        self.kiri   = None              # anak kiri (kunci < self.kunci)
        self.kanan  = None              # anak kanan (kunci > self.kunci)
        self.tinggi = 1                 # untuk info keseimbangan


# ──────────────────────────────────────────────
# BST INDEKS PERSIMPANGAN
# ──────────────────────────────────────────────
class BSTIndeksPersimpangan:
    """
    Binary Search Tree dengan kunci nama persimpangan (string).
    Perbandingan string: leksikografis (A < B < ... < Z).

    Operasi utama:
      insert   — O(log V) rata-rata, O(V) terburuk
      search   — O(log V) rata-rata, O(V) terburuk
      delete   — O(log V) rata-rata, O(V) terburuk
      inorder  — O(V) selalu
      min/max  — O(log V) rata-rata
    """

    def __init__(self):
        self.akar    = None
        self.ukuran  = 0        # jumlah node

    # ── HEIGHT HELPER ────────────────────────

    def _tinggi(self, node) -> int:
        return node.tinggi if node else 0

    def _perbarui_tinggi(self, node):
        if node:
            node.tinggi = 1 + max(
                self._tinggi(node.kiri),
                self._tinggi(node.kanan)
            )

    # ── INSERT ────────────────────────────────

    def insert(self, kunci: str, data: dict = None) -> bool:
        """
        Masukkan persimpangan baru ke BST.
        Big-O: O(log V) rata-rata, O(V) terburuk (tree tidak seimbang)
        Return: True jika berhasil, False jika kunci sudah ada
        """
        if self.akar is None:
            self.akar  = NodeBST(kunci, data)
            self.ukuran += 1
            return True
        berhasil = self._insert_rekursif(self.akar, kunci, data)
        if berhasil:
            self.ukuran += 1
        return berhasil

    def _insert_rekursif(self, node: NodeBST,
                         kunci: str, data: dict) -> bool:
        if kunci < node.kunci:
            if node.kiri is None:
                node.kiri = NodeBST(kunci, data)
                self._perbarui_tinggi(node)
                return True
            hasil = self._insert_rekursif(node.kiri, kunci, data)
            self._perbarui_tinggi(node)
            return hasil
        elif kunci > node.kunci:
            if node.kanan is None:
                node.kanan = NodeBST(kunci, data)
                self._perbarui_tinggi(node)
                return True
            hasil = self._insert_rekursif(node.kanan, kunci, data)
            self._perbarui_tinggi(node)
            return hasil
        else:
            # Kunci sudah ada — update data
            node.data = data or node.data
            return False

    # ── SEARCH ────────────────────────────────

    def search(self, kunci: str) -> NodeBST:
        """
        Cari persimpangan berdasarkan nama (kunci).
        Big-O: O(log V) rata-rata, O(V) terburuk
        Return: NodeBST atau None
        """
        return self._search_rekursif(self.akar, kunci)

    def _search_rekursif(self, node: NodeBST, kunci: str) -> NodeBST:
        if node is None:
            return None
        if kunci == node.kunci:
            return node
        if kunci < node.kunci:
            return self._search_rekursif(node.kiri, kunci)
        return self._search_rekursif(node.kanan, kunci)

    def ada(self, kunci: str) -> bool:
        """Big-O: O(log V) rata-rata"""
        return self.search(kunci) is not None

    # ── DELETE ────────────────────────────────

    def hapus(self, kunci: str) -> bool:
        """
        Hapus persimpangan dari BST.
        Big-O: O(log V) rata-rata
        """
        if not self.ada(kunci):
            return False
        self.akar    = self._hapus_rekursif(self.akar, kunci)
        self.ukuran -= 1
        return True

    def _hapus_rekursif(self, node: NodeBST, kunci: str) -> NodeBST:
        if node is None:
            return None
        if kunci < node.kunci:
            node.kiri = self._hapus_rekursif(node.kiri, kunci)
        elif kunci > node.kunci:
            node.kanan = self._hapus_rekursif(node.kanan, kunci)
        else:
            # Kasus 1: daun
            if node.kiri is None and node.kanan is None:
                return None
            # Kasus 2: satu anak
            if node.kiri is None:
                return node.kanan
            if node.kanan is None:
                return node.kiri
            # Kasus 3: dua anak — ganti dengan successor (inorder successor)
            successor  = self._min_node(node.kanan)
            node.kunci = successor.kunci
            node.data  = successor.data
            node.kanan = self._hapus_rekursif(node.kanan, successor.kunci)
        self._perbarui_tinggi(node)
        return node

    # ── MIN / MAX ─────────────────────────────

    def _min_node(self, node: NodeBST) -> NodeBST:
        """Kembalikan node dengan kunci terkecil di subtree. O(log V)"""
        curr = node
        while curr.kiri:
            curr = curr.kiri
        return curr

    def minimum(self) -> NodeBST:
        """Persimpangan dengan nama terkecil (abjad). O(log V)"""
        if self.akar is None:
            return None
        return self._min_node(self.akar)

    def maksimum(self) -> NodeBST:
        """Persimpangan dengan nama terbesar (abjad). O(log V)"""
        if self.akar is None:
            return None
        curr = self.akar
        while curr.kanan:
            curr = curr.kanan
        return curr

    # ── INORDER TRAVERSAL ─────────────────────

    def inorder(self) -> list:
        """
        Kembalikan list semua persimpangan terurut abjad.
        Big-O: O(V)
        """
        hasil = []
        self._inorder_rekursif(self.akar, hasil)
        return hasil

    def _inorder_rekursif(self, node: NodeBST, hasil: list):
        if node is None:
            return
        self._inorder_rekursif(node.kiri, hasil)
        hasil.append((node.kunci, node.data))
        self._inorder_rekursif(node.kanan, hasil)

    def preorder(self) -> list:
        """Preorder traversal (akar → kiri → kanan). O(V)"""
        hasil = []
        self._preorder_rekursif(self.akar, hasil)
        return hasil

    def _preorder_rekursif(self, node: NodeBST, hasil: list):
        if node is None:
            return
        hasil.append(node.kunci)
        self._preorder_rekursif(node.kiri, hasil)
        self._preorder_rekursif(node.kanan, hasil)

    def postorder(self) -> list:
        """Postorder traversal (kiri → kanan → akar). O(V)"""
        hasil = []
        self._postorder_rekursif(self.akar, hasil)
        return hasil

    def _postorder_rekursif(self, node: NodeBST, hasil: list):
        if node is None:
            return
        self._postorder_rekursif(node.kiri, hasil)
        self._postorder_rekursif(node.kanan, hasil)
        hasil.append(node.kunci)

    # ── STATISTIK ─────────────────────────────

    def tinggi_pohon(self) -> int:
        """
        Hitung tinggi pohon BST.
        Big-O: O(V)
        """
        return self._hitung_tinggi(self.akar)

    def _hitung_tinggi(self, node: NodeBST) -> int:
        if node is None:
            return 0
        return 1 + max(
            self._hitung_tinggi(node.kiri),
            self._hitung_tinggi(node.kanan)
        )

    def faktor_keseimbangan(self) -> float:
        """
        Ukuran seberapa seimbang pohon.
        0.0 = sempurna seimbang, mendekati 1.0 = tidak seimbang.
        Big-O: O(V)
        """
        if self.ukuran == 0:
            return 0.0
        import math
        h_ideal = math.log2(self.ukuran + 1)
        h_aktual = self.tinggi_pohon()
        return (h_aktual - h_ideal) / max(h_ideal, 1)

    def cari_awalan(self, awalan: str) -> list:
        """
        Cari semua persimpangan yang namanya diawali 'awalan'.
        Big-O: O(V) terburuk
        """
        awalan = awalan.lower()
        return [
            (k, d) for k, d in self.inorder()
            if k.lower().startswith(awalan)
        ]

    # ── VISUALISASI POHON ─────────────────────

    def tampilkan_pohon(self, maks_tinggi: int = 4):
        """
        Tampilkan representasi pohon BST secara tekstual (level order).
        Big-O: O(V)
        """
        if self.akar is None:
            print("  (BST kosong)")
            return

        print(f"\n  BST Indeks Persimpangan")
        print(f"  Ukuran: {self.ukuran} | Tinggi: {self.tinggi_pohon()}")
        print(f"  Faktor ketidakseimbangan: "
              f"{self.faktor_keseimbangan():.3f}")
        print()

        # Level-order BFS
        antrian = [(self.akar, 0)]
        level_saat_ini = -1
        head = 0
        while head < len(antrian):
            node, level = antrian[head]
            head += 1
            if level > maks_tinggi:
                break
            if level != level_saat_ini:
                if level_saat_ini >= 0:
                    print()
                print(f"  L{level}: ", end="")
                level_saat_ini = level
            print(f"[{node.kunci}]", end=" ")
            if node.kiri:
                antrian.append((node.kiri, level + 1))
            if node.kanan:
                antrian.append((node.kanan, level + 1))
        print()

    def tampilkan_inorder(self, maks: int = 25):
        """Tampilkan daftar persimpangan terurut abjad."""
        print(f"\n  ── Daftar Persimpangan (Inorder / Terurut Abjad) ──")
        terurut = self.inorder()
        for i, (kunci, _) in enumerate(terurut[:maks], 1):
            print(f"  {i:2d}. {kunci}")
        if len(terurut) > maks:
            print(f"  ... dan {len(terurut) - maks} lainnya")


# ──────────────────────────────────────────────
# FACTORY — Bangun BST dari Graf
# ──────────────────────────────────────────────

def bangun_bst_dari_graf(graf) -> BSTIndeksPersimpangan:
    """
    Bangun BST indeks dari semua persimpangan dalam graf.
    Urutan insert ACAK agar BST tidak menjadi linear.
    Big-O: O(V log V) rata-rata
    """
    import random
    bst   = BSTIndeksPersimpangan()
    nodes = graf.semua_persimpangan()
    random.seed(17)
    random.shuffle(nodes)           # acak agar pohon seimbang

    for nama in nodes:
        metadata = graf.nodes.get(nama, {})
        metadata["degree"] = graf.degree(nama)
        bst.insert(nama, metadata)

    return bst


# ──────────────────────────────────────────────
# BENCHMARK
# ──────────────────────────────────────────────

def benchmark_bst(bst: BSTIndeksPersimpangan,
                  daftar_cari: list) -> dict:
    """
    Benchmark operasi BST untuk analisis Big-O.
    Big-O: O(n * log V) untuk n operasi search
    """
    # Benchmark insert
    bst_baru = BSTIndeksPersimpangan()
    t0 = time.perf_counter()
    for k in daftar_cari:
        bst_baru.insert(k)
    t1 = time.perf_counter()
    t_insert = (t1 - t0) * 1000

    # Benchmark search
    t0 = time.perf_counter()
    for k in daftar_cari:
        bst.search(k)
    t1 = time.perf_counter()
    t_search = (t1 - t0) * 1000

    # Benchmark inorder
    t0 = time.perf_counter()
    bst.inorder()
    t1 = time.perf_counter()
    t_inorder = (t1 - t0) * 1000

    return {
        "n"        : len(daftar_cari),
        "t_insert" : t_insert,
        "t_search" : t_search,
        "t_inorder": t_inorder,
        "tinggi"   : bst.tinggi_pohon(),
    }


# ──────────────────────────────────────────────
# DEMO / TEST MANDIRI
# ──────────────────────────────────────────────

def demo_modul_4():
    from modul_1 import bangun_graf_kota, NAMA_PERSIMPANGAN

    print("\n" + "█"*60)
    print("  MODUL 4 — BST Indeks Persimpangan")
    print("  ELT60213 Algoritma dan Struktur Data | Topik 7")
    print("█"*60)

    g   = bangun_graf_kota()
    bst = bangun_bst_dari_graf(g)

    bst.tampilkan_pohon(maks_tinggi=3)
    bst.tampilkan_inorder()

    # Search demo
    uji_cari = ["Malioboro", "Prambanan", "XYZ", "Bantul"]
    print("\n  [>] Demo Search:")
    for nama in uji_cari:
        node = bst.search(nama)
        if node:
            print(f"  [✓] '{nama}' ditemukan — degree={node.data.get('degree', '?')}")
        else:
            print(f"  [✗] '{nama}' tidak ditemukan")

    # Cari awalan
    print("\n  [>] Cari persimpangan berawalan 'Ko':")
    hasil = bst.cari_awalan("Ko")
    for k, _ in hasil:
        print(f"  → {k}")

    # Min / Max
    print(f"\n  [i] Persimpangan pertama (abjad): {bst.minimum().kunci}")
    print(f"  [i] Persimpangan terakhir (abjad): {bst.maksimum().kunci}")

    # Hapus satu node
    print("\n  [>] Hapus 'Sleman' dari BST ...")
    bst.hapus("Sleman")
    print(f"  [i] Ukuran BST setelah hapus: {bst.ukuran}")
    print(f"  [i] 'Sleman' masih ada? {bst.ada('Sleman')}")

    # Benchmark
    print("\n  [>] Benchmark BST:")
    b = benchmark_bst(bst, NAMA_PERSIMPANGAN)
    print(f"  N={b['n']} | Tinggi={b['tinggi']}")
    print(f"  Insert : {b['t_insert']:.4f} ms")
    print(f"  Search : {b['t_search']:.4f} ms")
    print(f"  Inorder: {b['t_inorder']:.4f} ms")

    # Preorder
    print(f"\n  [>] Preorder (5 pertama): "
          f"{bst.preorder()[:5]}")

    print("\n  ╔══════════════════════════════════════════╗")
    print("  ║         RINGKASAN BIG-O MODUL 4          ║")
    print("  ╠══════════════════════════════════════════╣")
    print("  ║  insert        : O(log V) rata-rata     ║")
    print("  ║  search        : O(log V) rata-rata     ║")
    print("  ║  delete        : O(log V) rata-rata     ║")
    print("  ║  inorder       : O(V)                   ║")
    print("  ║  preorder      : O(V)                   ║")
    print("  ║  postorder     : O(V)                   ║")
    print("  ║  min/max       : O(log V) rata-rata     ║")
    print("  ║  tinggi_pohon  : O(V)                   ║")
    print("  ╚══════════════════════════════════════════╝")

    return bst


if __name__ == "__main__":
    demo_modul_4()