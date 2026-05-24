"""
=============================================================
TOPIK 7 - Smart Traffic Simulation & Signal Optimization
ELT60213 Algoritma dan Struktur Data | TA 2025/2026
=============================================================
MODUL 3: Dijkstra Rute Optimal
- Implementasi Dijkstra dari persimpangan sumber ke semua tujuan
- Output: jarak minimum dan rekonstruksi jalur
- Gunakan untuk rekomendasi rute alternatif saat kemacetan
- Tanpa heap library — menggunakan Priority Queue manual (Modul 2)
- Big-O: O(V² + E) tanpa heap
- 50 query rute sesuai spesifikasi
=============================================================
"""

import time


# ──────────────────────────────────────────────
# PRIORITY QUEUE MIN untuk Dijkstra (internal)
# Manual — tidak menggunakan heapq
# ──────────────────────────────────────────────
class _MinPQNode:
    def __init__(self, jarak: float, nama: str):
        self.jarak = jarak
        self.nama  = nama
        self.next  = None


class _MinPQ:
    """
    Min Priority Queue sederhana berbasis sorted linked list.
    Digunakan internal oleh Dijkstra.
    enqueue: O(n) | dequeue_min: O(1)
    """
    def __init__(self):
        self.head  = None
        self.ukuran = 0

    def masukkan(self, jarak: float, nama: str):
        node = _MinPQNode(jarak, nama)
        if self.head is None or jarak < self.head.jarak:
            node.next  = self.head
            self.head  = node
        else:
            curr = self.head
            while curr.next and curr.next.jarak <= jarak:
                curr = curr.next
            node.next  = curr.next
            curr.next  = node
        self.ukuran += 1

    def ambil_min(self):
        if self.head is None:
            return None, None
        node       = self.head
        self.head  = self.head.next
        self.ukuran -= 1
        return node.jarak, node.nama

    def kosong(self) -> bool:
        return self.head is None

    def perbarui(self, nama: str, jarak_baru: float):
        """
        Perbarui jarak node jika sudah ada.
        Hapus lama, masukkan baru. O(n).
        """
        prev, curr = None, self.head
        while curr:
            if curr.nama == nama:
                if prev:
                    prev.next = curr.next
                else:
                    self.head = curr.next
                self.ukuran -= 1
                break
            prev, curr = curr, curr.next
        self.masukkan(jarak_baru, nama)


# ──────────────────────────────────────────────
# HASIL DIJKSTRA
# ──────────────────────────────────────────────
class HasilDijkstra:
    """Menyimpan hasil satu run Dijkstra dari satu sumber."""

    def __init__(self, sumber: str, jarak: dict, pendahulu: dict,
                 waktu_eksekusi: float):
        self.sumber         = sumber
        self.jarak          = jarak          # {nama: jarak_minimum}
        self.pendahulu      = pendahulu      # {nama: nama_sebelumnya}
        self.waktu_eksekusi = waktu_eksekusi # detik

    def jalur_ke(self, tujuan: str) -> list:
        """
        Rekonstruksi jalur dari sumber ke tujuan.
        Big-O: O(V) — penelusuran mundur
        Return: list nama persimpangan [sumber, ..., tujuan]
                atau [] jika tidak terjangkau
        """
        if tujuan not in self.jarak or self.jarak[tujuan] == float('inf'):
            return []
        jalur = []
        curr  = tujuan
        while curr is not None:
            jalur.append(curr)
            curr = self.pendahulu.get(curr)
        jalur.reverse()
        return jalur

    def jarak_ke(self, tujuan: str) -> float:
        """
        Kembalikan jarak minimum ke tujuan.
        Big-O: O(1)
        Return: float atau inf jika tidak terjangkau
        """
        return self.jarak.get(tujuan, float('inf'))

    def terjangkau(self, tujuan: str) -> bool:
        """Big-O: O(1)"""
        return self.jarak.get(tujuan, float('inf')) < float('inf')

    def tampilkan_rute(self, tujuan: str):
        """Tampilkan rute dari sumber ke tujuan."""
        jalur  = self.jalur_ke(tujuan)
        jarak  = self.jarak_ke(tujuan)
        print(f"\n  Rute  : {self.sumber} → {tujuan}")
        if not jalur:
            print("  Status: ✗ Tidak ada rute")
            return
        print(f"  Jarak : {jarak:.0f} meter  ({jarak/1000:.2f} km)")
        print(f"  Jalur : {' → '.join(jalur)}")
        print(f"  Hop   : {len(jalur)-1} persimpangan")

    def ringkasan(self, maks: int = 5):
        """Tampilkan ringkasan jarak ke semua tujuan (maks terpendek)."""
        terurut = sorted(
            [(k, v) for k, v in self.jarak.items() if v < float('inf')],
            key=lambda x: x[1]
        )
        print(f"\n  ── Dijkstra dari '{self.sumber}' "
              f"({self.waktu_eksekusi*1000:.2f} ms) ──")
        print(f"  {'Tujuan':<20} {'Jarak (m)':>10}  Jalur")
        print("  " + "-"*55)
        for nama, jrk in terurut[:maks]:
            jalur = " → ".join(self.jalur_ke(nama))
            print(f"  {nama:<20} {jrk:>10.0f}  {jalur}")


# ──────────────────────────────────────────────
# DIJKSTRA UTAMA
# ──────────────────────────────────────────────
class DijkstraRuteOptimal:
    """
    Implementasi Dijkstra tanpa library heap.
    Menggunakan MinPQ manual berbasis sorted linked list.

    Big-O: O(V² + E) — karena enqueue O(V) di setiap iterasi
    Untuk graf padat: ekuivalen dengan O(V²)
    """

    def __init__(self, graf):
        """
        graf: instance GraphJaringanJalan dari modul_1
        """
        self.graf = graf
        self._cache = {}    # cache hasil per sumber

    def jalankan(self, sumber: str,
                 gunakan_cache: bool = True) -> HasilDijkstra:
        """
        Jalankan Dijkstra dari 'sumber' ke semua node.
        Big-O: O(V² + E) tanpa heap
        """
        if sumber not in self.graf.adj:
            raise ValueError(f"Sumber '{sumber}' tidak ada di graf.")

        if gunakan_cache and sumber in self._cache:
            return self._cache[sumber]

        t_mulai  = time.perf_counter()

        # Inisialisasi
        semua    = self.graf.nodes
        jarak    = {v: float('inf') for v in semua}
        pendahulu = {v: None for v in semua}
        dikunjungi = set()
        jarak[sumber] = 0.0

        pq = _MinPQ()
        pq.masukkan(0.0, sumber)

        while not pq.kosong():
            jarak_u, u = pq.ambil_min()

            if u in dikunjungi:
                continue
            dikunjungi.add(u)

            # Relaksasi edge
            for tetangga, bobot in self.graf.tetangga(u):
                alt = jarak_u + bobot
                if alt < jarak[tetangga]:
                    jarak[tetangga]     = alt
                    pendahulu[tetangga] = u
                    pq.masukkan(alt, tetangga)

        t_selesai = time.perf_counter()
        hasil = HasilDijkstra(
            sumber, jarak, pendahulu,
            t_selesai - t_mulai
        )

        if gunakan_cache:
            self._cache[sumber] = hasil
        return hasil

    def rute(self, asal: str, tujuan: str) -> tuple:
        """
        Kembalikan (jalur, jarak) dari asal ke tujuan.
        Big-O: O(V² + E) untuk Dijkstra + O(V) rekonstruksi
        """
        hasil = self.jalankan(asal)
        return hasil.jalur_ke(tujuan), hasil.jarak_ke(tujuan)

    def rute_alternatif(self, asal: str, tujuan: str,
                        k: int = 3) -> list:
        """
        Temukan hingga k rute alternatif dengan menghapus
        edge kritis satu per satu (simple k-path approximation).
        Big-O: O(k * (V² + E))
        Return: list of (jalur, jarak)
        """
        rute_list = []
        jalur_utama, jarak_utama = self.rute(asal, tujuan)

        if not jalur_utama:
            return rute_list

        rute_list.append((jalur_utama, jarak_utama))

        # Variasi: hapus sementara edge dari jalur utama
        for i in range(len(jalur_utama) - 1):
            u, v     = jalur_utama[i], jalur_utama[i+1]
            bobot_uv = self.graf.bobot_jalan(u, v)
            bobot_vu = self.graf.bobot_jalan(v, u)

            if bobot_uv is None:
                continue

            # Hapus sementara
            self.graf.hapus_jalan(u, v, dua_arah=False)
            if bobot_vu is not None:
                self.graf.hapus_jalan(v, u, dua_arah=False)

            # Hitung ulang (tanpa cache)
            try:
                hasil_alt = self.jalankan(asal, gunakan_cache=False)
                jalur_alt = hasil_alt.jalur_ke(tujuan)
                jarak_alt = hasil_alt.jarak_ke(tujuan)

                if jalur_alt and jalur_alt not in [r[0] for r in rute_list]:
                    rute_list.append((jalur_alt, jarak_alt))
            except Exception:
                pass

            # Pulihkan edge
            self.graf.tambah_jalan(u, v, bobot_uv, dua_arah=False)
            if bobot_vu is not None:
                self.graf.tambah_jalan(v, u, bobot_vu, dua_arah=False)

            if len(rute_list) >= k:
                break

        return sorted(rute_list, key=lambda x: x[1])


# ──────────────────────────────────────────────
# BATCH QUERY — 50 rute sesuai spesifikasi
# ──────────────────────────────────────────────

def jalankan_50_query(dijkstra, daftar_persimpangan: list,
                      seed: int = 17) -> list:
    """
    Jalankan 50 query rute acak sesuai spesifikasi.
    Big-O: O(50 * (V² + E))
    Return: list dict hasil query
    """
    import random
    import numpy as np
    random.seed(seed)
    np.random.seed(seed)

    hasil_query = []
    for i in range(50):
        asal   = random.choice(daftar_persimpangan)
        tujuan = random.choice(daftar_persimpangan)
        while tujuan == asal:
            tujuan = random.choice(daftar_persimpangan)

        jalur, jarak = dijkstra.rute(asal, tujuan)
        hasil_query.append({
            "no"    : i + 1,
            "asal"  : asal,
            "tujuan": tujuan,
            "jalur" : jalur,
            "jarak" : jarak,
            "hop"   : len(jalur) - 1 if jalur else 0,
            "valid" : bool(jalur),
        })

    return hasil_query


def tampilkan_hasil_query(hasil: list, maks: int = 10):
    """Tampilkan tabel hasil 50 query."""
    print(f"\n  {'No':>3} {'Asal':<16} {'Tujuan':<16} "
          f"{'Jarak (m)':>10} {'Hop':>4} {'Valid':>5}")
    print("  " + "─"*58)
    for r in hasil[:maks]:
        print(f"  {r['no']:>3} {r['asal']:<16} {r['tujuan']:<16} "
              f"{r['jarak']:>10.0f} {r['hop']:>4} "
              f"{'✓' if r['valid'] else '✗':>5}")
    if len(hasil) > maks:
        print(f"  ... dan {len(hasil) - maks} query lainnya")


# ──────────────────────────────────────────────
# DEMO / TEST MANDIRI
# ──────────────────────────────────────────────

def demo_modul_3():
    from modul_1 import build_traffic_graph, NAMA_PERSIMPANGAN

    print("\n" + "█"*60)
    print("  MODUL 3 — Dijkstra Rute Optimal")
    print("  ELT60213 Algoritma dan Struktur Data | Topik 7")
    print("█"*60)

    g = build_traffic_graph()
    dijkstra = DijkstraRuteOptimal(g)

    # Single source dari Malioboro
    print("\n  [>] Dijkstra dari 'Malioboro' ...")
    hasil = dijkstra.jalankan("Malioboro")
    hasil.ringkasan(maks=8)

    # Rute spesifik
    pasangan = [
        ("Malioboro", "Prambanan"),
        ("Tugu", "Wonosari"),
        ("Kraton", "Kaliurang"),
    ]
    print("\n  [>] Query Rute Spesifik:")
    for asal, tujuan in pasangan:
        hasil.tampilkan_rute(tujuan) if asal == "Malioboro" else \
            dijkstra.jalankan(asal).tampilkan_rute(tujuan)

    # 50 query batch
    print("\n  [>] Menjalankan 50 query rute (spesifikasi) ...")
    t0 = time.perf_counter()
    query_hasil = jalankan_50_query(dijkstra, NAMA_PERSIMPANGAN)
    t1 = time.perf_counter()
    print(f"  [✓] 50 query selesai dalam {(t1-t0)*1000:.2f} ms")

    valid = sum(1 for r in query_hasil if r["valid"])
    print(f"  [i] Rute valid: {valid}/50")

    tampilkan_hasil_query(query_hasil, maks=10)

    # Rute alternatif
    print("\n  [>] Rute Alternatif Malioboro → Prambanan:")
    alts = dijkstra.rute_alternatif("Malioboro", "Prambanan", k=3)
    for i, (jalur, jarak) in enumerate(alts, 1):
        print(f"  Opsi {i} ({jarak:.0f}m): {' → '.join(jalur)}")

    print("\n  ╔══════════════════════════════════════════╗")
    print("  ║         RINGKASAN BIG-O MODUL 3          ║")
    print("  ╠══════════════════════════════════════════╣")
    print("  ║  Dijkstra (tanpa heap)   : O(V² + E)    ║")
    print("  ║  Rekonstruksi jalur      : O(V)          ║")
    print("  ║  50 query rute           : O(50·(V²+E)) ║")
    print("  ║  Rute alternatif (k)     : O(k·(V²+E)) ║")
    print("  ║  _MinPQ enqueue          : O(n)          ║")
    print("  ║  _MinPQ dequeue_min      : O(1)          ║")
    print("  ╚══════════════════════════════════════════╝")

    return dijkstra, query_hasil


if __name__ == "__main__":
    demo_modul_3()