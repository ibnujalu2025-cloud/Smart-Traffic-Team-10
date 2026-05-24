# ============================================================
# tests/test_bst.py
# Unit test untuk BST Indeks Persimpangan
# (modul4_bst/bst.py)
# Jalankan: pytest tests/test_bst.py -v
# ============================================================
import sys
import os

sys.path.insert(
    0,
    os.path.join(os.path.dirname(__file__), "..", "src")
)

from data_structures.graph import build_traffic_graph
from data_structures.bst import IntersectionBST, build_intersection_bst

# ── helper ────────────────────────────────────────────────────
def buat_bst(*keys):
    bst = IntersectionBST()
    for k in keys: bst.insert(k)
    return bst

# ══════════════════════════════════════════════════════════════
# KELOMPOK 1 — insert & size
# ══════════════════════════════════════════════════════════════
def test_bst_baru_kosong():
    bst = IntersectionBST()
    assert bst.is_empty() and bst.size == 0

def test_insert_satu_node():
    bst = IntersectionBST()
    bst.insert("C3")
    assert bst.size == 1 and not bst.is_empty()

def test_insert_tiga_node():
    bst = buat_bst("C3","A1","E5")
    assert bst.size == 3

def test_insert_duplikat_tidak_tambah_size():
    bst = buat_bst("C3","A1","E5")
    bst.insert("C3")
    assert bst.size == 3

def test_insert_dengan_data():
    bst = IntersectionBST()
    bst.insert("B2", {"degree": 4})
    node = bst.search("B2")
    assert node.data.get("degree") == 4

def test_insert_duplikat_update_data():
    bst = IntersectionBST()
    bst.insert("B2", {"degree": 4})
    bst.insert("B2", {"traffic": 10})
    node = bst.search("B2")
    assert node.data.get("traffic") == 10
    assert node.data.get("degree") == 4

# ══════════════════════════════════════════════════════════════
# KELOMPOK 2 — search & contains
# ══════════════════════════════════════════════════════════════
def test_search_node_ada():
    bst = buat_bst("C3","A1","E5","B2","D4")
    node = bst.search("B2")
    assert node is not None and node.key == "B2"

def test_search_node_tidak_ada_return_none():
    bst = buat_bst("C3","A1","E5")
    assert bst.search("ZZ") is None

def test_search_di_bst_kosong_return_none():
    assert IntersectionBST().search("X") is None

def test_contains_benar():
    bst = buat_bst("C3","A1","E5")
    assert bst.contains("A1") is True
    assert bst.contains("ZZ") is False

# ══════════════════════════════════════════════════════════════
# KELOMPOK 3 — inorder terurut
# ══════════════════════════════════════════════════════════════
def test_inorder_terurut_alfabet():
    keys = ["C3","A1","E5","B2","D4"]
    bst = buat_bst(*keys)
    result = [k for k,_ in bst.inorder()]
    assert result == sorted(keys)

def test_inorder_bst_kosong():
    assert IntersectionBST().inorder() == []

def test_inorder_satu_node():
    bst = buat_bst("X")
    assert [k for k,_ in bst.inorder()] == ["X"]

def test_preorder_root_duluan():
    bst = buat_bst("C","A","E")
    assert bst.preorder()[0] == "C"

# ══════════════════════════════════════════════════════════════
# KELOMPOK 4 — delete
# ══════════════════════════════════════════════════════════════
def test_delete_node_daun():
    bst = buat_bst("C","A","E","B","D")
    assert bst.delete("B") is True
    assert not bst.contains("B") and bst.size == 4

def test_delete_inorder_tetap_terurut_setelah_hapus_daun():
    bst = buat_bst("C","A","E","B","D")
    bst.delete("B")
    assert [k for k,_ in bst.inorder()] == ["A","C","D","E"]

def test_delete_node_dua_anak():
    bst = buat_bst("C","A","E","B","D","F")
    bst.delete("C")
    assert not bst.contains("C")
    assert [k for k,_ in bst.inorder()] == sorted(["A","B","D","E","F"])

def test_delete_key_tidak_ada_return_false():
    bst = buat_bst("A","B")
    assert bst.delete("ZZZ") is False

def test_delete_bst_kosong_return_false():
    assert IntersectionBST().delete("X") is False

# ══════════════════════════════════════════════════════════════
# KELOMPOK 5 — range_query
# ══════════════════════════════════════════════════════════════
def test_range_query_benar():
    bst = buat_bst("A1","A2","B1","B2","C1","C2","D1","D2")
    result = [k for k,_ in bst.range_query("B1","C2")]
    assert result == ["B1","B2","C1","C2"]

def test_range_query_satu_elemen():
    bst = buat_bst("A1","B2","C3")
    result = [k for k,_ in bst.range_query("A1","A1")]
    assert result == ["A1"]

def test_range_query_tidak_ada_return_kosong():
    bst = buat_bst("A1","B2","C3")
    assert bst.range_query("Z1","Z9") == []

# ══════════════════════════════════════════════════════════════
# KELOMPOK 6 — height, min, max
# ══════════════════════════════════════════════════════════════
def test_height_bst_kosong():
    assert IntersectionBST().height() == 0

def test_height_satu_node():
    assert buat_bst("C").height() == 1

def test_height_tiga_node_seimbang():
    assert buat_bst("C","A","E").height() == 2

def test_min_key_benar():
    assert buat_bst("C3","A1","E5","B2","D4").min_key() == "A1"

def test_max_key_benar():
    assert buat_bst("C3","A1","E5","B2","D4").max_key() == "E5"

def test_min_max_bst_kosong_return_none():
    bst = IntersectionBST()
    assert bst.min_key() is None and bst.max_key() is None

# ══════════════════════════════════════════════════════════════
# KELOMPOK 7 — build_intersection_bst dengan graf Topik 7
# ══════════════════════════════════════════════════════════════
def test_bst_size_25():
    g = build_traffic_graph(17)
    assert build_intersection_bst(g).size == 25

def test_bst_berisi_a1_dan_e5():
    g = build_traffic_graph(17)
    bst = build_intersection_bst(g)
    assert bst.contains("A1") and bst.contains("E5")

def test_bst_inorder_terurut_25_node():
    g = build_traffic_graph(17)
    bst = build_intersection_bst(g)
    keys = [k for k,_ in bst.inorder()]
    assert keys == sorted(keys) and len(keys) == 25

def test_bst_data_degree_tersimpan():
    g = build_traffic_graph(17)
    bst = build_intersection_bst(g)
    node = bst.search("A1")
    assert "degree" in node.data and node.data["degree"] > 0