import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))

# ==========================================
# 1. TIGA POTONGAN KODE VALID + 1 KODE RUSAK
# ==========================================

# Potongan 1: Definisi Fungsi
kode_fungsi = b"""def sapa(nama):
    return nama
"""

# Potongan 2: Percabangan if / else
kode_if_else = b"""if nilai >= 75:
    status = "lulus"
else:
    status = "ulang"
"""

# Potongan 3: Definisi Kelas dengan satu method
kode_class = b"""class Mahasiswa:
    def belajar(self):
        pass
"""

# Potongan 4: Kode rusak (sengaja menghilangkan ':' setelah nama fungsi)
kode_rusak = b"""def sapa(nama)
    return nama
"""

kasus_uji = [
    ("Potongan 1 (Fungsi)", kode_fungsi),
    ("Potongan 2 (If / Else)", kode_if_else),
    ("Potongan 3 (Kelas)", kode_class),
    ("Potongan 4 (Kode Rusak - Error Recovery)", kode_rusak),
]

# ==========================================
# 2. PARSING & CETAK S-EXPRESSION
# ==========================================
for judul, kode in kasus_uji:
    print("=" * 60)
    print(f"--- {judul} ---")
    print("Kode Sumber:")
    print(kode.decode().strip())
    print("-" * 60)
    
    tree = parser.parse(kode)
    print("Hasil S-expression (Root Node):")
    print(tree.root_node)
    
    # Menampilkan node bernama vs anonim untuk child tingkat pertama
    print("\nInspeksi Child Pertama (Membedakan Bernama vs Anonim):")
    if len(tree.root_node.children) > 0:
        first_stmt = tree.root_node.children[0]
        print(f"Statement tipe: {first_stmt.type} (bernama: {first_stmt.is_named})")
        for c in first_stmt.children:
            status = "bernama" if c.is_named else "anonim"
            print(f"  - Node tipe: {c.type:<20} | Status: {status}")
            # Jika ada node parameters, telusuri lebih dalam untuk melihat tanda kurung '(' dan ')'
            if c.type == "parameters":
                for sub_c in c.children:
                    sub_status = "bernama" if sub_c.is_named else "anonim"
                    print(f"      * Sub-node: {sub_c.type:<16} | Status: {sub_status}")
    print()
