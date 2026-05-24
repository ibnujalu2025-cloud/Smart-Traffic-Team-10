"""
src/data_model.py
═══════════════════════════════════════════════════════
Data Model — Definisi Struktur Data Kendaraan & Sistem
ELT60213 Algoritma dan Struktur Data | Topik 7
═══════════════════════════════════════════════════════

Berisi semua dataclass dan konstanta yang digunakan
bersama oleh semua modul (1–6).

Tidak menggunakan library dataclass bawaan Python —
semua didefinisikan manual agar konsisten dengan
prinsip implementasi dari nol.
"""

import time

# ─────────────────────────────────────────────
# Konstanta Global
# ─────────────────────────────────────────────

SEED = 17  # JANGAN diubah — seed deterministik Topik 7

VEHICLE_PRIORITY = {
    "AMBULANS": 1,
    "BUS":      2,
    "MOBIL":    3,
    "MOTOR":    4,
}

VEHICLE_TYPES = list(VEHICLE_PRIORITY.keys())

# Jumlah persimpangan dan segmen jalan (parameter sistem)
JUMLAH_PERSIMPANGAN = 25
JUMLAH_EDGE_TARGET  = 40   # ~40 segmen jalan undirected

# Siklus lampu default (detik)
SIKLUS_LAMPU_DEFAULT = 30
SIKLUS_LAMPU_MIN     = 20
SIKLUS_LAMPU_MAX     = 120

# Status kemacetan
STATUS_MACET  = "MACET"   # antrian > 15
STATUS_RAMAI  = "RAMAI"   # antrian > 7
STATUS_NORMAL = "NORMAL"  # antrian <= 7


# ─────────────────────────────────────────────
# Model: Kendaraan
# ─────────────────────────────────────────────
class Kendaraan:
    """
    Representasi satu kendaraan dalam simulasi.

    Attributes:
        vehicle_id   : ID unik otomatis
        vehicle_type : AMBULANS | BUS | MOBIL | MOTOR
        priority     : 1 (tertinggi) – 4 (terendah)
        origin       : persimpangan asal
        destination  : persimpangan tujuan
        arrival_time : waktu masuk antrian (untuk tie-break FIFO)
    """
    _counter = 0

    def __init__(self, vehicle_type: str, origin: str,
                 destination: str, arrival_time: float = None):
        Kendaraan._counter += 1
        self.vehicle_id   = Kendaraan._counter
        self.vehicle_type = vehicle_type.upper()
        self.priority     = VEHICLE_PRIORITY.get(self.vehicle_type, 99)
        self.origin       = origin
        self.destination  = destination
        self.arrival_time = arrival_time if arrival_time is not None else time.time()

    def __repr__(self):
        return (f"Kendaraan(id={self.vehicle_id}, "
                f"type={self.vehicle_type}, "
                f"prio={self.priority}, "
                f"{self.origin}→{self.destination})")


# ─────────────────────────────────────────────
# Model: Persimpangan
# ─────────────────────────────────────────────
class Persimpangan:
    """
    Representasi satu persimpangan dalam jaringan.

    Attributes:
        nama         : identifier unik (contoh: "A1", "C3")
        degree       : jumlah jalan yang terhubung
        antrian      : jumlah kendaraan saat ini
        siklus_lampu : durasi lampu hijau (detik)
        status       : NORMAL | RAMAI | MACET
    """

    def __init__(self, nama: str, degree: int = 0):
        self.nama         = nama
        self.degree       = degree
        self.antrian      = 0
        self.siklus_lampu = SIKLUS_LAMPU_DEFAULT
        self.status       = STATUS_NORMAL

    def update_status(self) -> None:
        """Update status kemacetan berdasarkan jumlah antrian."""
        if self.antrian > 15:
            self.status = STATUS_MACET
        elif self.antrian > 7:
            self.status = STATUS_RAMAI
        else:
            self.status = STATUS_NORMAL

    def update_siklus_lampu(self) -> None:
        """
        Hitung siklus lampu optimal.
        Formula: 20 + (antrian × 2), max 120 detik.
        """
        self.siklus_lampu = min(
            SIKLUS_LAMPU_MIN + self.antrian * 2,
            SIKLUS_LAMPU_MAX
        )

    def __repr__(self):
        return (f"Persimpangan({self.nama}, "
                f"degree={self.degree}, "
                f"antrian={self.antrian}, "
                f"status={self.status})")


# ─────────────────────────────────────────────
# Model: Segmen Jalan
# ─────────────────────────────────────────────
class SegmenJalan:
    """
    Representasi satu segmen jalan (edge) dalam graf.

    Attributes:
        asal      : persimpangan asal
        tujuan    : persimpangan tujuan
        jarak     : bobot jarak dalam meter
        dua_arah  : True = undirected
    """

    def __init__(self, asal: str, tujuan: str,
                 jarak: float, dua_arah: bool = True):
        self.asal     = asal
        self.tujuan   = tujuan
        self.jarak    = jarak
        self.dua_arah = dua_arah

    def __repr__(self):
        arrow = "↔" if self.dua_arah else "→"
        return f"Jalan({self.asal}{arrow}{self.tujuan}, {self.jarak}m)"


# ─────────────────────────────────────────────
# Model: Hasil Rute
# ─────────────────────────────────────────────
class HasilRute:
    """
    Hasil pencarian rute Dijkstra.

    Attributes:
        asal    : persimpangan asal
        tujuan  : persimpangan tujuan
        jarak   : total jarak minimum (meter)
        jalur   : list persimpangan yang dilalui
        alternatif : True jika ini rute alternatif (hindari macet)
    """

    def __init__(self, asal: str, tujuan: str,
                 jarak: float, jalur: list,
                 alternatif: bool = False):
        self.asal        = asal
        self.tujuan      = tujuan
        self.jarak       = jarak
        self.jalur       = jalur
        self.alternatif  = alternatif

    @property
    def terjangkau(self) -> bool:
        return self.jarak < float("inf")

    @property
    def hop(self) -> int:
        return len(self.jalur) - 1 if self.jalur else 0

    def __repr__(self):
        if self.terjangkau:
            return (f"Rute({self.asal}→{self.tujuan}, "
                    f"{self.jarak:.0f}m, {self.hop} hop)")
        return f"Rute({self.asal}→{self.tujuan}, tidak terjangkau)"


# ─────────────────────────────────────────────
# Model: Event Simulasi
# ─────────────────────────────────────────────
class EventSimulasi:
    """
    Satu event dalam log simulasi.

    Attributes:
        nomor      : nomor urut event
        tipe       : MASUK | BERANGKAT | RUTE | SIKLUS
        persimpangan: persimpangan yang terlibat
        kendaraan  : objek Kendaraan (opsional)
        keterangan : deskripsi event
    """

    def __init__(self, nomor: int, tipe: str,
                 persimpangan: str,
                 kendaraan: Kendaraan = None,
                 keterangan: str = ""):
        self.nomor         = nomor
        self.tipe          = tipe
        self.persimpangan  = persimpangan
        self.kendaraan     = kendaraan
        self.keterangan    = keterangan
        self.timestamp     = time.time()

    def __repr__(self):
        k = f" [{self.kendaraan.vehicle_type}]" if self.kendaraan else ""
        return f"Event({self.nomor}, {self.tipe}, {self.persimpangan}{k})"


# ─────────────────────────────────────────────
# Model: Statistik Simulasi
# ─────────────────────────────────────────────
class StatistikSimulasi:
    """Akumulator statistik hasil simulasi."""

    def __init__(self):
        self.total_event      = 0
        self.total_masuk      = 0
        self.total_berangkat  = 0
        self.total_ambulans   = 0
        self.total_rute       = 0
        self.log_event: list  = []

    def catat_masuk(self, kendaraan: Kendaraan) -> None:
        self.total_masuk += 1
        self.total_event += 1
        if kendaraan.vehicle_type == "AMBULANS":
            self.total_ambulans += 1

    def catat_berangkat(self) -> None:
        self.total_berangkat += 1
        self.total_event += 1

    def catat_rute(self) -> None:
        self.total_rute += 1

    def ringkasan(self) -> dict:
        return {
            "total_event"     : self.total_event,
            "total_masuk"     : self.total_masuk,
            "total_berangkat" : self.total_berangkat,
            "total_ambulans"  : self.total_ambulans,
            "total_rute"      : self.total_rute,
        }

    def __repr__(self):
        return (f"Statistik(event={self.total_event}, "
                f"masuk={self.total_masuk}, "
                f"berangkat={self.total_berangkat})")


# ─────────────────────────────────────────────
# Demo standalone
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("DATA MODEL – Demo")
    print("=" * 50)

    k = Kendaraan("AMBULANS", "A1", "E5")
    print(f"Kendaraan  : {k}")

    p = Persimpangan("B3", degree=3)
    p.antrian = 18
    p.update_status()
    p.update_siklus_lampu()
    print(f"Persimpangan: {p}")
    print(f"Siklus lampu: {p.siklus_lampu}s")

    j = SegmenJalan("A1", "B2", 350)
    print(f"Jalan      : {j}")

    r = HasilRute("A1", "E5", 2130, ["A1","B1","C1","D1","E1","E5"])
    print(f"Rute       : {r}")
    print(f"Terjangkau : {r.terjangkau}, Hop: {r.hop}")