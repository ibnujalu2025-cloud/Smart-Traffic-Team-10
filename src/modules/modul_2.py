"""
=============================================================
TOPIK 7 - Smart Traffic Simulation & Signal Optimization
ELT60213 Algoritma dan Struktur Data | TA 2025/2026
=============================================================
MODUL 2: Priority Queue Kendaraan
- Setiap persimpangan memiliki Priority Queue kendaraan
- AMBULANS (prioritas 1) selalu berangkat duluan,
  diikuti BUS (2), MOBIL (3), MOTOR (4)
- Tie-break: FIFO (waktu masuk lebih awal = didahulukan)
- Mendukung: MASUK, BERANGKAT, ANTRIAN
- Big-O: enqueue O(n), dequeue O(1)
=============================================================
"""

import time


# ──────────────────────────────────────────────
# KONSTANTA PRIORITAS
# ──────────────────────────────────────────────
PRIORITAS = {
    "AMBULANS": 1,
    "BUS"     : 2,
    "MOBIL"   : 3,
    "MOTOR"   : 4,
}

JENIS_VALID = set(PRIORITAS.keys())


# ──────────────────────────────────────────────
# NODE KENDARAAN
# ──────────────────────────────────────────────
class NodeKendaraan:
    """
    Simpul dalam Priority Queue.
    Menyimpan data satu kendaraan.
    """
    _id_counter = 0     # auto-increment ID

    def __init__(self, jenis: str, plat: str,
                 asal: str, tujuan: str, waktu_masuk: float = None):
        NodeKendaraan._id_counter += 1
        self.id           = NodeKendaraan._id_counter
        self.jenis        = jenis.upper()
        self.prioritas    = PRIORITAS.get(self.jenis, 99)
        self.plat         = plat
        self.asal         = asal
        self.tujuan       = tujuan
        self.waktu_masuk  = waktu_masuk if waktu_masuk is not None else time.time()
        self.next         = None        # pointer linked list

    def __str__(self):
        return (f"[{self.jenis}|P{self.prioritas}] "
                f"Plat:{self.plat} {self.asal}→{self.tujuan} "
                f"(id={self.id})")


# ──────────────────────────────────────────────
# PRIORITY QUEUE berbasis Sorted Linked List
# ──────────────────────────────────────────────
class PriorityQueueKendaraan:
    """
    Priority Queue menggunakan sorted linked list.
    - Semakin kecil nilai prioritas → semakin depan
    - Tie-break: waktu_masuk lebih kecil (FIFO) → lebih depan
    - enqueue: O(n)  — insert ke posisi yang benar
    - dequeue: O(1)  — ambil dari head
    - peek   : O(1)
    - cari   : O(n)
    """

    def __init__(self, nama_persimpangan: str = ""):
        self.nama         = nama_persimpangan
        self.head         = None
        self.ukuran       = 0
        self.total_masuk  = 0
        self.total_keluar = 0

    # ── ENQUEUE ──────────────────────────────

    def masuk(self, jenis: str, plat: str,
              asal: str, tujuan: str,
              waktu_masuk: float = None) -> NodeKendaraan:
        """
        Masukkan kendaraan ke antrian dengan urutan prioritas.
        Big-O: O(n) — traversal untuk mencari posisi insert

        Urutan: prioritas kecil → depan; tie → waktu_masuk kecil depan (FIFO)
        """
        if jenis.upper() not in JENIS_VALID:
            raise ValueError(f"Jenis kendaraan '{jenis}' tidak valid. "
                             f"Pilih: {JENIS_VALID}")

        node = NodeKendaraan(jenis, plat, asal, tujuan, waktu_masuk)

        # Kasus 1: antrian kosong atau node lebih prioritas dari head
        if (self.head is None or
                node.prioritas < self.head.prioritas or
                (node.prioritas == self.head.prioritas and
                 node.waktu_masuk < self.head.waktu_masuk)):
            node.next  = self.head
            self.head  = node
        else:
            # Cari posisi yang tepat
            curr = self.head
            while (curr.next is not None and
                   not (node.prioritas < curr.next.prioritas or
                        (node.prioritas == curr.next.prioritas and
                         node.waktu_masuk < curr.next.waktu_masuk))):
                curr = curr.next
            node.next  = curr.next
            curr.next  = node

        self.ukuran      += 1
        self.total_masuk += 1
        return node

    # ── DEQUEUE ──────────────────────────────

    def berangkat(self) -> NodeKendaraan:
        """
        Keluarkan kendaraan dengan prioritas tertinggi (depan antrian).
        Big-O: O(1)
        Return None jika antrian kosong.
        """
        if self.head is None:
            return None
        keluar     = self.head
        self.head  = self.head.next
        keluar.next = None
        self.ukuran       -= 1
        self.total_keluar += 1
        return keluar

    # ── PEEK ─────────────────────────────────

    def lihat_depan(self) -> NodeKendaraan:
        """
        Lihat kendaraan terdepan tanpa mengeluarkan.
        Big-O: O(1)
        """
        return self.head

    # ── UTILITAS ─────────────────────────────

    def kosong(self) -> bool:
        """Big-O: O(1)"""
        return self.head is None

    def panjang(self) -> int:
        """Big-O: O(1)"""
        return self.ukuran

    def cari_kendaraan(self, plat: str) -> NodeKendaraan:
        """
        Cari kendaraan berdasarkan nomor plat.
        Big-O: O(n)
        """
        curr = self.head
        while curr:
            if curr.plat.upper() == plat.upper():
                return curr
            curr = curr.next
        return None

    def hitung_per_jenis(self) -> dict:
        """
        Hitung jumlah kendaraan per jenis dalam antrian.
        Big-O: O(n)
        """
        hitungan = {j: 0 for j in JENIS_VALID}
        curr = self.head
        while curr:
            hitungan[curr.jenis] = hitungan.get(curr.jenis, 0) + 1
            curr = curr.next
        return hitungan

    def daftar_antrian(self) -> list:
        """
        Kembalikan list semua NodeKendaraan dalam urutan antrian.
        Big-O: O(n)
        """
        hasil, curr = [], self.head
        while curr:
            hasil.append(curr)
            curr = curr.next
        return hasil

    def tampilkan(self):
        """Tampilkan isi antrian."""
        print(f"\n  ── Antrian [{self.nama}] "
              f"({self.ukuran} kendaraan) ──")
        if self.kosong():
            print("     (kosong)")
            return
        curr, urutan = self.head, 1
        while curr:
            tag = " ◄ BERANGKAT BERIKUTNYA" if urutan == 1 else ""
            print(f"     {urutan:2d}. {curr}{tag}")
            curr    = curr.next
            urutan += 1

    def statistik(self):
        """Tampilkan statistik antrian."""
        hitung = self.hitung_per_jenis()
        print(f"\n  ── Statistik [{self.nama}] ──")
        print(f"     Total masuk  : {self.total_masuk}")
        print(f"     Total keluar : {self.total_keluar}")
        print(f"     Dalam antrian: {self.ukuran}")
        for jenis, jumlah in sorted(hitung.items(),
                                    key=lambda x: PRIORITAS[x[0]]):
            bar = "█" * jumlah
            print(f"     {jenis:<10}: {jumlah:3d}  {bar}")


# ──────────────────────────────────────────────
# MANAJER ANTRIAN SELURUH PERSIMPANGAN
# ──────────────────────────────────────────────
class ManajerAntrian:
    """
    Mengelola Priority Queue untuk setiap persimpangan.
    Diinisialisasi dengan daftar nama persimpangan.
    """

    def __init__(self, daftar_persimpangan: list):
        self.antrian = {
            nama: PriorityQueueKendaraan(nama)
            for nama in daftar_persimpangan
        }

    def masuk(self, persimpangan: str, jenis: str, plat: str,
              asal: str, tujuan: str,
              waktu: float = None) -> NodeKendaraan:
        """
        Kendaraan masuk ke antrian persimpangan tertentu.
        Big-O: O(n)
        """
        if persimpangan not in self.antrian:
            raise KeyError(f"Persimpangan '{persimpangan}' tidak ada.")
        return self.antrian[persimpangan].masuk(
            jenis, plat, asal, tujuan, waktu)

    def berangkat(self, persimpangan: str) -> NodeKendaraan:
        """
        Kendaraan prioritas tertinggi berangkat dari persimpangan.
        Big-O: O(1)
        """
        if persimpangan not in self.antrian:
            raise KeyError(f"Persimpangan '{persimpangan}' tidak ada.")
        return self.antrian[persimpangan].berangkat()

    def antrian_persimpangan(self, persimpangan: str) -> list:
        """
        Tampilkan/kembalikan antrian di satu persimpangan.
        Big-O: O(n)
        """
        if persimpangan not in self.antrian:
            return []
        return self.antrian[persimpangan].daftar_antrian()

    def total_kendaraan(self) -> int:
        """Total kendaraan di semua persimpangan. Big-O: O(V)"""
        return sum(q.ukuran for q in self.antrian.values())

    def persimpangan_tersibuk(self) -> tuple:
        """
        Temukan persimpangan dengan antrian terpanjang.
        Big-O: O(V)
        Return: (nama, jumlah)
        """
        if not self.antrian:
            return (None, 0)
        maks = max(self.antrian.items(), key=lambda x: x[1].ukuran)
        return (maks[0], maks[1].ukuran)

    def tampilkan_semua(self, maks: int = 5):
        """Tampilkan antrian semua persimpangan (maks pertama)."""
        for i, (nama, q) in enumerate(self.antrian.items()):
            if i >= maks:
                break
            q.tampilkan()


# ──────────────────────────────────────────────
# SIMULASI EVENT KENDARAAN
# ──────────────────────────────────────────────

def simulasi_event(manajer: ManajerAntrian,
                   daftar_persimpangan: list,
                   n_event: int = 500,
                   seed: int = 17) -> list:
    """
    Simulasikan 500 event kendaraan masuk/keluar secara acak.
    Seed = 17 untuk reprodusibilitas.

    Event: 70% MASUK, 30% BERANGKAT
    Big-O: O(n * max_antrian)
    Return: list log event
    """
    import random as rnd
    rnd.seed(seed)
    import numpy as np
    np.random.seed(seed)

    jenis_list   = list(PRIORITAS.keys())
    bobot_masuk  = [1, 4, 6, 8]     # prob: AMBULANS lebih jarang
    log          = []
    plat_counter = 1000

    for i in range(n_event):
        waktu       = i * 0.1           # waktu simulasi (detik)
        persimpangan = rnd.choice(daftar_persimpangan)
        event_type  = "MASUK" if rnd.random() < 0.7 else "BERANGKAT"

        if event_type == "MASUK":
            jenis   = rnd.choices(jenis_list, weights=bobot_masuk)[0]
            plat    = f"AB{plat_counter:04d}{jenis[0]}"
            tujuan  = rnd.choice(daftar_persimpangan)
            plat_counter += 1
            try:
                node = manajer.masuk(persimpangan, jenis, plat,
                                     persimpangan, tujuan, waktu)
                log.append({
                    "event"        : "MASUK",
                    "t"            : waktu,
                    "persimpangan" : persimpangan,
                    "kendaraan"    : str(node),
                })
            except Exception as e:
                log.append({"event": "ERROR", "pesan": str(e)})
        else:
            node = manajer.berangkat(persimpangan)
            log.append({
                "event"        : "BERANGKAT",
                "t"            : waktu,
                "persimpangan" : persimpangan,
                "kendaraan"    : str(node) if node else "(kosong)",
            })

    return log


# ──────────────────────────────────────────────
# DEMO / TEST MANDIRI
# ──────────────────────────────────────────────

def demo_modul_2():
    from modul_1 import NAMA_PERSIMPANGAN

    print("\n" + "█"*60)
    print("  MODUL 2 — Priority Queue Kendaraan")
    print("  ELT60213 Algoritma dan Struktur Data | Topik 7")
    print("█"*60)

    manajer = ManajerAntrian(NAMA_PERSIMPANGAN)

    # Simulasi 500 event
    print("\n  [>] Menjalankan simulasi 500 event ...")
    log = simulasi_event(manajer, NAMA_PERSIMPANGAN,
                         n_event=500, seed=17)

    masuk_count    = sum(1 for e in log if e["event"] == "MASUK")
    berangkat_count = sum(1 for e in log if e["event"] == "BERANGKAT")
    print(f"  [✓] Event selesai: {masuk_count} MASUK, "
          f"{berangkat_count} BERANGKAT")
    print(f"  [i] Total kendaraan tersisa: {manajer.total_kendaraan()}")

    sibuk, jml = manajer.persimpangan_tersibuk()
    print(f"  [i] Persimpangan tersibuk: {sibuk} ({jml} kendaraan)")

    # Demo antrian manual
    print("\n  [>] Demo antrian manual di 'Malioboro' :")
    pq = manajer.antrian["Malioboro"]

    # Tambah beberapa kendaraan manual untuk demo urutan
    demo_pq = PriorityQueueKendaraan("Malioboro-Demo")
    demo_pq.masuk("MOTOR",    "AB9001M", "Malioboro", "Tugu",       waktu_masuk=1.0)
    demo_pq.masuk("AMBULANS", "AB0001A", "Malioboro", "Kraton",     waktu_masuk=2.0)
    demo_pq.masuk("MOBIL",    "AB5001B", "Malioboro", "Depok",      waktu_masuk=1.5)
    demo_pq.masuk("BUS",      "AB3001B", "Malioboro", "Kaliurang",  waktu_masuk=0.5)
    demo_pq.masuk("AMBULANS", "AB0002A", "Malioboro", "Bantul",     waktu_masuk=1.0)
    demo_pq.tampilkan()

    print("\n  [>] Proses BERANGKAT 3 kendaraan:")
    for _ in range(3):
        k = demo_pq.berangkat()
        print(f"     → Berangkat: {k}")

    demo_pq.tampilkan()

    # Statistik
    pq.statistik()

    print("\n  ╔══════════════════════════════════════════╗")
    print("  ║         RINGKASAN BIG-O MODUL 2          ║")
    print("  ╠══════════════════════════════════════════╣")
    print("  ║  enqueue / masuk     : O(n)              ║")
    print("  ║  dequeue / berangkat : O(1)              ║")
    print("  ║  peek / lihat_depan  : O(1)              ║")
    print("  ║  cari_kendaraan      : O(n)              ║")
    print("  ║  hitung_per_jenis    : O(n)              ║")
    print("  ╚══════════════════════════════════════════╝")

    return manajer, log


if __name__ == "__main__":
    demo_modul_2()