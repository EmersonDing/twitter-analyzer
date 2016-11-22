"""
This file is for extract important word from a sentence
"""

import nltk
from nltk.corpus import treebank

class Keyword:
    def __init__(self):
        self.stopWordList = set()           # stop word list
        f = open('StopWord.txt', 'r')
        for line in f:
            line = line[:-1]                # remove '\n'
            self.stopWordList.add(line)

    """
    extract import word from sentence
    """
    def getKeyword(self, sentence):
        words = []                              # create word list
        tokens = nltk.word_tokenize(sentence)   # tokenize sentence with nltk package
        tagged = nltk.pos_tag(tokens)           # get pos_tag for each word

        ## extract noun. not in use
        # for tag in tagged:
        #     word = tag[0].lower()
        #     if "NN" in tag[1] and word not in self.stopWordList:
        #         words.append(word)

        # extract noun and noun phrase
        word = ""
        index = 0
        check = 0
        while(index < len(tagged)):
            if "NN" in tagged[index][1]:            # extract word with "NN" in pos_tag
                word += tagged[index][0].lower()
                check = index
                while index+1 < len(tagged) and "NN" in tagged[index+1][1]:
                    word += " " + tagged[index+1][0].lower()
                    index += 1
                if "\\" not in word and "/" not in word and "rt" not in word and "@" not in word and "http" not in word:
                    words.append(word.lower())
            index += 1
            word = ""
        return words

if __name__ == "__main__":
    sentence = "Donald Trump is going to win the election!"
    kw = Keyword()
    print(kw.getKeyword(sentence))
