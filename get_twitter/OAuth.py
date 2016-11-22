"""
This file pull data from twitter database through tweey api
"""

import sys
sys.path.append('../create_word_graph')
import json
import time
import tweepy
from tweepy import OAuthHandler
from ConnectMongoDB import *


#define twitter api key, api object
consumer_key = 'ezclHHereiiID7cclEt6Cis38'
consumer_secret = '9t7smN2C6hhRhyYOlf0Bn3XzRE64tT0pskBj992gcgL1bThZW8'
access_token = '717204620565725184-SIQZ7joIVLZpyK4aMZo2Vm5HHOQZV7o'
access_secret = 'WcXrEtY7bMT1hfHbf3OhjMlyVqfKGnrQHByAjAV0EQDis'
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

# create db object
db = Database()

#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.streaming.StreamListener):
    def on_status(self, status):
        print(status.text)
        db.insertRow(status._json, "twitter_stream")

# get archived data from twitter stream. currently in use
def getTwitterArchivedData():
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
    myStream.filter(track=['Donald Trump'], async=True)             # extract twitter with "Donald Trump" in the content

# get live data from twitter stream. currently not using cause the daily limit (280 rows/15 minutes)
def getTwitterStreamData():
    count = 0                           # count current data amount
    # read from twitter and write into mongo
    for status in tweepy.Cursor(api.home_timeline).items():
        process_or_store(status._json)  # print data
        db.insertRow(status._json)      # save into mongodb
        count += 1
        if (count == 250):
            count = 0
            print("Waiting....")
            time.sleep(15 * 60)

# print
def process_or_store(tweet):
    print(json.dumps(tweet))

if __name__ == "__main__":
    # getTwitterData()
    getTwitterArchivedData()