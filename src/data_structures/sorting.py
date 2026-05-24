import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))


# ─────────────────────────────────────────────
# Node kemacetan
# ─────────────────────────────────────────────
class CongestionNode:
    """Node Linked List untuk data kemacetan."""
    def __init__(self, intersection: str, vehicle_count: int):
        self.intersection  = intersection
        self.vehicle_count = vehicle_count
        self.next          = None

    def __repr__(self):
        return f"({self.intersection}:{self.vehicle_count})"


# ─────────────────────────────────────────────
# CongestionLinkedList + 3 algoritma sort
# ─────────────────────────────────────────────
class CongestionLinkedList:
    """
    Linked List laporan kemacetan dengan tiga algoritma sort.

    Semua sort menggunakan swap DATA (bukan pointer)
    sehingga struktur pointer tetap valid.

    Big-O:
        append         : O(n)
        bubble_sort    : O(n²)
        insertion_sort : O(n²) worst / O(n) best
        selection_sort : O(n²) — O(n) swap
        to_list        : O(n)
        copy           : O(n)
    """

    def __init__(self):
        self.head: CongestionNode | None = None
        self._size: int = 0

    # ── Tambah ──────────────────────────────────
    def append(self, intersection: str, vehicle_count: int) -> None:
        """Tambah node di akhir. Big-O: O(n)"""
        node = CongestionNode(intersection, vehicle_count)
        if self.head is None:
            self.head = node
        else:
            curr = self.head
            while curr.next:
                curr = curr.next
            curr.next = node
        self._size += 1

    # ── Utilitas ─────────────────────────────────
    def to_list(self) -> list:
        """Konversi ke Python list of tuple. Big-O: O(n)"""
        result, curr = [], self.head
        while curr:
            result.append((curr.intersection, curr.vehicle_count))
            curr = curr.next
        return result

    def copy(self) -> "CongestionLinkedList":
        """Salin linked list. Big-O: O(n)"""
        new = CongestionLinkedList()
        curr = self.head
        while curr:
            new.append(curr.intersection, curr.vehicle_count)
            curr = curr.next
        return new

    @property
    def size(self) -> int:
        return self._size

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        items = self.to_list()
        sample = ", ".join(f"{i}:{c}" for i,c in items[:4])
        return f"CongestionLL([{sample}{'...' if self._size > 4 else ''}])"

    # ── Helper swap ──────────────────────────────
    @staticmethod
    def _swap_data(a: CongestionNode, b: CongestionNode) -> None:
        """Tukar DATA dua node (bukan pointer)."""
        a.intersection,  b.intersection  = b.intersection,  a.intersection
        a.vehicle_count, b.vehicle_count = b.vehicle_count, a.vehicle_count

    # ══════════════════════════════════════════
    # BUBBLE SORT — O(n²) stable
    # ══════════════════════════════════════════
    def bubble_sort(self, descending: bool = True) -> None:
        """
        Bubble Sort in-place pada Linked List.

        Cara kerja:
        - Bandingkan pasangan berurutan, swap jika salah urutan
        - Ulangi n-1 kali (tiap pass, elemen terbesar/terkecil
          "gelembung" ke posisi akhir bagian yang belum terurut)
        - Optimasi early-exit: jika satu pass tanpa swap → selesai

        Big-O: O(n²) worst/avg | O(n) best (sudah terurut)
        Stable: Ya
        """
        if self.head is None:
            return

        ada_swap = True
        while ada_swap:
            ada_swap = False
            curr = self.head
            while curr.next:
                kondisi = (
                    curr.vehicle_count < curr.next.vehicle_count
                    if descending else
                    curr.vehicle_count > curr.next.vehicle_count
                )
                if kondisi:
                    self._swap_data(curr, curr.next)
                    ada_swap = True
                curr = curr.next

    # ══════════════════════════════════════════
    # INSERTION SORT — O(n²) worst / O(n) best
    # ══════════════════════════════════════════
    def insertion_sort(self, descending: bool = True) -> None:
        """
        Insertion Sort in-place pada Linked List.

        Cara kerja:
        - Bagian kiri sudah terurut, bagian kanan belum
        - Ambil elemen kanan, sisipkan ke posisi tepat di kiri
        - Implementasi via swap data (lebih mudah pada LL)

        Big-O: O(n²) worst | O(n) best (hampir terurut)
        """
        if self.head is None:
            return

        sorted_end = self.head
        while sorted_end.next:
            key_node = sorted_end.next
            key_int  = key_node.intersection
            key_val  = key_node.vehicle_count

            curr = self.head
            while curr != key_node:
                harus_sisip = (
                    key_val > curr.vehicle_count if descending
                    else key_val < curr.vehicle_count
                )
                if harus_sisip:
                    # Geser elemen curr ke kanan satu slot via swap berantai
                    tmp_i, tmp_v = curr.intersection, curr.vehicle_count
                    curr.intersection  = key_int
                    curr.vehicle_count = key_val
                    key_int, key_val   = tmp_i, tmp_v
                curr = curr.next

            key_node.intersection  = key_int
            key_node.vehicle_count = key_val
            sorted_end = sorted_end.next

    # ══════════════════════════════════════════
    # SELECTION SORT — O(n²), O(n) swap
    # ══════════════════════════════════════════
    def selection_sort(self, descending: bool = True) -> None:
        """
        Selection Sort in-place pada Linked List.

        Cara kerja:
        - Cari elemen terbesar/terkecil dari sisa list
        - Swap ke posisi awal bagian yang belum terurut
        - Jumlah swap = O(n), jauh lebih sedikit dari Bubble Sort

        Big-O: O(n²) selalu (tidak adaptif)
        Swap  : O(n) — keunggulan dibanding Bubble Sort
        """
        if self.head is None:
            return

        outer = self.head
        while outer:
            best  = outer
            inner = outer.next
            while inner:
                kondisi = (
                    inner.vehicle_count > best.vehicle_count if descending
                    else inner.vehicle_count < best.vehicle_count
                )
                if kondisi:
                    best = inner
                inner = inner.next
            if best != outer:
                self._swap_data(outer, best)
            outer = outer.next


# ─────────────────────────────────────────────
# Fungsi helper untuk pipeline
# ─────────────────────────────────────────────
def buat_laporan(names: list, counts: dict = None,
                 seed: int = 17) -> CongestionLinkedList:
    """Bangun CongestionLinkedList dari data atau random."""
    import random
    random.seed(seed)
    ll = CongestionLinkedList()
    for name in names:
        count = counts.get(name, 0) if counts else random.randint(0, 50)
        ll.append(name, count)
    return ll


def eksperimen_runtime(sizes=(10, 25, 100)) -> None:
    """Bandingkan runtime ketiga sort untuk berbagai N."""
    import random
    print(f"\n{'='*65}")
    print("EKSPERIMEN RUNTIME SORTING")
    print(f"{'='*65}")
    print(f"{'N':<8} {'Bubble(s)':<16} {'Insertion(s)':<16} {'Selection(s)'}")
    print(f"{'-'*65}")

    for n in sizes:
        random.seed(17)
        pairs = [(f"P{i}", random.randint(0, 100)) for i in range(n)]

        results = {}
        for algo in ["bubble", "insertion", "selection"]:
            ll = CongestionLinkedList()
            for nm, ct in pairs:
                ll.append(nm, ct)
            t0 = time.perf_counter()
            if algo == "bubble":
                ll.bubble_sort()
            elif algo == "insertion":
                ll.insertion_sort()
            else:
                ll.selection_sort()
            results[algo] = time.perf_counter() - t0

        print(f"{n:<8} {results['bubble']:<16.6f} "
              f"{results['insertion']:<16.6f} {results['selection']:.6f}")

    print(f"{'='*65}")
    print("Big-O: Bubble O(n²) stable | Insertion O(n²)/O(n)* | Selection O(n²)")


# ─────────────────────────────────────────────
# Demo standalone
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("SORTING – Demo (Bubble, Insertion, Selection)")
    print("=" * 55)

    data = [("A1",15),("B2",3),("C3",27),("D4",8),("E5",42)]

    for algo_name, algo_fn in [
        ("Bubble Sort",    lambda ll: ll.bubble_sort()),
        ("Insertion Sort", lambda ll: ll.insertion_sort()),
        ("Selection Sort", lambda ll: ll.selection_sort()),
    ]:
        ll = CongestionLinkedList()
        for nm, ct in data:
            ll.append(nm, ct)
        algo_fn(ll)
        print(f"{algo_name:20}: {ll.to_list()}")

    eksperimen_runtime()
    