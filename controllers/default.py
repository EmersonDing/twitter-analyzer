# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
# import re
# import tweepy
# import redis
# from pymongo import MongoClient
#
# collection = MongoClient('localhost', 27017)["tweets"]["Trump"]
# rt_collection = MongoClient('localhost', 27017)["rt_analysis"]["Trump"]
#
# r_device = redis.Redis(host='localhost', port=6379, db=0)
# r_hashtag = redis.Redis(host='localhost', port=6379, db=1)
#
# # collection = None
# consumer_key = "8pCg0f2Ih81PSpbH5XQNptWPQ"
# consumer_secret = "ghSdXGQKYABWdCn44TNizjvBt05l2mqeQtveBrBCkbVFGtB1iB"
#
# access_token = "783900324704641024-fcqOlSez6zgnx3ArAq5jIDso736hT1V"
# access_token_secret = "mXO8CSnhGP1jwBbBGop6zZTgmau4ywO7HtrF44MwBKAGZ"
#
#
# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)
#
# api = tweepy.API(auth)
# myStream = None
# analysis_type = None
# number_of_tweet = 100
# number_of_item = 3
#
#
# def get_api():
#     consumer_key = "8pCg0f2Ih81PSpbH5XQNptWPQ"
#     consumer_secret = "ghSdXGQKYABWdCn44TNizjvBt05l2mqeQtveBrBCkbVFGtB1iB"
#
#     access_token = "783900324704641024-fcqOlSez6zgnx3ArAq5jIDso736hT1V"
#     access_token_secret = "mXO8CSnhGP1jwBbBGop6zZTgmau4ywO7HtrF44MwBKAGZ"
#
#     auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#     auth.set_access_token(access_token, access_token_secret)
#
#     api = tweepy.API(auth)
#
#     return api
#
#
def index():
    return dict()
#
#
# def get_source_name(x):
#     value = re.findall(pattern="<[^>]+>([^<]+)</a>", string=x)
#     if len(value) > 0:
#         return value[0]
#     else:
#         return ""
#
#
# def process_tweets(analysis_type, status):
#     print 'start process'
#     if analysis_type == 'Device':
#         name = get_source_name(status._json["source"])
#         if name is not None:
#             if r_device.get(name):
#                 r_device.incr(name, 1)
#             else:
#                 r_device.set(name, 1)
#     elif analysis_type == 'Hashtag':
#         try:
#             hashtags = status._json['entities']['hashtags']
#             for hashtag in hashtags:
#                 name = hashtag['text'].lower()
#                 if r_hashtag.get(name):
#                     r_hashtag.incr(name, 1)
#                 else:
#                     r_hashtag.set(name, 1)
#         except Exception as e:
#             print e.__doc__
#             pass
#
#
# class MyStreamListener(tweepy.StreamListener):
#     global myStream
#     global number_of_tweet
#
#     analysis_type = None
#     count = 0
#
#     def on_status(self, status):
#         self.count += 1
#         print self.count
#         process_tweets(analysis_type, status)
#         if self.count > int(number_of_tweet):
#             myStream.disconnect()
#             print "Twitter stream has been disconnected successfully."
#
#
# def get_streaming_tweets(search_word):
#     global myStream
#     print 'the search word is : ' + search_word
#     myStream = tweepy.Stream(auth=api.auth, listener=MyStreamListener())
#     myStream.filter(track=[search_word])
#
#
# def get_chart_data():
#     global analysis_type
#     global number_of_tweet
#     global number_of_item
#
#     r_device.flushall()
#     r_hashtag.flushall()
#
#     search_word = request.vars.search_text
#     analysis_type = request.vars.type_of_analysis
#     number_of_tweet = request.vars.number_of_tweet
#     number_of_item = request.vars.number_of_item
#
#     print number_of_item
#
#     if analysis_type is None:
#         analysis_type = 'Device'
#     if search_word is None:
#         search_word = 'Trump'
#     print 'The search word is : '
#     print search_word
#     get_streaming_tweets(search_word)
#
#     data = []
#     if analysis_type == 'Device':
#         for key in r_device.keys():
#             data.append((key, int(r_device.get(key))))
#         print data
#     elif analysis_type == 'Hashtag':
#         for key in r_hashtag.keys():
#             data.append((key, int(r_hashtag.get(key))))
#         print data
#     sorted_data = sorted(data, key=lambda x: x[1], reverse=True)
#     print '-------- sorted data --------'
#     print sorted_data
#     data = []
#     count = 0
#     for tp in sorted_data:
#         if count >= int(number_of_item):
#             break
#         else:
#             count += 1
#             data.append({
#                 'Type': tp[0],
#                 'tweets': tp[1]
#             })
#     return response.json(data)
#
#
# def get_realtime_update():
#     analysis_type = request.vars.type_of_analysis
#     number_of_item = request.vars.number_of_item
#     print number_of_item
#     print analysis_type
#
#     data = []
#     if analysis_type == 'Device':
#         for key in r_device.keys():
#             data.append((key, int(r_device.get(key))))
#         print data
#     elif analysis_type == 'Hashtag':
#         for key in r_hashtag.keys():
#             data.append((key, int(r_hashtag.get(key))))
#         print data
#     sorted_data = sorted(data, key=lambda x: x[1], reverse=True)
#     print '-------- sorted data --------'
#     print sorted_data
#     data = []
#     count = 0
#     for tp in sorted_data:
#         if count >= int(number_of_item):
#             break
#         else:
#             count += 1
#             data.append({
#                 'Type': tp[0],
#                 'tweets': tp[1]
#             })
#     return response.json(data)
#
#
# def user():
#     """
#     exposes:
#     http://..../[app]/default/user/login
#     http://..../[app]/default/user/logout
#     http://..../[app]/default/user/register
#     http://..../[app]/default/user/profile
#     http://..../[app]/default/user/retrieve_password
#     http://..../[app]/default/user/change_password
#     http://..../[app]/default/user/bulk_register
#     use @auth.requires_login()
#         @auth.requires_membership('group name')
#         @auth.requires_permission('read','table name',record_id)
#     to decorate functions that need access control
#     also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
#     """
#     return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


