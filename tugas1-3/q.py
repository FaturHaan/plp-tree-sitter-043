import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)

if len(sys.argv) < 3:
    print("Penggunaan: python q.py <file.py> <query.scm>")
    sys.exit(1)

kode = open(sys.argv[1], "rb").read()
pola = open(sys.argv[2], encoding="utf-8").read()
tree = parser.parse(kode)
query = Query(PY, pola)

# Jika query menargetkan pasangan nama fungsi & parameter (seperti q_fungsi.scm)
# kita gunakan cursor.matches agar nama dan parameternya berpasangan per fungsi
matches = list(QueryCursor(query).matches(tree.root_node))
has_nama_params = any("nama" in cap and "params" in cap for _, cap in matches)

if has_nama_params:
    print("--- Mode Pasangan (Nama Fungsi & Jumlah Parameter) ---")
    for _, cap in matches:
        nama = cap["nama"][0].text.decode()
        # Jumlah parameter dihitung dari named_child_count di dalam node parameters
        jumlah_params = cap["params"][0].named_child_count
        baris = cap["nama"][0].start_point[0] + 1
        print(f"Fungsi: '{nama:<15}' | Jumlah parameter: {jumlah_params} | Baris: {baris}")
else:
    # Mode umum: mencetak seluruh capture berdasarkan tag @capture_name
    hasil = QueryCursor(query).captures(tree.root_node)
    for nama, nodes in hasil.items():
        for n in nodes:
            teks = n.text.decode(errors="replace").strip().replace("\n", " ")
            print(f"@{nama:<10} baris {n.start_point[0] + 1:<3}: {teks}")
