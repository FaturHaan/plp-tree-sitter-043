import sys
from pathlib import Path
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)

# Query untuk Fitur 1: Komentar TODO atau FIXME
Q_TODO = Query(PY, '((comment) @c (#match? @c "TODO|FIXME"))')

# Query untuk Fitur 2: Definisi fungsi dan namanya
Q_FUNGSI = Query(PY, '(function_definition name: (identifier) @nama) @fungsi')

def cek_file(path: Path):
    try:
        konten_bytes = path.read_bytes()
    except Exception as e:
        print(f"Error membaca file {path}: {e}")
        return

    tree = parser.parse(konten_bytes)

    # ----------------------------------------------------
    # Fitur 1: Deteksi komentar TODO / FIXME
    # ----------------------------------------------------
    todo_nodes = QueryCursor(Q_TODO).captures(tree.root_node).get("c", [])
    for node in sorted(todo_nodes, key=lambda n: n.start_point):
        teks_komentar = node.text.decode(errors="replace").strip()
        print(f"{path}:{node.start_point[0] + 1}: {teks_komentar}")

    # ----------------------------------------------------
    # Fitur 2: Deteksi fungsi lebih dari 30 baris
    # ----------------------------------------------------
    for _, cap in QueryCursor(Q_FUNGSI).matches(tree.root_node):
        fungsi_node = cap["fungsi"][0]
        nama_node = cap["nama"][0]
        nama_fungsi = nama_node.text.decode(errors="replace")
        jumlah_baris = fungsi_node.end_point[0] - fungsi_node.start_point[0] + 1
        
        if jumlah_baris > 30:
            baris_mulai = fungsi_node.start_point[0] + 1
            print(f"{path}:{baris_mulai}: fungsi '{nama_fungsi}' terlalu panjang ({jumlah_baris} baris)")

    # Fitur 3 akan diimplementasikan pada Tahap 9

def main():
    if len(sys.argv) < 2:
        print("Penggunaan: python cek.py <folder>")
        sys.exit(1)

    target_dir = Path(sys.argv[1])
    if not target_dir.exists():
        print(f"Folder tidak ditemukan: {target_dir}")
        sys.exit(1)

    # Direktori yang dilewati saat pengecekan rekursif
    ignored_dirs = {".git", "venv", ".venv", "node_modules", "__pycache__"}

    for path in sorted(target_dir.rglob("*.py")):
        # Lewati file jika berada di dalam folder yang diabaikan
        if any(part in ignored_dirs for part in path.parts):
            continue
        cek_file(path)

if __name__ == "__main__":
    main()
