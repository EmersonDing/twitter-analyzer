# Twitter-Analyzer
### What's Twitter Analyzer?
There're two major functions of twitter analyzer. The first one is stream data analysis. With tweey api, twitter_analyzer can get twitter stream data from twitter database, and the system will save data in Redis, and then parse and analyze data, eventually show the statistic result.
The second function is keyword graph analysis based on offline data. System will save twitter data into a local mongodb, and extract keyword from each twitter, and create a keyword graph, e.g. for a twitter "Donald Trump has won the election over Hilary Clinton with 4 points.", keyword like "Donald Trump", "election" and "Hilary Clinton" will be extracted, and a connected graph with these three keyword as nodes will be build and saved. And for the second part of the system, when a user search for "Donald Trump", system will show the neighbors of this keyword, in this case it will be "Hilary Clinton", "election" and their frequency, and user can choose the topic he's interested. With another click to "Hilary Clinton", system will show all of the twitters related to both "Donald Trump" and "Hilary Clinton". 

### Directory
master branch contains web2py code
Nan branch contains keyword_graph code
