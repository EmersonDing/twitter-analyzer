"""
This file connect with local MongoDB
"""

from pymongo import MongoClient

class Database:
    def __init__(self):
        try:
            self.client = MongoClient()
            self.db = self.client.twitter
            self.collection = self.db.twitter_stream
        except Exception:
            print(Exception)

    def getRow(self):
        for line in self.collection.find():
            print(line)

    def insertRow(self, row):
        post_id = self.db.twitter_stream.insert_one(row)
        return post_id

if __name__ == "__main__":
    db = Database()
    #db.insertRow({'text':'test'})
    db.getRow()

