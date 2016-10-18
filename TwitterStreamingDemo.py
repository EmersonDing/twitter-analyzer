import tweepy
from pymongo import MongoClient
import datetime

collection = MongoClient('localhost', 27017)["tweets"]["StreamingDemo"]

consumer_key = "8pCg0f2Ih81PSpbH5XQNptWPQ"
consumer_secret = "ghSdXGQKYABWdCn44TNizjvBt05l2mqeQtveBrBCkbVFGtB1iB"

access_token = "783900324704641024-fcqOlSez6zgnx3ArAq5jIDso736hT1V"
access_token_secret = "mXO8CSnhGP1jwBbBGop6zZTgmau4ywO7HtrF44MwBKAGZ"


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

f = open("test.txt", "wb")


class MyStreamListener(tweepy.StreamListener):

    count = 0

    def on_status(self, status):
    	self.count += 1
    	print self.count
    	collection.insert_one(status._json)
        if self.count > 1000000:
        	myStream.disconnect()
        	print "Twitter stream has been disconnected successfully."

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=MyStreamListener())

myStream.filter(track=['Trump'])

print collection.find_one()
print collection.count()
