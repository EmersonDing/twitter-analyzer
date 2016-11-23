"""
This file connect with local MongoDB. define database execution related functions
"""

from pymongo import MongoClient

class Database:
    def __init__(self):
        try:
            self.client = MongoClient()
            self.db = self.client.twitter   # define a database object
        except Exception:
            print(Exception)

    # read twitter stream data from mongodb with start and end index
    def getTwitterText(self, collection, start, end):
        return self.db[collection].find({},{"_id":0, "text":1})[start:end]

    # write an edge {keyword, neighbor} into keyword_graph table with count as the weight
    def insertKeywordGraph(self, keyword, neighbor, count):
        # if no keyword "keyword" in keyword_graph, create an keyword node with empty neighbors array
        if self.db.keyword_graph.find({"keyword": keyword}).count() == 0:
            self.db.keyword_graph.insert({"keyword": keyword, "neighbors": []})
        # if no neighbor "neighbor", create new neighbor in keyword with count as weight
        if self.db.keyword_graph.find({"keyword": keyword, "neighbors": {"$elemMatch": {"keyword": neighbor}}}).count() == 0:
            self.db.keyword_graph.update_one({"keyword": keyword}, {"$addToSet" : {"neighbors": {"keyword":neighbor, "count": count}}})
        # if neighbor already exist, update count
        else:
            self.db.keyword_graph.update_one({"keyword": keyword, "neighbors.keyword": neighbor}, {"$inc": {"neighbors.$.count": count}})

    # return twitter_stream table size
    def getTwitterCollectionSize(self):
        return self.db.twitter_stream.find().count()

    # return one row of data in "collection" table
    def getRow(self, collection):
        return self.db[collection].find({},{"_id":0, "text":1})

    # insert one row of data into "collection" table
    def insertRow(self, row, collection):
        post_id = self.db[collection].insert_one(row)
        return post_id

if __name__ == "__main__":
    db = Database()

    # for line in db.getTwitterText("twitter_stream", 0, 1000):
    #     print(line)

    # db.getTwitterText()

    # db.insertKeywordGraph("Don", "JFK", 3)

    # print(db.insertRow({'text':'test'}, "twitter_stream"))

    # db.getRow("twitter_stream")
