# ─────────────────────────────────────────────
# Node
# ─────────────────────────────────────────────
class Node:
    """Satu simpul dalam Singly Linked List."""
    def __init__(self, data):
        self.data = data
        self.next = None

    def __repr__(self):
        return f"Node({self.data!r})"


# ─────────────────────────────────────────────
# Singly Linked List
# ─────────────────────────────────────────────
class LinkedList:
    """
    Singly Linked List dengan pointer head dan tail.

    Big-O:
        add_front  : O(1)
        add_back   : O(1)
        find       : O(n)
        delete     : O(n)
        to_list    : O(n)
        __len__    : O(1)
        __iter__   : O(n)
    """

    def __init__(self):
        self.head: Node | None = None
        self.tail: Node | None = None
        self._size: int = 0

    # ── Tambah ──────────────────────────────────
    def add_front(self, data) -> None:
        """Tambah node di depan (head). Big-O: O(1)"""
        node = Node(data)
        node.next = self.head
        self.head = node
        if self.tail is None:
            self.tail = node
        self._size += 1

    def add_back(self, data) -> None:
        """Tambah node di belakang (tail). Big-O: O(1)"""
        node = Node(data)
        if self.tail is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self._size += 1

    # ── Cari ────────────────────────────────────
    def find(self, data) -> Node | None:
        """Cari node berdasarkan data. Big-O: O(n)"""
        curr = self.head
        while curr:
            if curr.data == data:
                return curr
            curr = curr.next
        return None

    def contains(self, data) -> bool:
        """Cek apakah data ada. Big-O: O(n)"""
        return self.find(data) is not None

    def get_at(self, index: int):
        """Ambil data di posisi index (0-based). Big-O: O(n)"""
        if index < 0 or index >= self._size:
            raise IndexError(f"Index {index} out of range (size={self._size})")
        curr = self.head
        for _ in range(index):
            curr = curr.next
        return curr.data

    # ── Hapus ────────────────────────────────────
    def delete(self, data) -> bool:
        """
        Hapus node pertama dengan nilai data.
        Big-O: O(n)
        Returns: True jika berhasil, False jika tidak ada.
        """
        if self.head is None:
            return False

        # Hapus head
        if self.head.data == data:
            self.head = self.head.next
            if self.head is None:
                self.tail = None
            self._size -= 1
            return True

        # Hapus node tengah/akhir
        prev, curr = self.head, self.head.next
        while curr:
            if curr.data == data:
                prev.next = curr.next
                if curr == self.tail:
                    self.tail = prev
                self._size -= 1
                return True
            prev, curr = curr, curr.next
        return False

    def delete_front(self):
        """Hapus dan kembalikan node di depan. Big-O: O(1)"""
        if self.head is None:
            return None
        data = self.head.data
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self._size -= 1
        return data

    # ── Konversi ─────────────────────────────────
    def to_list(self) -> list:
        """Konversi ke Python list. Big-O: O(n)"""
        result = []
        curr = self.head
        while curr:
            result.append(curr.data)
            curr = curr.next
        return result

    def clear(self) -> None:
        """Kosongkan linked list. Big-O: O(1)"""
        self.head = self.tail = None
        self._size = 0

    # ── Properti ─────────────────────────────────
    def is_empty(self) -> bool:
        return self._size == 0

    def __len__(self) -> int:
        return self._size

    def __iter__(self):
        curr = self.head
        while curr:
            yield curr.data
            curr = curr.next

    def __repr__(self) -> str:
        items = self.to_list()
        chain = " → ".join(str(x) for x in items[:6])
        if len(items) > 6:
            chain += f" ... (total {len(items)})"
        return f"LinkedList([{chain}])"


# ─────────────────────────────────────────────
# Demo standalone
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("LINKED LIST – Demo")
    print("=" * 50)

    ll = LinkedList()
    for i in [10, 20, 30, 40, 50]:
        ll.add_back(i)
    print(f"Setelah add_back 10–50 : {ll}")
    print(f"Panjang               : {len(ll)}")

    ll.add_front(0)
    print(f"Setelah add_front(0)  : {ll}")

    ll.delete(30)
    print(f"Setelah delete(30)    : {ll}")

    print(f"contains(20)          : {ll.contains(20)}")
    print(f"contains(30)          : {ll.contains(30)}")
    print(f"get_at(0)             : {ll.get_at(0)}")
    print(f"Iterasi               : {[x for x in ll]}")