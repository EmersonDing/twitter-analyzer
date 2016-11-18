import tweepy
from pymongo import MongoClient
from hashtag import getTopKHashtags



print '--------------------------'
collection = MongoClient('localhost', 27017)["tweets"]["StreamingDemo"]

consumer_key = "8pCg0f2Ih81PSpbH5XQNptWPQ"
consumer_secret = "ghSdXGQKYABWdCn44TNizjvBt05l2mqeQtveBrBCkbVFGtB1iB"

access_token = "783900324704641024-fcqOlSez6zgnx3ArAq5jIDso736hT1V"
access_token_secret = "mXO8CSnhGP1jwBbBGop6zZTgmau4ywO7HtrF44MwBKAGZ"
print '--------------------------'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

print '----------Hilary-------------'

HilaryCol = MongoClient('localhost', 27017)["tweets"]["Hilary"]
print HilaryCol.count()





class MyStreamListener(tweepy.StreamListener):

    count = 0

    def on_status(self, status):
    	self.count += 1
    	print self.count
    	HilaryCol.insert_one(status._json)
        if self.count > 100:
        	myStream.disconnect()
        	print "Twitter stream has been disconnected successfully."


myStream = tweepy.Stream(auth = api.auth, listener=MyStreamListener())
print '---------------------------------'
myStream.filter(track=['Trump'])

print HilaryCol.find_one()
print HilaryCol.count()
"""
keywords = Keyword()

parsed_word = Keyword.getKeyword(keywords, collection.find_one()['text'])
print parsed_word

WordFrequency = {}

cnt = 0
for item in collection.find():
	words = Keyword.getKeyword(keywords, item['text'])
	for uword in words:
		try:
			word = str(uword)
		except (UnicodeEncodeError):
			pass
		if WordFrequency.has_key(word):
			WordFrequency[word] += 1
		else:
			WordFrequency[word] = 1
	print cnt
	cnt += 1
	print words

print WordFrequency

print '-----------------------'

TopKHashtag = {}
for item in collection.find():
	try:
		hashtags = item['entities']['hashtags']
		for hashtag in hashtags:
			text = hashtag['text'].lower()
			print text
			if text not in TopKHashtag:
				TopKHashtag[text] = 1
			else:
				temp = TopKHashtag.get(text);
				temp = temp + 1
				TopKHashtag[text] = temp
	except:
		print 'error happens'
		pass
topTree  = sorted(TopKHashtag.iteritems(), key = lambda x : x[1], reverse = True)
i = 1
for e in topTree[:10]:
	print (str(i) + ". " + str(e))
	i = i + 1
"""