import config
from tweepy import OAuthHandler, Cursor, API
from tweepy.streaming import StreamListener
import logging
import pymongo

# create a connection - (create engine)
client = pymongo.MongoClient('mongodb')    #name of the docker container 
db = client.tweetsdb                         #the name of a database*(autom created)
collection = db.tweet_data                 #create a collection

def authenticate():
    """Function for handling Twitter Authentication. Please note
       that this script assumes you have a file called config.py
       which stores the 2 required authentication tokens:

       1. API_KEY
       2. API_SECRET
     

    See course material for instructions on getting your own Twitter credentials.
    """
    auth = OAuthHandler(config.API_KEY, config.API_SECRET)
    return auth

if __name__ == '__main__':
    auth = authenticate()
    api = API(auth)
    list=['washingtonpost', 'nytimes']  #chosing 2 diff newspapers
    for i in list:

        cursor = Cursor(
            api.user_timeline,
            id = i,
            tweet_mode = 'extended'
        )

        for status in cursor.items(100):    #get 100 tweets per newspaper
            text = status.full_text

        # take extended tweets into account
        # TODO: CHECK
            if 'extended_tweet' in dir(status):
                text =  status.extended_tweet.full_text
            if 'retweeted_status' in dir(status):
                r = status.retweeted_status
                if 'extended_tweet' in dir(r):
                    text =  r.extended_tweet.full_text

            tweet = {
                'text': text,
                'username': status.user.screen_name
            }
            collection.insert_one(tweet)  #insert into Mongodb
            print(tweet)

