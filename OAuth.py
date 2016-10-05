"""
This file test the tweepy library
"""

import tweepy
from tweepy import OAuthHandler

consumer_key = 'ezclHHereiiID7cclEt6Cis38'
consumer_secret = '9t7smN2C6hhRhyYOlf0Bn3XzRE64tT0pskBj992gcgL1bThZW8'
access_token = '717204620565725184-SIQZ7joIVLZpyK4aMZo2Vm5HHOQZV7o'
access_secret = 'WcXrEtY7bMT1hfHbf3OhjMlyVqfKGnrQHByAjAV0EQDis'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

for status in tweepy.Cursor(api.home_timeline).items(10):
    print(status.text)
