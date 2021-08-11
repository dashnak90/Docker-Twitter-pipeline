import pymongo
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sqlalchemy import create_engine
import logging

# Establish a connection to the MongoDB server
time.sleep(10)  # seconds
client = pymongo.MongoClient("mongodb")
db = client.tweetsdb 
# Establish a connection to the PostgresDB server
pg = create_engine('postgresql://user:pass123@postgresdb:5432/dbname', echo=True)

pg.execute('''
    CREATE TABLE IF NOT EXISTS tweets (    
    text VARCHAR(500) UNIQUE,
    username VARCHAR(255),
    date VARCHAR(255),
    photo TEXT,
    count NUMERIC,
    sentiment NUMERIC

);
''')

#a function extract() reads data from MongoDB and returns the entries
def extract(): 
    extracted=list(db.tweet_data.find())    
    return extracted



#a function transform() performs the Sentiment Analysis 
# and returns entries with sentiments    

s  = SentimentIntensityAnalyzer()

def transform(extracted):
    transformed=[]
    for e in extracted:
        if e['text'].startswith('RT') or e['text'].startswith('@'):
            continue
        else:
            d={}
            #print(e)
            d['text'] = e['text']
            d['user']= e['username']
            d['date'] = e['date']
            d['photo'] = e['photo'].replace("_normal",'')
            d['count']= e['followers_count']
                
            sentiment = s.polarity_scores(e['text'])   
            compound = sentiment['compound']
            d['sentiment']=compound
            transformed.append(d)

    return  transformed


#a function load() stores the result

def load(transformed):
    for i in transformed:
        query = "INSERT INTO tweets (text, username, date, photo, count, sentiment) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (text) DO NOTHING;"
        pg.execute(query, (i['text'],i['user'],i['date'],i['photo'],i['count'], i['sentiment'])) 



while True:
    extracted=extract()
    transformed=transform(extracted)
    load(transformed)
    logging.critical("ETL job finished")
    time.sleep(10)

    
