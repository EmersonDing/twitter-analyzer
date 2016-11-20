"""
This file test the tweepy library
"""

import tweepy
import json
import time
from tweepy import OAuthHandler
from tweepy import streaming
from ConnectMongoDB import *

"""
define twitter api key
"""
consumer_key = 'ezclHHereiiID7cclEt6Cis38'
consumer_secret = '9t7smN2C6hhRhyYOlf0Bn3XzRE64tT0pskBj992gcgL1bThZW8'
access_token = '717204620565725184-SIQZ7joIVLZpyK4aMZo2Vm5HHOQZV7o'
access_secret = 'WcXrEtY7bMT1hfHbf3OhjMlyVqfKGnrQHByAjAV0EQDis'
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

def process_or_store(tweet):
    print(json.dumps(tweet))

def getTwitterStreamData():
    # create db object
    db = Database()
    count = 0
    # read from twitter and write into mongo
    for status in tweepy.Cursor(api.home_timeline).items():
        process_or_store(status._json)
        # db.insertRow(status._json)
        count += 1
        if (count == 250):
            count = 0
            print("Waiting....")
            time.sleep(15 * 60)

db = Database()
#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.streaming.StreamListener):
    def on_status(self, status):
        print(status.text)
        db.insertRow(status._json, "twitter_stream")

# get archived data from twitter stream
def getTwitterArchivedData():
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
    myStream.filter(track=['Donald Trump'], async=True)

if __name__ == "__main__":
    # getTwitterData()
    getTwitterArchivedData()


