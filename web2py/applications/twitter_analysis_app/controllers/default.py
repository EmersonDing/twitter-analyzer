# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
import re

import pandas as pd
import tweepy
from pymongo import MongoClient

import nltk
from nltk.corpus import treebank

collection = MongoClient('localhost', 27017)["tweets"]["StreamingDemo"]

# collection = None
consumer_key = "8pCg0f2Ih81PSpbH5XQNptWPQ"
consumer_secret = "ghSdXGQKYABWdCn44TNizjvBt05l2mqeQtveBrBCkbVFGtB1iB"

access_token = "783900324704641024-fcqOlSez6zgnx3ArAq5jIDso736hT1V"
access_token_secret = "mXO8CSnhGP1jwBbBGop6zZTgmau4ywO7HtrF44MwBKAGZ"


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
myStream = None


def get_api():
    consumer_key = "8pCg0f2Ih81PSpbH5XQNptWPQ"
    consumer_secret = "ghSdXGQKYABWdCn44TNizjvBt05l2mqeQtveBrBCkbVFGtB1iB"

    access_token = "783900324704641024-fcqOlSez6zgnx3ArAq5jIDso736hT1V"
    access_token_secret = "mXO8CSnhGP1jwBbBGop6zZTgmau4ywO7HtrF44MwBKAGZ"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    return api


class MyStreamListener(tweepy.StreamListener):
    global collection
    global myStream
    count = 1
    goal = 1000 - collection.count()

    def on_status(self, status):
        self.count += 1
        collection.insert_one(status._json)
        if self.count > 1000:
            myStream.disconnect()
            print "Twitter stream has been disconnected successfully."


class Keyword:
    def __init__(self):
        self.stopWordList = set()          # stop word list
        f = open('D:\Workspaces\Tweet-Streaming-Data-Analysis-Service\web2py\StopWord.txt', 'r')
        for line in f:
            line = line[:-1]            # remove '\n'
            self.stopWordList.add(line)

    def getKeyword(self, sentence):
        words = []
        tokens = nltk.word_tokenize(sentence)
        tagged = nltk.pos_tag(tokens)

        # extract noun and noun phrase
        word = ""
        index = 0
        check = 0
        while(index < len(tagged)):
            if "NN" in tagged[index][1]:
                word += tagged[index][0].lower()
                check = index
                while index+1 < len(tagged) and "NN" in tagged[index+1][1]:
                    word += " " + tagged[index+1][0].lower()
                    index += 1
                words.append(word)
            index += 1
            word = ""

        return words


def update_collection(search_word):
    global myStream

    myStream = tweepy.Stream(auth=api.auth, listener=MyStreamListener())
    myStream.filter(track=[search_word])


def index():
    return dict()


def get_source_name(x):
    value = re.findall(pattern="<[^>]+>([^<]+)</a>", string=x)
    if len(value) > 0:
        return value[0]
    else:
        return ""


def process_device_analysis():
    global collection

    dataset = [{"source": item["source"]
                } for item in collection.find()]

    dataset = pd.DataFrame(dataset)
    dataset.device_name = dataset.source.apply(get_source_name)
    result = dataset.device_name.value_counts().sort_values()[-10:]

    data = []
    for s in result.iteritems():
        data.insert(0, {
            "Type": s[0],
            "tweets": s[1].item()
        })

    return data


def process_language_analysis():
    global collection

    dataset = [{"lang": item["lang"]
                } for item in collection.find()]

    dataset = pd.DataFrame(dataset)
    result = dataset.lang.value_counts().sort_values()[-5:]

    data = []
    for s in result.iteritems():
        data.insert(0, {
            "Type": s[0],
            "tweets": s[1].item()
        })

    return data


def process_hashtag_analysis():
    global collection

    top_k_hashtag = {}
    for item in collection.find():
        try:
            hashtags = item['entities']['hashtags']
            for hashtag in hashtags:
                text = hashtag['text'].lower()
                if text not in top_k_hashtag:
                    top_k_hashtag[text] = 1
                else:
                    temp = top_k_hashtag[text]
                    temp = temp + 1
                    top_k_hashtag[text] = temp
        except Exception as e:
            pass

    data = []
    top_sorted = sorted(top_k_hashtag.iteritems(), key=lambda x: x[1], reverse=False)
    for item in top_sorted[-10:]:
        data.insert(0, {
            "Type": str(item[0]),
            "tweets": item[1]
        })

    return data


def process_keyword_analysis():
    global collection

    key_word = Keyword()
    word_frequency = {}

    for item in collection.find():
        parsed_word = Keyword.getKeyword(key_word, item['text'])
        for unicode_word in parsed_word:
            try:
                word = str(unicode_word)
            except (UnicodeEncodeError):
                pass
            if word_frequency.has_key(word):
                word_frequency[word] += 1
            else:
                word_frequency[word] = 1

    data = []
    top_sorted = sorted(word_frequency.iteritems(), key=lambda x: x[1], reverse=False)
    for item in top_sorted[-10:]:
        data.insert(0, {
            "Type": str(item[0]),
            "tweets": item[1]
        })

    return data


def get_chart_data():
    global collection

    search_word = request.vars.search_text
    analysis_type = request.vars.type_of_analysis

    collection = MongoClient('localhost', 27017)["tweets"][search_word]
    if collection.count() < 1000:
        update_collection(search_word)

    data = []
    if analysis_type == 'Device':
        data = process_device_analysis()
    elif analysis_type == 'Language':
        data = process_language_analysis()
    elif analysis_type == 'Hashtag':
        data = process_hashtag_analysis()
    elif analysis_type == 'Keyword':
        data = process_keyword_analysis()

    return response.json(data)


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


