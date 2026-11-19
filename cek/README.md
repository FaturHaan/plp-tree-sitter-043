# Code Quality & Error Checker CLI (`cek.py`)

Tool baris perintah (CLI) berbasis **Tree-sitter** untuk menganalisis kualitas kode dan memeriksa integritas sintaks pada proyek Python.

Tool ini melakukan inspeksi Concrete Syntax Tree (CST) secara deterministik dan cepat tanpa perlu mengeksekusi (*run*) kode sumber target.

---

## Fitur Utama

1. **Deteksi Komentar Instruksi (`TODO` / `FIXME`):**  
   Mencari setiap komentar yang memuat penanda pekerjaan tertunda (`TODO` atau `FIXME`) menggunakan pencocokan pola query deklaratif dan predikat `#match?`.
2. **Pendeteksi Fungsi Terlalu Panjang (> 30 baris):**  
   Menghitung rentang baris (`end_point - start_point + 1`) dari setiap definisi fungsi (`function_definition`) dan melaporkan fungsi yang melebihi ambang batas 30 baris.
3. **Pendeteksi Syntax Error (`has_error`):**  
   Mendeteksi file yang pohon sintaksnya tidak valid (mengandung node `ERROR` atau `MISSING`) akibat kesalahan pengetikan atau kode rusak.

---

## Prasyarat & Instalasi

Pastikan Python 3.10+ sudah terpasang. Pasang dependensi parser Tree-sitter:

```bash
pip install tree-sitter tree-sitter-python
```

---

## Cara Menjalankan

Jalankan skrip `cek.py` dengan memberikan path direktori target yang ingin diperiksa:

```bash
python cek.py <path_ke_folder>
```

Contoh jika dijalankan dari root proyek:

```bash
python cek/cek.py cek/uji/
```

Atau memeriksa repositori Python lain:

```bash
python cek/cek.py /path/ke/proyek-python/
```

> **Catatan Filter Folder:**  
> Tool ini secara otomatis mengabaikan folder non-kode sumber umum seperti `.git/`, `venv/`, `.venv/`, `__pycache__/`, dan `node_modules/`.

---

## Contoh Output

### 1. Pengecekan pada Folder Pengujian Lokal (`cek/uji/`):

```text
cek\uji\ada_todo.py:4: # TODO: tambahkan validasi tipe data sebelum proses
cek\uji\ada_todo.py:6: # FIXME: perbaiki penanganan nilai kosong/None
cek\uji\fungsi_panjang.py:7: fungsi 'fungsi_sangat_panjang' terlalu panjang (33 baris)
cek\uji\kode_rusak.py:3: syntax error ditemukan
```

### 2. Pengecekan pada Repositori Open-Source Nyata (`docopt`):

```text
docopt\docopt.py:455: # FIXME corner case "bla: options: --foo"
docopt\docopt.py:301: fungsi 'parse_long' terlalu panjang (31 baris)
docopt\docopt.py:334: fungsi 'parse_shorts' terlalu panjang (33 baris)
docopt\docopt.py:490: fungsi 'docopt' terlalu panjang (92 baris)
docopt\test_docopt.py:387: # "--" is not allowed; FIXME?
docopt\test_docopt.py:103: fungsi 'test_parse_pattern' terlalu panjang (40 baris)
docopt\test_docopt.py:391: fungsi 'test_docopt' terlalu panjang (37 baris)
```

---

## Catatan Perilaku Analisis

- **Fungsi Bersarang & Method Kelas:**  
  Pencarian fungsi menggunakan query `(function_definition)` menangkap seluruh level fungsi, termasuk fungsi lokal di dalam fungsi lain (*nested function*) maupun *method* di dalam sebuah kelas. Seluruhnya dihitung berdasarkan batas baris masing-masing.
- **Toleransi Encoding:**  
  Pembacaan teks menggunakan penanganan `errors="replace"` sehingga aman dari kendala `UnicodeDecodeError` saat memindai file dengan karakter khusus.
