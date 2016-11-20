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

    def getRow(self, collection):
        # for line in self.db[collection].find({},{"text":1}):
        #     print(line)
        return self.db[collection].find({},{"_id":0, "text":1})

    def insertRow(self, row, collection):
        post_id = self.db[collection].insert_one(row)
        return post_id

if __name__ == "__main__":
    db = Database()
    # db.insertRow({'text':'test'}, "twitter_stream")
    db.getRow("twitter_stream")

