import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.data_structures.linked_list import LinkedList


# ─────────────────────────────────────────────
# Stack
# ─────────────────────────────────────────────
class Stack:
    """
    Stack LIFO berbasis Linked List.

    Semua operasi O(1) karena add_front/delete_front
    pada LinkedList adalah O(1).

    Big-O:
        push              : O(1)
        pop               : O(1)
        peek              : O(1)
        is_empty          : O(1)
        __len__           : O(1)
        tampilkan_stack   : O(n)
        pindah_ke_linked_list : O(n)
    """

    def __init__(self):
        self._ll = LinkedList()   # head = top of stack

    # ── Operasi Utama ────────────────────────────
    def push(self, item) -> None:
        """
        Masukkan item ke atas stack.
        Big-O: O(1)
        """
        self._ll.add_front(item)

    def pop(self):
        """
        Keluarkan dan kembalikan item dari atas stack.
        Kembalikan None jika stack kosong (tidak raise error).
        Big-O: O(1)
        """
        return self._ll.delete_front()

    def peek(self):
        """
        Lihat item teratas tanpa menghapus.
        Kembalikan None jika kosong.
        Big-O: O(1)
        """
        if self._ll.head is None:
            return None
        return self._ll.head.data

    # ── Tampilan ─────────────────────────────────
    def tampilkan_stack(self) -> list:
        """
        Kembalikan semua isi stack dari atas ke bawah.
        Tidak mengubah isi stack.
        Big-O: O(n)
        """
        return self._ll.to_list()   # head = top, sudah urutan atas→bawah

    # ── Archiving ────────────────────────────────
    def pindah_ke_linked_list(self, maks_simpan: int) -> list:
        """
        Jika ukuran stack > maks_simpan, pindahkan elemen
        TERLAMA (terbawah) ke arsip (list biasa).

        Stack menyisakan maks_simpan elemen teratas.
        Elemen terlama = yang pertama masuk = paling bawah.

        Big-O: O(n)
        Returns: list elemen yang diarsipkan (terlama duluan)
        """
        if len(self._ll) <= maks_simpan:
            return []

        # Ambil semua isi stack
        semua = self._ll.to_list()          # [top, ..., bottom]
        simpan = semua[:maks_simpan]        # maks_simpan teratas
        arsip  = semua[maks_simpan:]        # sisanya → arsip

        # Bangun ulang stack hanya dari elemen yang disimpan
        self._ll.clear()
        for item in reversed(simpan):       # push dari bawah ke atas
            self.push(item)

        return arsip

    # ── Properti ─────────────────────────────────
    def is_empty(self) -> bool:
        return self._ll.is_empty()

    def __len__(self) -> int:
        return len(self._ll)

    def __repr__(self) -> str:
        top5 = self.tampilkan_stack()[:5]
        return (f"Stack(top→bot={top5}"
                f"{'...' if len(self._ll) > 5 else ''}, "
                f"size={len(self._ll)})")


# ─────────────────────────────────────────────
# Demo standalone
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("STACK – Demo")
    print("=" * 50)

    s = Stack()
    for item in ["A", "B", "C", "D"]:
        s.push(item)
        print(f"push({item!r}) → size={len(s)}, peek={s.peek()!r}")

    print(f"\nStack (atas→bawah): {s.tampilkan_stack()}")

    print(f"\npop() → {s.pop()!r}")
    print(f"pop() → {s.pop()!r}")
    print(f"Sisa  : {s.tampilkan_stack()}")

    print(f"\nArchiving (maks_simpan=1):")
    s2 = Stack()
    for i in range(1, 6):
        s2.push(i)
    arsip = s2.pindah_ke_linked_list(maks_simpan=3)
    print(f"  Stack tersisa : {s2.tampilkan_stack()}")
    print(f"  Arsip         : {arsip}")