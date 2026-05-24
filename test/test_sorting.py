# ============================================================
# test/test_sorting.py
# Unit test untuk Sorting Algorithms pada Linked List
# (src/data_structures/sorting.py)
# Jalankan: pytest test/test_sorting.py -v
# ============================================================
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from src.data_structures.sorting import CongestionLinkedList, buat_laporan

# ── helper ────────────────────────────────────────────────────
def buat_ll(*pairs) -> CongestionLinkedList:
    """Buat CongestionLinkedList dari pasangan (nama, count)."""
    ll = CongestionLinkedList()
    for nm, ct in pairs:
        ll.append(nm, ct)
    return ll

def counts(ll: CongestionLinkedList) -> list:
    return [c for _, c in ll.to_list()]

def names(ll: CongestionLinkedList) -> list:
    return [n for n, _ in ll.to_list()]


# ══════════════════════════════════════════════════════════════
# KELOMPOK 1 — CongestionLinkedList dasar
# ══════════════════════════════════════════════════════════════

def test_ll_baru_kosong():
    ll = CongestionLinkedList()
    assert ll.size == 0 and ll.head is None

def test_append_menambah_size():
    ll = buat_ll(("A1",10),("B2",5),("C3",20))
    assert ll.size == 3

def test_to_list_urutan_append():
    ll = buat_ll(("A1",10),("B2",5),("C3",20))
    assert names(ll) == ["A1","B2","C3"]

def test_to_list_mengembalikan_tuple():
    ll = buat_ll(("A1",10))
    items = ll.to_list()
    assert isinstance(items[0], tuple) and len(items[0]) == 2

def test_copy_independen():
    ll1 = buat_ll(("A",5),("B",10))
    ll2 = ll1.copy()
    ll2.append("C", 15)
    assert ll1.size == 2 and ll2.size == 3

def test_len_sama_dengan_size():
    ll = buat_ll(("A",1),("B",2),("C",3))
    assert len(ll) == 3

# ══════════════════════════════════════════════════════════════
# KELOMPOK 2 — Bubble Sort
# ══════════════════════════════════════════════════════════════

def test_bubble_sort_descending():
    ll = buat_ll(("A",3),("B",7),("C",1),("D",5),("E",9))
    ll.bubble_sort(descending=True)
    assert counts(ll) == [9,7,5,3,1]

def test_bubble_sort_ascending():
    ll = buat_ll(("A",3),("B",7),("C",1),("D",5),("E",9))
    ll.bubble_sort(descending=False)
    assert counts(ll) == [1,3,5,7,9]

def test_bubble_sort_nama_ikut_pindah():
    ll = buat_ll(("A",3),("B",7),("C",1))
    ll.bubble_sort(descending=True)
    assert names(ll)[0] == "B"

def test_bubble_sort_sudah_terurut():
    ll = buat_ll(("A",9),("B",7),("C",5))
    ll.bubble_sort(descending=True)
    assert counts(ll) == [9,7,5]

def test_bubble_sort_terbalik():
    ll = buat_ll(("A",1),("B",3),("C",7))
    ll.bubble_sort(descending=True)
    assert counts(ll) == [7,3,1]

def test_bubble_sort_satu_elemen():
    ll = buat_ll(("A",42))
    ll.bubble_sort()
    assert counts(ll) == [42]

def test_bubble_sort_kosong_tidak_crash():
    ll = CongestionLinkedList()
    ll.bubble_sort()   # tidak boleh raise apapun
    assert ll.size == 0

def test_bubble_sort_semua_nilai_sama():
    ll = buat_ll(("A",5),("B",5),("C",5))
    ll.bubble_sort()
    assert counts(ll) == [5,5,5]

# ══════════════════════════════════════════════════════════════
# KELOMPOK 3 — Insertion Sort
# ══════════════════════════════════════════════════════════════

def test_insertion_sort_descending():
    ll = buat_ll(("A",3),("B",7),("C",1),("D",5),("E",9))
    ll.insertion_sort(descending=True)
    assert counts(ll) == [9,7,5,3,1]

def test_insertion_sort_ascending():
    ll = buat_ll(("A",3),("B",7),("C",1),("D",5),("E",9))
    ll.insertion_sort(descending=False)
    assert counts(ll) == [1,3,5,7,9]

def test_insertion_sort_nama_ikut_pindah():
    ll = buat_ll(("A",3),("B",7),("C",1))
    ll.insertion_sort(descending=True)
    assert names(ll)[0] == "B"

def test_insertion_sort_sudah_terurut():
    ll = buat_ll(("A",9),("B",7),("C",5))
    ll.insertion_sort(descending=True)
    assert counts(ll) == [9,7,5]

def test_insertion_sort_terbalik():
    ll = buat_ll(("A",1),("B",3),("C",7))
    ll.insertion_sort(descending=True)
    assert counts(ll) == [7,3,1]

def test_insertion_sort_satu_elemen():
    ll = buat_ll(("A",42))
    ll.insertion_sort()
    assert counts(ll) == [42]

def test_insertion_sort_kosong_tidak_crash():
    ll = CongestionLinkedList()
    ll.insertion_sort()
    assert ll.size == 0

def test_insertion_sort_semua_nilai_sama():
    ll = buat_ll(("A",5),("B",5),("C",5))
    ll.insertion_sort()
    assert counts(ll) == [5,5,5]

# ══════════════════════════════════════════════════════════════
# KELOMPOK 4 — Selection Sort
# ══════════════════════════════════════════════════════════════

def test_selection_sort_descending():
    ll = buat_ll(("A",3),("B",7),("C",1),("D",5),("E",9))
    ll.selection_sort(descending=True)
    assert counts(ll) == [9,7,5,3,1]

def test_selection_sort_ascending():
    ll = buat_ll(("A",3),("B",7),("C",1),("D",5),("E",9))
    ll.selection_sort(descending=False)
    assert counts(ll) == [1,3,5,7,9]

def test_selection_sort_nama_ikut_pindah():
    ll = buat_ll(("A",3),("B",7),("C",1))
    ll.selection_sort(descending=True)
    assert names(ll)[0] == "B"

def test_selection_sort_sudah_terurut():
    ll = buat_ll(("A",9),("B",7),("C",5))
    ll.selection_sort(descending=True)
    assert counts(ll) == [9,7,5]

def test_selection_sort_terbalik():
    ll = buat_ll(("A",1),("B",3),("C",7))
    ll.selection_sort(descending=True)
    assert counts(ll) == [7,3,1]

def test_selection_sort_satu_elemen():
    ll = buat_ll(("A",42))
    ll.selection_sort()
    assert counts(ll) == [42]

def test_selection_sort_kosong_tidak_crash():
    ll = CongestionLinkedList()
    ll.selection_sort()
    assert ll.size == 0

def test_selection_sort_semua_nilai_sama():
    ll = buat_ll(("A",5),("B",5),("C",5))
    ll.selection_sort()
    assert counts(ll) == [5,5,5]

# ══════════════════════════════════════════════════════════════
# KELOMPOK 5 — Konsistensi ketiga algoritma
# ══════════════════════════════════════════════════════════════

def test_ketiga_sort_hasil_nilai_sama_descending():
    import random; random.seed(17)
    pairs = [(f"P{i}", random.randint(0,100)) for i in range(20)]

    ll_b = CongestionLinkedList()
    ll_i = CongestionLinkedList()
    ll_s = CongestionLinkedList()
    for nm, ct in pairs:
        ll_b.append(nm, ct)
        ll_i.append(nm, ct)
        ll_s.append(nm, ct)

    ll_b.bubble_sort(descending=True)
    ll_i.insertion_sort(descending=True)
    ll_s.selection_sort(descending=True)

    assert counts(ll_b) == counts(ll_i) == counts(ll_s)

def test_ketiga_sort_hasil_nilai_sama_ascending():
    import random; random.seed(17)
    pairs = [(f"P{i}", random.randint(0,100)) for i in range(20)]

    ll_b = CongestionLinkedList()
    ll_i = CongestionLinkedList()
    ll_s = CongestionLinkedList()
    for nm, ct in pairs:
        ll_b.append(nm, ct); ll_i.append(nm, ct); ll_s.append(nm, ct)

    ll_b.bubble_sort(descending=False)
    ll_i.insertion_sort(descending=False)
    ll_s.selection_sort(descending=False)

    assert counts(ll_b) == counts(ll_i) == counts(ll_s)

def test_tidak_ada_elemen_hilang_setelah_sort():
    import random; random.seed(42)
    pairs = [(f"X{i}", random.randint(1,50)) for i in range(15)]
    original_counts = sorted([ct for _,ct in pairs])

    ll = CongestionLinkedList()
    for nm, ct in pairs: ll.append(nm, ct)
    ll.bubble_sort(descending=False)
    assert sorted(counts(ll)) == original_counts

def test_sort_copy_tidak_mengubah_original():
    ll_orig = buat_ll(("A",3),("B",7),("C",1))
    ll_copy = ll_orig.copy()
    ll_copy.bubble_sort()
    # original tidak berubah
    assert counts(ll_orig) == [3,7,1]

# ══════════════════════════════════════════════════════════════
# KELOMPOK 6 — buat_laporan & skenario simulasi
# ══════════════════════════════════════════════════════════════

def test_buat_laporan_jumlah_node_benar():
    names_list = ["A1","B2","C3","D4","E5"]
    ll = buat_laporan(names_list, seed=17)
    assert ll.size == 5

def test_buat_laporan_deterministik_seed_sama():
    names_list = ["A1","B2","C3"]
    ll1 = buat_laporan(names_list, seed=17)
    ll2 = buat_laporan(names_list, seed=17)
    assert counts(ll1) == counts(ll2)

def test_buat_laporan_dengan_counts_manual():
    manual = {"A1":10, "B2":5, "C3":20}
    ll = buat_laporan(["A1","B2","C3"], counts=manual, seed=17)
    items = dict(ll.to_list())
    assert items["A1"] == 10 and items["B2"] == 5 and items["C3"] == 20

def test_skenario_identifikasi_bottleneck():
    """Top-1 setelah sort descending = persimpangan paling macet."""
    ll = buat_ll(("A1",5),("B2",30),("C3",12),("D4",25),("E5",8))
    ll.selection_sort(descending=True)
    top1_name, top1_count = ll.to_list()[0]
    assert top1_name == "B2" and top1_count == 30

def test_500_elemen_bubble_sort_terurut():
    """Beban 500 node: hasil harus terurut descending."""
    import random; random.seed(17)
    pairs = [(f"N{i}", random.randint(0,500)) for i in range(500)]
    ll = CongestionLinkedList()
    for nm, ct in pairs: ll.append(nm, ct)
    ll.bubble_sort(descending=True)
    result = counts(ll)
    assert result == sorted(result, reverse=True)

def test_500_elemen_selection_sort_terurut():
    import random; random.seed(17)
    pairs = [(f"N{i}", random.randint(0,500)) for i in range(500)]
    ll = CongestionLinkedList()
    for nm, ct in pairs: ll.append(nm, ct)
    ll.selection_sort(descending=False)
    result = counts(ll)
    assert result == sorted(result)