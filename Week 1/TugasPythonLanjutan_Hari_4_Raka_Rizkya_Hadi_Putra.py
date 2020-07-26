# Import library yang dibutuhkan
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd
import csv

# Mengakses halaman dengan tambahan header
alamat = "https://pokemondb.net/pokedex/all"
safeAdd = Request(alamat, headers={'User-Agent': 'Mozilla/5.0'})
html = urlopen(safeAdd)
data = BeautifulSoup(html, 'html.parser')

# Mencari tabel dan baris pada halaman web
table = data.find("table", {"id":"pokedex"})
rows = data.findAll("tr", limit=28)

# Membuat nested list untuk setiap baris pada tabel
hasil = []
for row in rows:
    info = []
    for item in row.findAll(["th", "td"]):
        info.append(item.get_text())
    hasil.append(info)

# Mengubah list menjadi dataframe
df = pd.DataFrame(hasil[1:],columns=hasil[0])

# Export dataframe menjadi csv dan memisahkan tiap cell
df.to_csv('pokemon.csv', sep=';', index=False)
print(df)