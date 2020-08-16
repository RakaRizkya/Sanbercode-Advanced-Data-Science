# import library yang dibutuhkan
import tweepy
import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Menyiapkan key yang dibutuhkan
consumer_key =  "onqGw4kpoQl8V9civEIDTzwct"
consumer_secret = "GwoBtWhEuuQQqmthLMnCTY0JexAwjLjFgUNvqTLoFcL9I1eCDk"
access_token = "1288079487284858880-a9IzuV48TwVfjmN3Uh024hGCrCWAql"
access_token_secret = "3Dmek80uNr6yVBW1YQ496GOgsXo0IgUX9Na6gYOSMnMwT"

# Autentikasi dengan key yang telah disiapkan
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Menentukan keyword yang akan dicari
search_words1 = "jouska"
search_words2 = "anies baswedan"
search_words3 = "terawan"

date_since = "2020-07-27"
new_search1 = search_words1 + " -filter:retweets"
new_search2 = search_words2 + " -filter:retweets"
new_search3 = search_words3 + " -filter:retweets"

# Mencari tweet dengan api.search untuk 1000 data
tweets1 = tweepy.Cursor(api.search, q=new_search1, lang="id", since=date_since).items(1000)
tweets2 = tweepy.Cursor(api.search, q=new_search2, lang="id", since=date_since).items(1000)
tweets3 = tweepy.Cursor(api.search, q=new_search3, lang="id", since=date_since).items(1000)

# Memasukkan data tweet ke dalam list pertama
items1 = []
for tweet in tweets1:
  item = []
  item.append (' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet.text).split()))
  items1.append(item)

# Mengubah list menjadi dataframe
hasil1 = pd.DataFrame(data=items1, columns=['tweet'])

# Memasukkan data tweet ke dalam list kedua
items2 = []
for tweet in tweets2:
  item = []
  item.append (' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet.text).split()))
  items2.append(item)

# Mengubah list menjadi dataframe
hasil2 = pd.DataFrame(data=items2, columns=['tweet'])

# Memasukkan data tweet ke dalam list ketiga
items3 = []
for tweet in tweets3:
  item = []
  item.append (' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet.text).split()))
  items3.append(item)

# Mengubah list menjadi dataframe
hasil3 = pd.DataFrame(data=items3, columns=['tweet'])

# Mengubah data dalam dataframe menjadi lowercase
hasil1['tweet'] = hasil1['tweet'].str.lower()
hasil2['tweet'] = hasil2['tweet'].str.lower()
hasil3['tweet'] = hasil3['tweet'].str.lower()
print(hasil1.shape)
print(hasil2.shape)
print(hasil3.shape)

# Memasukkan dokumen kata positif dan kata negatif
pos_list= open("./kata_positif.txt","r")
pos_kata = pos_list.readlines()
neg_list= open("./kata_negatif.txt","r")
neg_kata = neg_list.readlines()

# Deklarasi list untuk masing2 keyword
S1 = []
S2 = []
S3 = []

# iterasi untuk list pertama
for item in items1:
  count_p = 0
  count_n = 0
  for kata_pos in pos_kata:
    if kata_pos.strip() in item[0]:
      count_p +=1
  for kata_neg in neg_kata:
    if kata_neg.strip() in item[0]:
      count_n +=1
  S1.append(count_p - count_n)

# iterasi untuk list kedua
for item in items2:
  count_p = 0
  count_n = 0
  for kata_pos in pos_kata:
    if kata_pos.strip() in item[0]:
      count_p +=1
  for kata_neg in neg_kata:
    if kata_neg.strip() in item[0]:
      count_n +=1
  S2.append(count_p - count_n)

# iterasi untuk list pertama
for item in items3:
  count_p = 0
  count_n = 0
  for kata_pos in pos_kata:
    if kata_pos.strip() in item[0]:
      count_p +=1
  for kata_neg in neg_kata:
    if kata_neg.strip() in item[0]:
      count_n +=1
  S3.append(count_p - count_n)

# Melihat panjang dari setiap list
print(len(S1))
print(len(S2))
print(len(S3))

# Hasil untuk topik pertama
hasil1["value"] = S1
print ("Nilai rata-rata: "+str(np.mean(hasil1["value"])))
print ("Nilai median: "+str(np.median(hasil1["value"])))
print ("Standar deviasi: "+str(np.std(hasil1["value"])))

# Hasil untuk topik kedua
hasil2["value"] = S2
print ("\nNilai rata-rata: "+str(np.mean(hasil2["value"])))
print ("Nilai median: "+str(np.median(hasil2["value"])))
print ("Standar deviasi: "+str(np.std(hasil2["value"])))

# Hasil untuk topik ketiga
hasil3["value"] = S3
print ("\nNilai rata-rata: "+str(np.mean(hasil3["value"])))
print ("Nilai median: "+str(np.median(hasil3["value"])))
print ("Standar deviasi: "+str(np.std(hasil3["value"])))

# Membuat 3 subplot untuk masing2 hasil
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18,6))
plt.style.use('seaborn')

# Plotting hasil pertama
labels1, counts1 = np.unique(hasil1["value"], return_counts=True)
ax1.bar(labels1, counts1, align='center')
ax1.set_title("Sentimen terhadap Penipuan Jouska")

# Plotting hasil kedua
labels2, counts2 = np.unique(hasil2["value"], return_counts=True)
ax2.bar(labels2, counts2, align='center')
ax2.set_title("Sentimen terhadap Anies Baswedan")

# Plotting hasil ketiga
labels3, counts3 = np.unique(hasil3["value"], return_counts=True)
ax3.bar(labels3, counts3, align='center')
ax3.set_title("Sentimen terhadap Menteri Kesehatan, Dr.Terawan")

plt.show()

kesimpulan = """Dapat dilihat pada plot bahwa dari ketiga topik yang telah diambil dari twitter,
Topik pertama memiliki sentimen yang netral dengan nilai tertingi yaitu 300 bahasan, topik kedua
memiliki sentimen yang sedikit negatif (-1) dengan total bahasan sebanyak lebih dari 175, dan topik
ketiga, juga memiliki sentimen yang sedikit negatif (-1) dengan total bahasan terbanyak lebih dari 60"""
print(kesimpulan)