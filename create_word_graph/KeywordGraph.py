"""
create keyword graph based on twitters
"""

import sys
import time
from create_word_graph.ConnectMongoDB import *
from create_word_graph.KeywordExtraction import *

chunkSize = 10000       # number of rows of twitter read from database each time
dictSize = 20000        # maxinum size of dict that saves keyword

class CreateGraph:
    def __init__(self):
        self.keywordExtration = Keyword()   # keyword_extraction object
        self.db = Database()                # database object
        self.dict = {}                      # dictionary to save temperory graph before inserting graph directly into mongodb
        self.data = []                      # twitter data

    # insert graph in dict into database
    def insertDictIntoGraph(self):
        for i in self.dict:
            for j in self.dict[i]:
                self.db.insertKeywordGraph(i, j, self.dict[i][j])
        self.dict.clear()      # clear dict

    # main function to create graph. read twitter from mongodb, and do keyword extraction
    # then update dict. insert dict into mongodb when dict over the size limit
    def createGraph(self):
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
                # for each word in wordList, rest of the words in wordList will be its neighbor
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
    start_time = time.time()    # calculate program running time
    graph = CreateGraph()
    graph.createGraph()
    print("time elapsed: {:.2f}s".format(time.time() - start_time))
