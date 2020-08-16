# Import library yang dibutuhkan
import tweepy
import pandas as pd
import matplotlib.pyplot as plt
import re
import numpy as np
import datetime
import sqlite3

# Nama : Raka Rizkya Hadi Putra
# Email : rakarizkya07@gmail.com

print('Apa yang ingin anda lakukan?\n\t1.Update Data\n\t2.Update Nilai Sentiment\n\t3.Lihat Data\n\t4.Visualisasi\n\t5.Keluar')
x = input()
if x == '1':
  # Input Tanggal
  date_entry = input('Tanggal Awal (format: 2020-04-24)')
  year, month, day = map(int, date_entry.split('-'))
  date_until = datetime.date(year, month, day)
  df = lihat_data(consumer_key,consumer_secret,access_token,access_token_secret,keyword)
  input_sql(df)
elif x == '2':
  # Membuka tabel ke dataframe
  cnx = sqlite3.connect('project.db')
  data = pd.read_sql_query("SELECT * FROM tweet", cnx)
  input_sentiment(data)
elif x == '3':
  lihat_sentiment()
elif x == '4':
  lihat_sentiment()
  visualisasi(data1)

elif x == '5':
  exit()
else:
  print('Pilihan tidak tersedia')

# Menyiapkan key untuk mengakses API twitter
consumer_key = "onqGw4kpoQl8V9civEIDTzwct"
consumer_secret = "GwoBtWhEuuQQqmthLMnCTY0JexAwjLjFgUNvqTLoFcL9I1eCDk"
access_token = "1288079487284858880-a9IzuV48TwVfjmN3Uh024hGCrCWAql"
access_token_secret = "3Dmek80uNr6yVBW1YQ496GOgsXo0IgUX9Na6gYOSMnMwT"

# Menentukan keyword yang akan dicari
keyword = "vaksin covid"

def lihat_data(consumer_key,consumer_secret,access_token,access_token_secret, keyword):
  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_token_secret)
  api = tweepy.API(auth)

  # Mengambil tweet pada hari sebelum hari-H
  date_since = datetime.datetime.strftime(date_until - datetime.timedelta(1), '%Y-%m-%d')
  new_search = keyword + " -filter:retweets"

  # Mencari tweet dengan api.search
  tweets = tweepy.Cursor(api.search, q=new_search, lang="id", since=date_since, until=date_until).items(-1)

  # Memasukkan data tweet ke dalam list pertama
  items = []
  for tweet in tweets:
    item = []
    item.append(tweet.created_at)
    item.append(tweet.user.screen_name)
    item.append(tweet.user.location)
    item.append (' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet.text).split()))
    items.append(item)
    
  # Mengubah list menjadi dataframe
  hasil = pd.DataFrame(data=items, columns=['Created','User','Lokasi','Tweet'])
  return hasil

def input_sql(df):
  database_name = "project.db"
  create_table = '''CREATE TABLE IF NOT EXISTS tweet (
                            Created TEXT,
                            Username TEXT,
                            Lokasi TEXT,
                            Tweet TEXT);'''
  insert_table = '''INSERT INTO tweet (Created, Username, Lokasi, Tweet) values (?, ?, ?, ?);'''
  connection = sqlite3.connect(database_name)
  cursor = connection.cursor()
  cursor.execute(create_table)
  for i in range(len(df)-1):
    baris = df.loc[[i+1],:]
    try:
      Created = str(baris["Created"].values[0])
      Username = str(baris["User"].values)
      Lokasi = str(baris["Lokasi"].values)
      Tweet = str(baris["Tweet"].values)
      cursor.execute(insert_table, (Created, Username, Lokasi, Tweet))
    except:
      continue
  connection.commit()
  cursor.close()
  connection.close()

def lihat_sentiment():  
  # Membuka tabel ke dataframe
  cnx = sqlite3.connect('project.db')
  data1 = pd.read_sql_query("SELECT * FROM sentimen", cnx)
  return data1

def visualisasi(data):
  labels, counts = np.unique(data["Sentiment"], return_counts=True)
  plt.bar(labels, counts, align='center')
  plt.gca().set_xticks(labels)
  plt.show()

def input_sentiment(df):
  items = data['Tweet'].tolist()
  items = [s.strip('[]') for s in items]
  items = [s.strip("'") for s in items]
  items = [x.lower() for x in items]

  pos_list= open("./kata_positif.txt","r")
  pos_kata = pos_list.readlines()
  neg_list= open("./kata_negatif.txt","r")
  neg_kata = neg_list.readlines()
  
  S=[]

  for item in items:
    count_p = 0
    count_n = 0
    for kata_pos in pos_kata:
      if kata_pos.strip() in item:
        count_p +=1
    
    for kata_neg in neg_kata:
      if kata_neg.strip() in item:
        count_n +=1
    
    S.append(count_p - count_n)

  data['Sentiment'] = S

  database_name = "project.db"
  create_table = '''CREATE TABLE IF NOT EXISTS sentimen (
                            Created VARCHAR(50),
                            Username VARCHAR(50),
                            Lokasi VARCHAR(50),
                            Tweet VARCHAR(500),
                            Sentiment INTEGER);'''
  insert_table = '''INSERT INTO sentimen (Created, Username, Lokasi, Tweet, Sentiment) values (?, ?, ?, ?, ?);'''
  connection = sqlite3.connect(database_name)
  cursor = connection.cursor()
  cursor.execute(create_table)
  for i in range(len(df)-1):
    try:
      baris = df.loc[[i+1],:]
      Created = str(baris["Created"].values[0])
      Username = str(baris["Username"].values)
      Lokasi = str(baris["Lokasi"].values)
      Tweet = str(baris["Tweet"].values)
      Sentiment = int(baris["Sentiment"].values)
      cursor.execute(insert_table, (Created, Username, Lokasi, Tweet, Sentiment))
    except:
      continue
  connection.commit()
  cursor.close()
  connection.close()