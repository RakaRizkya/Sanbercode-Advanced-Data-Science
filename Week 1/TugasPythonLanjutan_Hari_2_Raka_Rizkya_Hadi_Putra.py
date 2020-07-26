"""TugasPythonLanjutan_Hari_2_Raka Rizkya Hadi Putra

Nama : Raka Rizkya Hadi Putra
Email : rakarizkya07@gmail.com
"""

# Import library yang dibutuhkan
from urllib.request import urlopen
from bs4 import BeautifulSoup

# Mengakses website yang ingin dituju
alamat = "https://blog.sanbercode.com/"
html = urlopen(alamat)
data = BeautifulSoup(html, 'html.parser')

# Mencari tag yang diinginkan dan melakukan slicing
raw1 = data.findAll("a", {"class":"text-dark"})[1:4]
raw2 = data.findAll("a", {"class":"text-muted"})[2:5]

# Membuat list kosong untuk data judul dan penulis
list1 = []
list2 = []

# Menyimpan data judul dari raw1 ke dalam list1 
for i in range(len(raw1)):
    list1.append(raw1[i].get_text())

# Menyimpan data penulis dari raw2 ke dalam list2 
for i in range(len(raw2)):
    list2.append(raw2[i].get_text())

# Menghilangkan line break dan white space pada list1
list1 = [n.replace('\n', '') for n in list1]
list1 = [w.strip(' ') for w in list1]
print(list1)

# Menghilangkan line break dan white space pada list2
list2 = [n.replace('\n', '') for n in list2]
list2 = [w.strip(' ') for w in list2]
print(list2)