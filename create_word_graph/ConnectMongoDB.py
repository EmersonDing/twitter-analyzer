"""
This file connect with local MongoDB
"""

from pymongo import MongoClient

class Database:
    def __init__(self):
        try:
            self.client = MongoClient()
            self.db = self.client.twitter
        except Exception:
            print(Exception)

    def getTwitterText(self, collection, start, end):
        # for line in self.db[collection].find({},{"text":1})[9:10]:
        #     print(line)
        return self.db[collection].find({},{"_id":0, "text":1})[start:end]

    def insertKeywordGraph(self, keyword, neighbor, count):
        if self.db.keyword_graph.find({"keyword": keyword}).count() == 0:
            self.db.keyword_graph.insert({"keyword": keyword, "neighbors": []})
        if self.db.keyword_graph.find({"keyword": keyword, "neighbors": {"$elemMatch": {"keyword": neighbor}}}).count() == 0:
            self.db.keyword_graph.update_one({"keyword": keyword}, {"$addToSet" : {"neighbors": {"keyword":neighbor, "count": count}}})
        else:
            self.db.keyword_graph.update_one({"keyword": keyword, "neighbors.keyword": neighbor}, {"$inc": {"neighbors.$.count": count}})

        # post_id = self.db.keyword_graph.insert_one("")
        # return post_id

    def getTwitterCollectionSize(self):
        return self.db.twitter_stream.find().count()

    def getRow(self, collection):
        # for line in self.db[collection].find({},{"text":1}):
        #     print(line)
        return self.db[collection].find({},{"_id":0, "text":1})

    def insertRow(self, row, collection):
        post_id = self.db[collection].insert_one(row)
        return post_id

if __name__ == "__main__":
    db = Database()
    for line in db.getTwitterText("twitter_stream", 0, 1000):
        print(line)
    # db.getTwitterText()
    # db.insertKeywordGraph("Don", "JFK", 3)
    # print(db.insertRow({'text':'test'}, "twitter_stream"))
    # db.getRow("twitter_stream")

