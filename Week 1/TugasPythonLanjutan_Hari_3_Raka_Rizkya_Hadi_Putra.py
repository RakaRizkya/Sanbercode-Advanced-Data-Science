# import library yang dibutuhkan
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

# Mengakses website yang ingin dituju
alamat = "https://en.wikipedia.org/wiki/List_of_brightest_stars"
html = urlopen(alamat)
data = BeautifulSoup(html, 'html.parser')

# Mencari tag untuk tabel dan baris
table = data.findAll("table", {"class":"wikitable"})[0]
rows = table.findAll("tr")

# Menambahkan tiap baris, kolom, dan header ke dalam list
hasil = []
for row in rows:
    info = []
    for cell in row.findAll(["td", "th"]):
        info.append(cell.get_text())
        info = [n.strip('\n') for n in info]
    hasil.append(info)

# Melakukan sedikit formatting dan mengubah list menjadi dataframe
hasil[1].insert(4, '')
df = pd.DataFrame(hasil[1:],columns=hasil[0])
print(df)

print("\n------------------------------------------------------------------------------\n")

# Mengakses website yang ingin dituju
address = "https://en.wikipedia.org/wiki/List_of_action_films_of_the_2020s"
url = urlopen(address)
data2 = BeautifulSoup(url, 'html.parser')

# Mencari tag untuk tabel dan baris tahun 2020 dan 2021
tabel2020 = data2.findAll("table", {"class":"wikitable"})[0]
tabel2021 = data2.findAll("table", {"class":"wikitable"})[1]
baris1 = tabel2020.findAll("tr")
baris2 = tabel2021.findAll("tr")

# Membuat list untuk hasil akhir
result = []

# Membuat list dari tabel pertama (2020)
list1 = []
for i in baris1:
    elemen = []
    for j in i.findAll(["td", "th"]):
        elemen.append(j.get_text())
        elemen = [x.replace('\n', '') for x in elemen]
    list1.append(elemen)

# Membuat list dari tabel pertama (2021)
list2 = []
for i in baris2:
    elemen2 = []
    for j in i.findAll(["td", "th"]):
        elemen2.append(j.get_text())
        elemen2 = [x.replace('\n', '') for x in elemen2]
    list2.append(elemen2)

# Menggabungkan dan mencetak list
result = list1 + list2
print(result)