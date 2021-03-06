# -*- coding: utf-8 -*-
"""TugasPythonLanjutan_Hari_10_Raka_Rizkya_Hadi_Putra.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1H-pQRFUFkpcdrAoI7TGxAByLzmExVsjz
"""

# Import library yang dibutuhkan
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from openpyxl import Workbook

# Mengakses website target
alamat = "https://pokemondb.net/pokedex/all"
safeAdd = Request(alamat, headers={'User-Agent': 'Mozilla/5.0'})
html = urlopen(safeAdd)
data = BeautifulSoup(html, 'html.parser')

# Mengambil tabel pada website target
table = data.find("table", {"id":"pokedex"})
rows = data.findAll("tr", limit=17)

# Membuat nested list untuk setiap baris pada tabel
hasil = []
for row in rows:
  info = []
  for item in row.findAll(["th", "td"]):
    info.append(item.get_text())
  hasil.append(info)

# Membuat workbook baru
wb = Workbook()
ws = wb.active

# Memasukkan elemen list ke dalam workbook aktif
for item in hasil:
  ws.append(item)

# Memberi nama untuk sheet pada workbook aktif
ws.title = "Pokedex List"

# Menyimpan workbook dalam format xlsx
wb.save("TugasPythonLanjutan_Hari_10_Raka_Rizkya_Hadi_Putra.xlsx")