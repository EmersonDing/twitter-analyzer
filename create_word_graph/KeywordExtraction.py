"""
This file is for extract important word from a sentence
"""

import nltk
from nltk.corpus import treebank

class Keyword:
    def __init__(self):
        self.stopWordList = set()          # stop word list
        f = open('StopWord.txt', 'r')
        for line in f:
            line = line[:-1]            # remove '\n'
            self.stopWordList.add(line)

    def getKeyword(self, sentence):
        words = []
        tokens = nltk.word_tokenize(sentence)
        tagged = nltk.pos_tag(tokens)

        # extract noun
        # for tag in tagged:
        #     word = tag[0].lower()
        #     if "NN" in tag[1] and word not in self.stopWordList:
        #         words.append(word)

        # extract noun and noun phrase
        word = ""
        index = 0
        check = 0
        while(index < len(tagged)):
            if "NN" in tagged[index][1]:
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
