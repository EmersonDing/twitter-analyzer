# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
import tweepy
import numpy as np
import pandas as pd
from pymongo import MongoClient
import re
import datetime
import json


collection = MongoClient('localhost', 27017)["tweets"]["StreamingDemo"]

consumer_key = "8pCg0f2Ih81PSpbH5XQNptWPQ"
consumer_secret = "ghSdXGQKYABWdCn44TNizjvBt05l2mqeQtveBrBCkbVFGtB1iB"

access_token = "783900324704641024-fcqOlSez6zgnx3ArAq5jIDso736hT1V"
access_token_secret = "mXO8CSnhGP1jwBbBGop6zZTgmau4ywO7HtrF44MwBKAGZ"


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


def get_api():
    consumer_key = "8pCg0f2Ih81PSpbH5XQNptWPQ"
    consumer_secret = "ghSdXGQKYABWdCn44TNizjvBt05l2mqeQtveBrBCkbVFGtB1iB"

    access_token = "783900324704641024-fcqOlSez6zgnx3ArAq5jIDso736hT1V"
    access_token_secret = "mXO8CSnhGP1jwBbBGop6zZTgmau4ywO7HtrF44MwBKAGZ"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    return api


def get_collection():
    collection = MongoClient('localhost', 27017)["tweets"]["StreamingDemo"]
    return collection


class MyStreamListener(tweepy.StreamListener):

    count = 0

    def on_status(self, status):
        self.count += 1
        print self.count
        collection.insert_one(status._json)
        if self.count > 1000:
            myStream.disconnect()
            print "Twitter stream has been disconnected successfully."

# myStreamListener = MyStreamListener()
# myStream = tweepy.Stream(auth=api.auth, listener=MyStreamListener())
#
# myStream.filter(track=['Trump'])


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    collection = get_collection()
    dataset = [{"created_at": item["created_at"],
                "text": item["text"],
                "user": "@%s" % item["user"]["screen_name"],
                "source": item["source"],
                "lang": item["lang"],
                } for item in collection.find()]

    dataset = pd.DataFrame(dataset)
    dataset.source_name = dataset.source.apply(get_source_name)
    source_counts = dataset.source_name.value_counts().sort_values()[-10:]
    lang_counts = dataset.lang.value_counts().sort_values()
    source_info = {}
    for s in source_counts.iteritems():
        source_info[s[0]] = s[1]
    return dict(source_info=source_info)


def get_source_name(x):
    value = re.findall(pattern="<[^>]+>([^<]+)</a>", string=x)
    if len(value) > 0:
        return value[0]
    else:
        return ""


def get_chart_device():
    print "get_chart_data"
    collection = get_collection()
    dataset = [{"created_at": item["created_at"],
                "text": item["text"],
                "user": "@%s" % item["user"]["screen_name"],
                "source": item["source"],
                "lang": item["lang"],
                "filter_level": item["filter_level"],
                } for item in collection.find()]

    dataset = pd.DataFrame(dataset)
    dataset.source_name = dataset.source.apply(get_source_name)
    source_counts = dataset.source_name.value_counts().sort_values()[-10:]
    lang_counts = dataset.lang.value_counts().sort_values()[-5:]
    filter_level_counts = dataset.filter_level.value_counts().sort_values()
    print "------------ The language distribution is : ------------------"
    print lang_counts
    print "---------- End of the language distribution is : -------------"
    print "------------ The filter_level distribution is : ------------------"
    print filter_level_counts
    print "---------- End of the filter_level distribution is : -------------"
    data = []
    for s in source_counts.iteritems():
        data.insert(0, {
            "Device": s[0],
            "tweets": s[1].item()
        })
        print type(s[1].item())
    print data
    json_data = response.json(data)
    print json_data
    return response.json(data)
    # json_data = json.dumps(data)
    # print json_data
    # return json.dumps(data)


def get_chart_lang():
    print "get_chart_data"
    collection = get_collection()
    dataset = [{"created_at": item["created_at"],
                "text": item["text"],
                "user": "@%s" % item["user"]["screen_name"],
                "source": item["source"],
                "lang": item["lang"],
                "filter_level": item["filter_level"],
                } for item in collection.find()]

    dataset = pd.DataFrame(dataset)
    lang_counts = dataset.lang.value_counts().sort_values()[-5:]
    filter_level_counts = dataset.filter_level.value_counts().sort_values()
    print "------------ The language distribution is : ------------------"
    print lang_counts
    print "---------- End of the language distribution is : -------------"
    print "------------ The filter_level distribution is : ------------------"
    print filter_level_counts
    print "---------- End of the filter_level distribution is : -------------"
    data = []
    for s in lang_counts.iteritems():
        data.insert(0, {
            "Language": s[0],
            "tweets": s[1].item()
        })
        print type(s[1].item())
    print data
    json_data = response.json(data)
    print json_data
    return response.json(data)
    # json_data = json.dumps(data)
    # print json_data
    # return json.dumps(data)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


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


