import time

from create_word_graph.ConnectMongoDB import *
from create_word_graph.KeywordExtraction import *
import sys

chunkSize = 10000       # number of rows of twitter read from database each time
dictSize = 20000        # maminum size of dict that saves keyword

class CreateGraph:
    def __init__(self):
        self.keywordExtration = Keyword()
        self.db = Database()
        self.dict = {}
        self.data = []

    def insertDictIntoGraph(self):
        for i in self.dict:
            for j in self.dict[i]:
                self.db.insertKeywordGraph(i, j, self.dict[i][j])
        self.dict.clear()      # clear dict

    def getDataFromDatabase(self):
        totalTwitterCollectionSize = self.db.getTwitterCollectionSize()
        chunkCount = int(totalTwitterCollectionSize/chunkSize)
        start = 0
        end = min(start + chunkSize, totalTwitterCollectionSize)
        for i in range(0, chunkCount+1):
            data = list(self.db.getTwitterText("twitter_stream", start, end))
            for line in data:
                if len(self.dict) > dictSize:
                    CreateGraph.insertDictIntoGraph(self)
                wordList = self.keywordExtration.getKeyword(str(line))
                for word in wordList:
                    for word2 in wordList:
                        if word != word2:
                            if word in self.dict:
                                if word2 in self.dict[word]:
                                    self.dict[word][word2] += 1
                                else:
                                    self.dict[word][word2] = 1
                            else:
                                self.dict[word] = {}
                                self.dict[word][word2] = 1
            if len(self.dict) != 0:
                CreateGraph.insertDictIntoGraph(self)   # insert dict into database
            start = chunkSize*i
            end = min(start + chunkSize, totalTwitterCollectionSize)
            # print(self.dict)
            print(sys.getsizeof(self.dict))

if __name__ == "__main__":
    start_time = time.time()

    graph = CreateGraph()
    graph.getDataFromDatabase()

    print("time elapsed: {:.2f}s".format(time.time() - start_time))
