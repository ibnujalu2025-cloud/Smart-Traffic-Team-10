"""
=============================================================
TOPIK 7 - Smart Traffic Simulation & Signal Optimization
ELT60213 Algoritma dan Struktur Data | TA 2025/2026
=============================================================
MODUL 6: CLI Simulasi
- Command Line Interface interaktif untuk simulasi lalu lintas
- Perintah: MASUK, BERANGKAT, RUTE, ANTRIAN, LAPORAN,
            KEMACETAN, ISOLASI, SIKLUS_LAMPU, KELUAR
- Setiap perintah menampilkan Big-O
=============================================================
"""

import sys
import os
import time
import random
import numpy as np

# Seed global
np.random.seed(17)
random.seed(17)

# Tambah path agar modul dapat diimport
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modul_1 import bangun_graf_kota, NAMA_PERSIMPANGAN, GraphJaringanJalan
from modul_2 import ManajerAntrian, simulasi_event, PRIORITAS
from modul_3 import DijkstraRuteOptimal
from modul_4 import BSTIndeksPersimpangan, bangun_bst_dari_graf
from modul_5 import (bangun_laporan, LinkedListLaporan,
                     identifikasi_bottleneck)


# ââââââââââââââââââââââââââââââââââââââââââââââ
# SIKLUS LAMPU LALU LINTAS
# ââââââââââââââââââââââââââââââââââââââââââââââ

class SiklusLampu:
    """
    Simulasi siklus lampu lalu lintas per persimpangan.
    Stack digunakan untuk history perubahan fase.
    Big-O: push/pop O(1)
    """

    FASE = ["MERAH", "KUNING", "HIJAU"]

    def __init__(self, nama: str, durasi_default: int = 30):
        self.nama           = nama
        self.fase_index     = 0                    # indeks fase saat ini
        self.durasi         = {                    # detik per fase
            "MERAH"  : durasi_default,
            "KUNING" : 5,
            "HIJAU"  : durasi_default,
        }
        self.history_stack  = []                   # stack history fase
        self.siklus_selesai = 0

    def fase_sekarang(self) -> str:
        return self.FASE[self.fase_index]

    def maju(self):
        """Maju ke fase berikutnya. Push ke history stack. O(1)"""
        self.history_stack.append(self.fase_sekarang())
        self.fase_index = (self.fase_index + 1) % len(self.FASE)
        if self.fase_index == 0:
            self.siklus_selesai += 1

    def mundur(self) -> str:
        """Mundur ke fase sebelumnya (pop history). O(1)"""
        if not self.history_stack:
            return None
        fase_lama = self.history_stack.pop()
        self.fase_index = self.FASE.index(fase_lama)
        return fase_lama

    def atur_durasi(self, fase: str, detik: int):
        """Atur durasi fase tertentu. O(1)"""
        if fase.upper() in self.durasi:
            self.durasi[fase.upper()] = detik

    def status(self) -> str:
        fase = self.fase_sekarang()
        dur  = self.durasi[fase]
        return (f"[{self.nama}] LAMPU: {fase} ({dur}s) | "
                f"Siklus ke-{self.siklus_selesai}")


class ManajerLampu:
    """Mengelola siklus lampu semua persimpangan."""

    def __init__(self, daftar_persimpangan: list):
        self.lampu = {
            nama: SiklusLampu(nama)
            for nama in daftar_persimpangan
        }

    def maju(self, persimpangan: str):
        if persimpangan in self.lampu:
            self.lampu[persimpangan].maju()

    def status(self, persimpangan: str) -> str:
        if persimpangan not in self.lampu:
            return f"Persimpangan '{persimpangan}' tidak ditemukan."
        return self.lampu[persimpangan].status()

    def semua_status(self, maks: int = 5) -> list:
        return [l.status() for l in list(self.lampu.values())[:maks]]


# ââââââââââââââââââââââââââââââââââââââââââââââ
# STATE SIMULASI GLOBAL
# ââââââââââââââââââââââââââââââââââââââââââââââ

class StateSimulasi:
    """Menyimpan seluruh state simulasi."""

    def __init__(self):
        print("  [â³] Membangun infrastruktur simulasi ...")
        self.graf        = bangun_graf_kota()
        self.manajer     = ManajerAntrian(NAMA_PERSIMPANGAN)
        self.dijkstra    = DijkstraRuteOptimal(self.graf)
        self.bst         = bangun_bst_dari_graf(self.graf)
        self.manajer_lampu = ManajerLampu(NAMA_PERSIMPANGAN)
        self.log_event   = []
        self.waktu_sim   = 0.0
        self.plat_counter = 1000
        print("  [â] Infrastruktur siap!")
        print(f"  [i] {self.graf.jumlah_persimpangan} persimpangan, "
              f"{self.graf.jumlah_jalan} ruas jalan terdaftar")

    def plat_baru(self, jenis: str) -> str:
        self.plat_counter += 1
        return f"AB{self.plat_counter:04d}{jenis[0]}"


# ââââââââââââââââââââââââââââââââââââââââââââââ
# HANDLER PERINTAH CLI
# ââââââââââââââââââââââââââââââââââââââââââââââ

def _header(judul: str):
    lebar = 58
    print("\n  " + "â" * lebar)
    print(f"  {'  ' + judul:^{lebar}}")
    print("  " + "â" * lebar)


def _bigo(operasi: str, kompleksitas: str):
    print(f"  [Big-O] {operasi:<35} â {kompleksitas}")


def cmd_masuk(state: StateSimulasi, args: list):
    """
    MASUK <persimpangan> <jenis>
    Masukkan kendaraan ke antrian persimpangan.
    Big-O: O(n)
    """
    _header("MASUK KENDARAAN")
    if len(args) < 2:
        print("  Penggunaan: MASUK <persimpangan> <jenis>")
        print(f"  Jenis valid: {', '.join(PRIORITAS.keys())}")
        print(f"  Contoh    : MASUK Malioboro AMBULANS")
        return

    persimpangan = args[0].capitalize()
    jenis        = args[1].upper()

    # Validasi persimpangan
    if not state.bst.ada(persimpangan):
        # Coba partial match
        cocok = state.bst.cari_awalan(persimpangan[:3])
        if cocok:
            persimpangan = cocok[0][0]
            print(f"  [i] Persimpangan dikoreksi â '{persimpangan}'")
        else:
            print(f"  [â] Persimpangan '{persimpangan}' tidak ditemukan.")
            print(f"  Tersedia: {', '.join(NAMA_PERSIMPANGAN[:5])} ...")
            _bigo("BST search", "O(log V)")
            return

    if jenis not in PRIORITAS:
        print(f"  [â] Jenis '{jenis}' tidak valid. Pilih: "
              f"{', '.join(PRIORITAS.keys())}")
        return

    plat   = state.plat_baru(jenis)
    tujuan = random.choice(NAMA_PERSIMPANGAN)
    state.waktu_sim += 0.1

    try:
        node = state.manajer.masuk(
            persimpangan, jenis, plat,
            persimpangan, tujuan, state.waktu_sim
        )
        print(f"  [â] {node}")
        print(f"  Menuju  : {tujuan}")
        print(f"  Antrian : {state.manajer.antrian[persimpangan].ukuran} kendaraan")
        state.log_event.append({"cmd": "MASUK", "node": str(node)})
    except Exception as e:
        print(f"  [â] Error: {e}")

    _bigo("enqueue ke Priority Queue", "O(n)")
    _bigo("BST search persimpangan", "O(log V)")


def cmd_berangkat(state: StateSimulasi, args: list):
    """
    BERANGKAT <persimpangan>
    Kendaraan prioritas tertinggi berangkat.
    Big-O: O(1)
    """
    _header("KENDARAAN BERANGKAT")
    if not args:
        print("  Penggunaan: BERANGKAT <persimpangan>")
        print("  Contoh    : BERANGKAT Malioboro")
        return

    persimpangan = args[0].capitalize()
    if persimpangan not in state.manajer.antrian:
        print(f"  [â] Persimpangan '{persimpangan}' tidak ditemukan.")
        _bigo("dequeue Priority Queue", "O(1)")
        return

    pq = state.manajer.antrian[persimpangan]
    if pq.kosong():
        print(f"  [i] Antrian '{persimpangan}' kosong â tidak ada kendaraan.")
        _bigo("dequeue Priority Queue", "O(1)")
        return

    node = state.manajer.berangkat(persimpangan)
    print(f"  [â] Berangkat: {node}")
    print(f"  Sisa antrian: {pq.ukuran} kendaraan")
    state.log_event.append({"cmd": "BERANGKAT", "node": str(node)})
    _bigo("dequeue Priority Queue", "O(1)")


def cmd_rute(state: StateSimulasi, args: list):
    """
    RUTE <asal> <tujuan>
    Hitung rute optimal menggunakan Dijkstra.
    Big-O: O(VÂ² + E)
    """
    _header("RUTE OPTIMAL â DIJKSTRA")
    if len(args) < 2:
        print("  Penggunaan: RUTE <asal> <tujuan>")
        print("  Contoh    : RUTE Malioboro Prambanan")
        return

    asal   = args[0].capitalize()
    tujuan = args[1].capitalize()

    if not state.bst.ada(asal):
        print(f"  [â] Asal '{asal}' tidak ditemukan di indeks BST.")
        _bigo("Dijkstra", "O(VÂ² + E)")
        return
    if not state.bst.ada(tujuan):
        print(f"  [â] Tujuan '{tujuan}' tidak ditemukan di indeks BST.")
        _bigo("Dijkstra", "O(VÂ² + E)")
        return

    t0    = time.perf_counter()
    hasil = state.dijkstra.jalankan(asal)
    t1    = time.perf_counter()

    jalur = hasil.jalur_ke(tujuan)
    jarak = hasil.jarak_ke(tujuan)

    if not jalur:
        print(f"  [â] Tidak ada rute dari '{asal}' ke '{tujuan}'.")
    else:
        print(f"  Asal   : {asal}")
        print(f"  Tujuan : {tujuan}")
        print(f"  Jarak  : {jarak:.0f} meter ({jarak/1000:.2f} km)")
        print(f"  Jalur  : {' â '.join(jalur)}")
        print(f"  Hop    : {len(jalur)-1} persimpangan")
        print(f"  Waktu  : {(t1-t0)*1000:.2f} ms")
        state.log_event.append({
            "cmd": "RUTE", "asal": asal,
            "tujuan": tujuan, "jarak": jarak
        })

    # Rute alternatif
    print("\n  [>] Rute Alternatif:")
    alts = state.dijkstra.rute_alternatif(asal, tujuan, k=3)
    for i, (j, d) in enumerate(alts, 1):
        print(f"  Opsi {i} ({d:.0f}m): {' â '.join(j)}")

    _bigo("Dijkstra satu sumber", "O(VÂ² + E)")
    _bigo("Rekonstruksi jalur", "O(V)")
    _bigo("BST search", "O(log V)")


def cmd_antrian(state: StateSimulasi, args: list):
    """
    ANTRIAN <persimpangan>
    Tampilkan antrian kendaraan di persimpangan.
    Big-O: O(n)
    """
    _header("ANTRIAN KENDARAAN")
    if not args:
        print("  Penggunaan: ANTRIAN <persimpangan>")
        print("  Contoh    : ANTRIAN Malioboro")
        # Tampilkan ringkasan semua
        sibuk, jml = state.manajer.persimpangan_tersibuk()
        print(f"\n  [i] Total kendaraan: {state.manajer.total_kendaraan()}")
        print(f"  [i] Persimpangan tersibuk: {sibuk} ({jml} kendaraan)")
        _bigo("scan semua antrian", "O(V)")
        return

    persimpangan = args[0].capitalize()
    if persimpangan not in state.manajer.antrian:
        print(f"  [â] Persimpangan '{persimpangan}' tidak ditemukan.")
        _bigo("tampil antrian", "O(n)")
        return

    pq = state.manajer.antrian[persimpangan]
    pq.tampilkan()
    pq.statistik()
    _bigo("tampil antrian", "O(n)")
    _bigo("hitung_per_jenis", "O(n)")


def cmd_laporan(state: StateSimulasi, args: list):
    """
    LAPORAN KEMACETAN
    Tampilkan laporan kemacetan terurut (Selection Sort).
    Big-O: O(nÂ²)
    """
    _header("LAPORAN KEMACETAN")
    laporan = bangun_laporan(state.manajer)

    # Pilih sorting method
    metode = "SELECTION"
    if args and args[0].upper() == "INSERTION":
        metode = "INSERTION"

    lap_terurut = laporan.salin()
    t0 = time.perf_counter()
    if metode == "SELECTION":
        swap = lap_terurut.selection_sort_desc()
        print(f"  [â] Selection Sort: {swap} swap")
    else:
        komp = lap_terurut.insertion_sort_desc()
        print(f"  [â] Insertion Sort: {komp} komparasi")
    t1 = time.perf_counter()
    print(f"  Waktu sorting: {(t1-t0)*1000:.4f} ms")

    lap_terurut.tampilkan(maks=10, judul=f"Laporan Kemacetan ({metode} SORT)")

    # Bottleneck
    btk = identifikasi_bottleneck(lap_terurut)
    if btk:
        print(f"\n  [â ] Bottleneck ({len(btk)} persimpangan kritis):")
        for b in btk:
            print(f"  â   {b}")

    _bigo(f"{metode} Sort pada Linked List", "O(nÂ²)")
    _bigo("identifikasi_bottleneck", "O(n)")


def cmd_siklus_lampu(state: StateSimulasi, args: list):
    """
    SIKLUS_LAMPU <persimpangan> [p=durasi]
    Tampilkan / maju siklus lampu lalu lintas.
    Big-O: O(1) per operasi
    """
    _header("SIKLUS LAMPU LALU LINTAS")
    if not args:
        print("  Penggunaan: SIKLUS_LAMPU <persimpangan> [p=durasi_detik]")
        print("  Contoh    : SIKLUS_LAMPU Malioboro")
        print("  Contoh    : SIKLUS_LAMPU Malioboro p=45")
        print("\n  Status lampu semua persimpangan (5 pertama):")
        for s in state.manajer_lampu.semua_status(maks=5):
            print(f"  {s}")
        _bigo("status lampu", "O(1)")
        return

    persimpangan = args[0].capitalize()
    if persimpangan not in state.manajer_lampu.lampu:
        print(f"  [â] Persimpangan '{persimpangan}' tidak ditemukan.")
        _bigo("siklus lampu", "O(1)")
        return

    lampu = state.manajer_lampu.lampu[persimpangan]

    # Cek parameter durasi
    for arg in args[1:]:
        if arg.startswith("p="):
            try:
                dur = int(arg.split("=")[1])
                lampu.atur_durasi(lampu.fase_sekarang(), dur)
                print(f"  [i] Durasi {lampu.fase_sekarang()} diatur ke {dur}s")
            except ValueError:
                print(f"  [â] Format salah. Gunakan p=<angka>")

    # Maju siklus
    print(f"  Sebelum: {lampu.status()}")
    lampu.maju()
    print(f"  Sesudah: {lampu.status()}")
    print(f"  History stack depth: {len(lampu.history_stack)}")

    _bigo("maju siklus lampu (push stack)", "O(1)")
    _bigo("mundur siklus lampu (pop stack)", "O(1)")


def cmd_isolasi(state: StateSimulasi, _args: list):
    """
    ISOLASI
    Deteksi persimpangan terisolasi dengan DFS.
    Big-O: O(V + E)
    """
    _header("DETEKSI PERSIMPANGAN TERISOLASI â DFS")
    t0       = time.perf_counter()
    terisolasi = state.graf.deteksi_terisolasi()
    komp     = state.graf.komponen_terhubung()
    t1       = time.perf_counter()

    print(f"  [i] Total persimpangan  : {state.graf.jumlah_persimpangan}")
    print(f"  [i] Komponen terhubung  : {len(komp)}")
    print(f"  [i] Waktu DFS           : {(t1-t0)*1000:.4f} ms")

    if terisolasi:
        print(f"\n  [â ] Persimpangan terisolasi ({len(terisolasi)}):")
        for nama in terisolasi:
            print(f"  â   {nama} (degree={state.graf.degree(nama)})")
    else:
        print("\n  [â] Semua persimpangan terhubung â tidak ada yang terisolasi.")

    if len(komp) > 1:
        print("\n  [i] Detail komponen:")
        for i, k in enumerate(komp, 1):
            print(f"  Komponen {i}: {', '.join(k)}")

    _bigo("DFS deteksi terisolasi", "O(V + E)")
    _bigo("komponen_terhubung", "O(V + E)")


def cmd_help(_state, _args):
    """Tampilkan bantuan perintah."""
    _header("BANTUAN PERINTAH CLI")
    perintah = [
        ("MASUK <persimpangan> <jenis>",
         "Tambah kendaraan ke antrian",           "O(n)"),
        ("BERANGKAT <persimpangan>",
         "Keluarkan kendaraan prioritas tertinggi","O(1)"),
        ("RUTE <asal> <tujuan>",
         "Hitung rute optimal (Dijkstra)",         "O(VÂ²+E)"),
        ("ANTRIAN <persimpangan>",
         "Tampilkan antrian kendaraan",            "O(n)"),
        ("LAPORAN [SELECTION|INSERTION]",
         "Laporan kemacetan terurut",              "O(nÂ²)"),
        ("KEMACETAN",
         "Ringkasan kemacetan semua persimpangan", "O(VÂ·n)"),
        ("SIKLUS_LAMPU <persimpangan> [p=dur]",
         "Kelola siklus lampu lalu lintas",        "O(1)"),
        ("ISOLASI",
         "Deteksi persimpangan terisolasi (DFS)",  "O(V+E)"),
        ("SIMULASI [n_event]",
         "Jalankan simulasi otomatis",             "O(nÂ²)"),
        ("BST [nama]",
         "Tampilkan indeks BST persimpangan",      "O(log V)"),
        ("GRAF",
         "Tampilkan graph jaringan jalan",         "O(V+E)"),
        ("LOG [n]",
         "Tampilkan log event terakhir",           "O(n)"),
        ("HELP",
         "Tampilkan bantuan ini",                  "O(1)"),
        ("KELUAR",
         "Keluar dari simulasi",                   "O(1)"),
    ]
    print(f"  {'Perintah':<38} {'Keterangan':<35} {'Big-O'}")
    print("  " + "â"*80)
    for cmd, ket, bigo in perintah:
        print(f"  {cmd:<38} {ket:<35} {bigo}")


def cmd_kemacetan(state: StateSimulasi, _args: list):
    """
    KEMACETAN
    Tampilkan ringkasan kemacetan seluruh persimpangan.
    """
    _header("RINGKASAN KEMACETAN KOTA")
    laporan = bangun_laporan(state.manajer)
    laporan_terurut = laporan.salin()
    laporan_terurut.selection_sort_desc()
    laporan_terurut.tampilkan(maks=10,
                               judul="Kemacetan (Terurut Descending)")
    total = state.manajer.total_kendaraan()
    print(f"\n  Total kendaraan di seluruh kota: {total}")
    sibuk, jml = state.manajer.persimpangan_tersibuk()
    print(f"  Paling macet: {sibuk} ({jml} kendaraan)")
    _bigo("bangun_laporan", "O(VÂ·n)")
    _bigo("selection_sort_desc", "O(nÂ²)")


def cmd_simulasi(state: StateSimulasi, args: list):
    """
    SIMULASI [n_event]
    Jalankan simulasi otomatis sejumlah event.
    """
    _header("SIMULASI OTOMATIS")
    n = 500
    if args:
        try:
            n = int(args[0])
        except ValueError:
            pass

    print(f"  [>] Menjalankan {n} event simulasi ...")
    t0  = time.perf_counter()
    log = simulasi_event(state.manajer, NAMA_PERSIMPANGAN,
                         n_event=n, seed=17)
    t1  = time.perf_counter()
    masuk_c = sum(1 for e in log if e["event"] == "MASUK")
    brgkt_c = sum(1 for e in log if e["event"] == "BERANGKAT")
    print(f"  [â] Selesai dalam {(t1-t0)*1000:.2f} ms")
    print(f"  [i] MASUK: {masuk_c} | BERANGKAT: {brgkt_c}")
    print(f"  [i] Total kendaraan tersisa: {state.manajer.total_kendaraan()}")
    state.log_event.extend(log[:20])
    _bigo("simulasi event", "O(n * antrian)")


def cmd_bst(state: StateSimulasi, args: list):
    """BST â tampilkan indeks BST persimpangan."""
    _header("BST INDEKS PERSIMPANGAN")
    if args:
        nama = args[0].capitalize()
        node = state.bst.search(nama)
        if node:
            print(f"  [â] Ditemukan: {nama}")
            print(f"  Data: {node.data}")
        else:
            print(f"  [â] '{nama}' tidak ada di BST.")
        _bigo("BST search", "O(log V) rata-rata")
    else:
        state.bst.tampilkan_pohon(maks_tinggi=3)
        state.bst.tampilkan_inorder()
        _bigo("BST inorder traversal", "O(V)")


def cmd_graf(state: StateSimulasi, _args: list):
    """GRAF â tampilkan graph jaringan jalan."""
    state.graf.tampilkan_graf(maks_tampil=10)
    _bigo("tampil adjacency list", "O(V + E)")


def cmd_log(state: StateSimulasi, args: list):
    """LOG [n] â tampilkan log event terakhir."""
    _header("LOG EVENT SIMULASI")
    n    = 20
    if args:
        try:
            n = int(args[0])
        except ValueError:
            pass
    log  = state.log_event[-n:]
    if not log:
        print("  (Belum ada event tercatat)")
        return
    for i, e in enumerate(log, 1):
        print(f"  {i:3d}. {e}")
    _bigo("tampil log", "O(n)")


# ââââââââââââââââââââââââââââââââââââââââââââââ
# ROUTER PERINTAH
# ââââââââââââââââââââââââââââââââââââââââââââââ

PERINTAH_MAP = {
    "MASUK"        : cmd_masuk,
    "BERANGKAT"    : cmd_berangkat,
    "RUTE"         : cmd_rute,
    "ANTRIAN"      : cmd_antrian,
    "LAPORAN"      : cmd_laporan,
    "KEMACETAN"    : cmd_kemacetan,
    "SIKLUS_LAMPU" : cmd_siklus_lampu,
    "ISOLASI"      : cmd_isolasi,
    "SIMULASI"     : cmd_simulasi,
    "BST"          : cmd_bst,
    "GRAF"         : cmd_graf,
    "LOG"          : cmd_log,
    "HELP"         : cmd_help,
    "?"            : cmd_help,
}


def proses_perintah(state: StateSimulasi, baris: str):
    """Parse dan eksekusi satu baris perintah."""
    baris = baris.strip()
    if not baris:
        return True

    token   = baris.split()
    cmd     = token[0].upper()
    args    = token[1:]

    if cmd in ("KELUAR", "EXIT", "QUIT", "Q"):
        print("\n  [â] Terima kasih telah menggunakan Smart Traffic CLI!")
        print("  Simulasi selesai. Sampai jumpa! ð¦")
        return False

    handler = PERINTAH_MAP.get(cmd)
    if handler:
        try:
            handler(state, args)
        except Exception as e:
            print(f"  [â] Error eksekusi '{cmd}': {e}")
            import traceback
            traceback.print_exc()
    else:
        print(f"  [â] Perintah '{cmd}' tidak dikenal. Ketik HELP untuk bantuan.")

    return True


# ââââââââââââââââââââââââââââââââââââââââââââââ
# MAIN CLI LOOP
# ââââââââââââââââââââââââââââââââââââââââââââââ

def jalankan_cli():
    """Loop utama CLI interaktif."""
    print("\n" + "â" + "â"*58 + "â")
    print("â" + "  ð¦  SMART TRAFFIC SIMULATION & SIGNAL OPTIMIZATION  " + "  â")
    print("â" + "     ELT60213 Algoritma dan Struktur Data | TA 2025/2026 " + "â")
    print("â" + "     Topik 7 | Seed = 17 | 25 Persimpangan Yogyakarta  " + "â")
    print("â" + "â"*58 + "â")

    state = StateSimulasi()

    print("\n  Ketik HELP untuk daftar perintah. KELUAR untuk keluar.")
    print("  Tip: Coba 'SIMULASI 100' lalu 'LAPORAN' untuk melihat kemacetan.\n")

    while True:
        try:
            baris = input("  TRAFFIC> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  [i] Keluar (Ctrl+C / EOF)")
            break

        lanjut = proses_perintah(state, baris)
        if not lanjut:
            break


# ââââââââââââââââââââââââââââââââââââââââââââââ
# SKENARIO UJI OTOMATIS (non-interaktif)
# ââââââââââââââââââââââââââââââââââââââââââââââ

def skenario_demo():
    """
    Jalankan skenario uji otomatis tanpa input pengguna.
    Berguna untuk demo presentasi.
    """
    print("\n" + "â"*60)
    print("  MODUL 6 â CLI Simulasi (Skenario Demo Otomatis)")
    print("  ELT60213 Algoritma dan Struktur Data | Topik 7")
    print("â"*60)

    state = StateSimulasi()

    perintah_demo = [
        "SIMULASI 300",
        "ANTRIAN Malioboro",
        "MASUK Malioboro AMBULANS",
        "MASUK Malioboro BUS",
        "MASUK Malioboro MOTOR",
        "ANTRIAN Malioboro",
        "BERANGKAT Malioboro",
        "ANTRIAN Malioboro",
        "RUTE Malioboro Prambanan",
        "RUTE Tugu Wonosari",
        "LAPORAN",
        "LAPORAN INSERTION",
        "KEMACETAN",
        "ISOLASI",
        "SIKLUS_LAMPU Malioboro",
        "SIKLUS_LAMPU Malioboro p=60",
        "BST",
        "BST Kraton",
        "GRAF",
        "LOG 5",
    ]

    for perintah in perintah_demo:
        print(f"\n  {'â'*50}")
        print(f"  TRAFFIC> {perintah}")
        lanjut = proses_perintah(state, perintah)
        if not lanjut:
            break


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        skenario_demo()
    else:
        jalankan_cli()