# Determines the top K hashtags

import sys
import json
import codecs

def getTopKHashtags(dict, collection):
    for item in collection.find():
        if not 'entities' in item:
            pass
        else:
            entities = item['entities']
            if not 'hashtags' in item:
                pass
            else:
                hashtags = entities['hashtags']
                if not hashtags:
                    pass
                else:
                    for hashtag in hashtags:
                        text = hashtag['text'].lower()
                        if text not in dict:
                            dict[text] = 1
                        else:
                            temp = dict.get(text);
                            temp = temp + 1
                            dict[text] = temp
    topK = sorted(dict.iteritems(), key = lambda x : x[1], reverse = True)
    print topK