from ConnectMongoDB import *
from KeywordExtraction import *
from pymongo import MongoClient

class CreateGraph:
    def __init__(self):
        self.keywordExtration = Keyword()
        self.db = Database()
        self.dict = {}
        self.data = []

    def getDataFromDatabase(self):
        data = list(self.db.getRow("twitter_stream"))
        for line in data:
            wordList = self.keywordExtration.getKeyword(str(line))
            print(wordList)

    def getKeyword(self, ):
        keyword = []
        for line in self.data:
            print(line)
            # keyword = self.keywordExtration(line)
            # print(keyword)



if __name__ == "__main__":
    graph = CreateGraph()
    graph.getDataFromDatabase()
