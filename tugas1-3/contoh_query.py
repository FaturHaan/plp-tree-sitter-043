import os
import sys
from pathlib import Path
from math import sqrt, pi

def halo():
    print("Halo, dunia!")

def tambah(a, b):
    print("Menghitung penjumlahan...")
    return a + b

def cetak_profil(nama, umur, kota="Jakarta"):
    pesan = f"{nama} berumur {umur} tinggal di {kota}"
    print(pesan)
    return pesan

if __name__ == "__main__":
    halo()
    tambah(10, 20)
    cetak_profil("Budi", 20)
