"""
=============================================================
TOPIK 7 - Smart Traffic Simulation & Signal Optimization
ELT60213 Algoritma dan Struktur Data | TA 2025/2026
=============================================================
MODUL 5: Sorting Laporan Kemacetan
- Urutkan persimpangan berdasarkan jumlah kendaraan tertunda
- Implementasi: Selection Sort dan Insertion Sort pada Linked List
- Bandingkan runtime untuk N = 10, 25, 100 persimpangan simulatif
- Identifikasi bottleneck network
- Big-O: O(n²) untuk kedua algoritma
=============================================================
"""

import time
import random
import numpy as np

random.seed(17)
np.random.seed(17)


# ──────────────────────────────────────────────
# NODE LAPORAN
# ──────────────────────────────────────────────
class NodeLaporan:
    """
    Simpul dalam linked list laporan kemacetan.
    Kunci sorting: jumlah_kendaraan (desc) = paling macet duluan
    """
    def __init__(self, nama: str, jumlah_kendaraan: int,
                 jenis_terbanyak: str = "", rata_tunggu: float = 0.0):
        self.nama             = nama
        self.jumlah_kendaraan = jumlah_kendaraan    # kunci sorting
        self.jenis_terbanyak  = jenis_terbanyak
        self.rata_tunggu      = rata_tunggu         # detik
        self.next             = None

    def __str__(self):
        return (f"{self.nama:<20} | {self.jumlah_kendaraan:>4} kendaraan "
                f"| {self.jenis_terbanyak:<8} | tunggu {self.rata_tunggu:.1f}s")


# ──────────────────────────────────────────────
# LINKED LIST LAPORAN
# ──────────────────────────────────────────────
class LinkedListLaporan:
    """
    Linked list untuk menyimpan laporan kemacetan.
    Mendukung dua algoritma sorting in-place.
    """

    def __init__(self):
        self.head   = None
        self.ukuran = 0

    def tambah(self, nama: str, jumlah_kendaraan: int,
               jenis_terbanyak: str = "", rata_tunggu: float = 0.0):
        """
        Tambah laporan di akhir linked list.
        Big-O: O(n) — traversal ke akhir
        """
        node = NodeLaporan(nama, jumlah_kendaraan,
                           jenis_terbanyak, rata_tunggu)
        if self.head is None:
            self.head = node
        else:
            curr = self.head
            while curr.next:
                curr = curr.next
            curr.next = node
        self.ukuran += 1

    def tambah_depan(self, nama: str, jumlah_kendaraan: int,
                     jenis_terbanyak: str = "", rata_tunggu: float = 0.0):
        """Tambah di depan. Big-O: O(1)"""
        node      = NodeLaporan(nama, jumlah_kendaraan,
                                jenis_terbanyak, rata_tunggu)
        node.next = self.head
        self.head = node
        self.ukuran += 1

    def ke_list(self) -> list:
        """Konversi ke list Python. Big-O: O(n)"""
        hasil, curr = [], self.head
        while curr:
            hasil.append(curr)
            curr = curr.next
        return hasil

    def salin(self) -> 'LinkedListLaporan':
        """Buat salinan linked list. Big-O: O(n)"""
        baru = LinkedListLaporan()
        curr = self.head
        while curr:
            baru.tambah(curr.nama, curr.jumlah_kendaraan,
                        curr.jenis_terbanyak, curr.rata_tunggu)
            curr = curr.next
        return baru

    def tampilkan(self, maks: int = 10, judul: str = "Laporan Kemacetan"):
        """Tampilkan linked list. Big-O: O(n)"""
        print(f"\n  ── {judul} ({self.ukuran} persimpangan) ──")
        print(f"  {'No':<4} {'Nama':<20} {'Kendaraan':>10} "
              f"{'Terbanyak':<10} {'Tunggu':>8}")
        print("  " + "─"*58)
        curr, i = self.head, 1
        while curr and i <= maks:
            bar = "█" * min(curr.jumlah_kendaraan // 2, 15)
            print(f"  {i:<4} {curr.nama:<20} {curr.jumlah_kendaraan:>10} "
                  f"{curr.jenis_terbanyak:<10} {curr.rata_tunggu:>7.1f}s")
            curr = curr.next
            i   += 1
        if self.ukuran > maks:
            print(f"  ... dan {self.ukuran - maks} lainnya")

    # ── SELECTION SORT ────────────────────────

    def selection_sort_desc(self) -> int:
        """
        Selection Sort pada linked list — urutan MENURUN (macet → tidak macet).
        Swap data (bukan pointer) untuk kesederhanaan.
        Big-O: O(n²) — n iterasi luar × n iterasi dalam

        Return: jumlah swap yang dilakukan
        """
        jumlah_swap = 0
        curr_i = self.head

        while curr_i:
            maks_node = curr_i           # anggap curr_i adalah maks sementara
            curr_j    = curr_i.next

            # Cari node dengan nilai terbesar di sisa list
            while curr_j:              # O(n) per iterasi luar → total O(n²)
                if curr_j.jumlah_kendaraan > maks_node.jumlah_kendaraan:
                    maks_node = curr_j
                curr_j = curr_j.next

            # Swap data (bukan pointer)
            if maks_node is not curr_i:
                # Tukar field data
                (curr_i.nama, maks_node.nama) = (maks_node.nama, curr_i.nama)
                (curr_i.jumlah_kendaraan, maks_node.jumlah_kendaraan) = \
                    (maks_node.jumlah_kendaraan, curr_i.jumlah_kendaraan)
                (curr_i.jenis_terbanyak, maks_node.jenis_terbanyak) = \
                    (maks_node.jenis_terbanyak, curr_i.jenis_terbanyak)
                (curr_i.rata_tunggu, maks_node.rata_tunggu) = \
                    (maks_node.rata_tunggu, curr_i.rata_tunggu)
                jumlah_swap += 1

            curr_i = curr_i.next

        return jumlah_swap

    # ── INSERTION SORT ────────────────────────

    def insertion_sort_desc(self) -> int:
        """
        Insertion Sort pada linked list — urutan MENURUN.
        Menggunakan teknik relink pointer.
        Big-O: O(n²) terburuk, O(n) terbaik (sudah terurut)

        Return: jumlah operasi perbandingan
        """
        if self.head is None or self.head.next is None:
            return 0

        jumlah_komparasi = 0
        terurut = None              # bagian yang sudah terurut

        curr = self.head
        while curr:
            next_node     = curr.next
            curr.next     = None

            # Sisipkan curr ke posisi yang benar di 'terurut'
            jumlah_komparasi += 1
            if terurut is None or curr.jumlah_kendaraan >= terurut.jumlah_kendaraan:
                curr.next = terurut
                terurut   = curr
            else:
                ptr = terurut
                while ptr.next:
                    jumlah_komparasi += 1
                    if curr.jumlah_kendaraan >= ptr.next.jumlah_kendaraan:
                        break
                    ptr = ptr.next
                curr.next = ptr.next
                ptr.next  = curr

            curr = next_node

        self.head = terurut
        return jumlah_komparasi


# ──────────────────────────────────────────────
# LAPORAN KEMACETAN DARI MANAJER ANTRIAN
# ──────────────────────────────────────────────

def bangun_laporan(manajer_antrian) -> LinkedListLaporan:
    """
    Bangun linked list laporan dari ManajerAntrian (Modul 2).
    Big-O: O(V * n) — V persimpangan, n kendaraan tiap antrian
    """
    from modul_2 import PRIORITAS

    laporan = LinkedListLaporan()
    for nama, pq in manajer_antrian.antrian.items():
        hitungan = pq.hitung_per_jenis()
        total    = pq.ukuran

        if total == 0:
            jenis_terbanyak = "-"
            rata_tunggu     = 0.0
        else:
            jenis_terbanyak = max(
                hitungan, key=lambda j: hitungan[j]
            )
            # Estimasi rata-rata tunggu (simulatif)
            rata_tunggu = total * 2.5     # asumsi 2.5 detik/kendaraan

        laporan.tambah(nama, total, jenis_terbanyak, rata_tunggu)

    return laporan


def bangun_laporan_simulatif(daftar_persimpangan: list,
                              seed: int = 17) -> LinkedListLaporan:
    """
    Bangun laporan kemacetan SIMULATIF (tanpa manajer antrian).
    Digunakan untuk benchmark dengan N berbeda.
    Big-O: O(n)
    """
    rng = random.Random(seed)
    lap = LinkedListLaporan()
    jenis = ["AMBULANS", "BUS", "MOBIL", "MOTOR"]
    for nama in daftar_persimpangan:
        jumlah  = rng.randint(0, 50)
        jenis_t = rng.choice(jenis)
        tunggu  = round(jumlah * rng.uniform(1.5, 4.0), 1)
        lap.tambah(nama, jumlah, jenis_t, tunggu)
    return lap


# ──────────────────────────────────────────────
# IDENTIFIKASI BOTTLENECK
# ──────────────────────────────────────────────

def identifikasi_bottleneck(laporan_terurut: LinkedListLaporan,
                            persentil: float = 0.2) -> list:
    """
    Identifikasi persimpangan bottleneck = N% teratas terpadat.
    Laporan harus sudah diurutkan descending.
    Big-O: O(n)
    Return: list NodeLaporan
    """
    k   = max(1, int(laporan_terurut.ukuran * persentil))
    hasil, curr, i = [], laporan_terurut.head, 0
    while curr and i < k:
        if curr.jumlah_kendaraan > 0:
            hasil.append(curr)
        curr = curr.next
        i   += 1
    return hasil


# ──────────────────────────────────────────────
# BENCHMARK — N = 10, 25, 100
# ──────────────────────────────────────────────

def benchmark_sorting(ukuran_list: list = None,
                      seed: int = 17) -> list:
    """
    Bandingkan runtime Selection Sort vs Insertion Sort
    untuk N = 10, 25, 100 persimpangan simulatif.
    Big-O: O(n²) kedua algoritma

    Return: list dict hasil benchmark
    """
    if ukuran_list is None:
        ukuran_list = [10, 25, 100]

    hasil_semua = []
    rng         = random.Random(seed)

    # Buat nama persimpangan simulatif
    def buat_nama(n):
        return [f"P{i:03d}" for i in range(n)]

    for n in ukuran_list:
        nama_list = buat_nama(n)

        # Buat linked list data sama untuk perbandingan fair
        laporan_ref = bangun_laporan_simulatif(nama_list, seed)

        # Selection Sort
        lap_sel = laporan_ref.salin()
        t0      = time.perf_counter()
        swap_sel = lap_sel.selection_sort_desc()
        t1      = time.perf_counter()
        t_sel   = (t1 - t0) * 1000

        # Insertion Sort
        lap_ins = laporan_ref.salin()
        t0      = time.perf_counter()
        komp_ins = lap_ins.insertion_sort_desc()
        t1      = time.perf_counter()
        t_ins   = (t1 - t0) * 1000

        # Verifikasi kebenaran
        sel_list = [node.jumlah_kendaraan for node in lap_sel.ke_list()]
        ins_list = [node.jumlah_kendaraan for node in lap_ins.ke_list()]
        benar    = sel_list == ins_list == sorted(sel_list, reverse=True)

        hasil_semua.append({
            "n"         : n,
            "t_sel"     : t_sel,
            "t_ins"     : t_ins,
            "swap_sel"  : swap_sel,
            "komp_ins"  : komp_ins,
            "benar"     : benar,
        })

    return hasil_semua


def tampilkan_benchmark(hasil: list):
    """Tampilkan tabel benchmark sorting."""
    print("\n  ╔══════════════════════════════════════════════════════╗")
    print("  ║          TABEL BENCHMARK SORTING — BIG-O O(n²)       ║")
    print("  ╠══════════╦═══════════════╦═══════════════╦══════════╣")
    print("  ║    N     ║ Selection (ms)║ Insertion (ms)║ Benar?   ║")
    print("  ╠══════════╬═══════════════╬═══════════════╬══════════╣")
    for r in hasil:
        print(f"  ║ {r['n']:>8} ║ {r['t_sel']:>13.4f} ║ "
              f"{r['t_ins']:>13.4f} ║ "
              f"{'  ✓' if r['benar'] else '  ✗':>8}   ║")
    print("  ╚══════════╩═══════════════╩═══════════════╩══════════╝")
    print()
    # Rasio runtime
    if len(hasil) >= 2:
        r1, r2 = hasil[0], hasil[-1]
        rasio_n   = r2["n"] / r1["n"]
        rasio_sel = r2["t_sel"] / r1["t_sel"] if r1["t_sel"] > 0 else 0
        rasio_ins = r2["t_ins"] / r1["t_ins"] if r1["t_ins"] > 0 else 0
        print(f"  Ketika N naik {rasio_n:.0f}× :")
        print(f"    Selection Sort lebih lambat {rasio_sel:.1f}× "
              f"(teori: {rasio_n**2:.0f}×)")
        print(f"    Insertion Sort lebih lambat {rasio_ins:.1f}× "
              f"(teori: {rasio_n**2:.0f}×)")


# ──────────────────────────────────────────────
# DEMO / TEST MANDIRI
# ──────────────────────────────────────────────

def demo_modul_5():
    from modul_1 import bangun_graf_kota, NAMA_PERSIMPANGAN
    from modul_2 import ManajerAntrian, simulasi_event

    print("\n" + "█"*60)
    print("  MODUL 5 — Sorting Laporan Kemacetan")
    print("  ELT60213 Algoritma dan Struktur Data | Topik 7")
    print("█"*60)

    # Bangun data dari simulasi
    g       = bangun_graf_kota()
    manajer = ManajerAntrian(NAMA_PERSIMPANGAN)
    simulasi_event(manajer, NAMA_PERSIMPANGAN, n_event=500, seed=17)

    laporan = bangun_laporan(manajer)
    laporan.tampilkan(maks=5, judul="Data Sebelum Sorting")

    # Selection Sort
    lap_sel = laporan.salin()
    t0 = time.perf_counter()
    swap = lap_sel.selection_sort_desc()
    t1 = time.perf_counter()
    print(f"\n  [✓] Selection Sort selesai: {swap} swap, "
          f"{(t1-t0)*1000:.4f} ms")
    lap_sel.tampilkan(maks=8, judul="Setelah Selection Sort (Desc)")

    # Insertion Sort
    lap_ins = laporan.salin()
    t0 = time.perf_counter()
    komp = lap_ins.insertion_sort_desc()
    t1 = time.perf_counter()
    print(f"\n  [✓] Insertion Sort selesai: {komp} komparasi, "
          f"{(t1-t0)*1000:.4f} ms")

    # Verifikasi hasil sama
    sel_l = [n.jumlah_kendaraan for n in lap_sel.ke_list()]
    ins_l = [n.jumlah_kendaraan for n in lap_ins.ke_list()]
    print(f"\n  [i] Hasil Selection == Insertion: {sel_l == ins_l}")

    # Bottleneck
    btk = identifikasi_bottleneck(lap_sel, persentil=0.2)
    print(f"\n  [>] Bottleneck (20% teratas = {len(btk)} persimpangan):")
    for b in btk:
        print(f"  ⚠ {b}")

    # Benchmark N=10, 25, 100
    print("\n  [>] Benchmark Sorting (N=10, 25, 100) ...")
    hasil_bm = benchmark_sorting([10, 25, 100], seed=17)
    tampilkan_benchmark(hasil_bm)

    print("  ╔══════════════════════════════════════════╗")
    print("  ║         RINGKASAN BIG-O MODUL 5          ║")
    print("  ╠══════════════════════════════════════════╣")
    print("  ║  Selection Sort  : O(n²) selalu          ║")
    print("  ║  Insertion Sort  : O(n²) terburuk        ║")
    print("  ║                    O(n)  terbaik         ║")
    print("  ║  bangun_laporan  : O(V·n)                ║")
    print("  ║  bottleneck      : O(n)                  ║")
    print("  ╚══════════════════════════════════════════╝")

    return lap_sel


if __name__ == "__main__":
    demo_modul_5()