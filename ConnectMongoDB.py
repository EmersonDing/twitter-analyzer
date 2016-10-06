"""
This file connect with local MongoDB
"""

from pymongo import MongoClient

class Database:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.test
        self.collection = self.db.foo

    def getOneRow(self):
        print(self.collection.find_one())

if __name__ == "__main__":
    db = Database()
    db.getOneRow()

