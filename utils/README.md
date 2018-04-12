### Utils

## This is a list of files that will deal with our dataset from the raw 30 GB files to a cohesive dataset

* ```parserv2.py``` there is no v1 because that was a terrible parser. This file takes in a single parameter, ```filename``` which is the raw, unprocessed file downloaded from [https://files.pushshift.io/reddit/comments/]. it will return a ```.json``` file in the same directory of the same name as the filename.

* ```subset_parser.py``` will parse all files of a given directory, which are ideally parsed JSONs from ```parserv2.py```. Basically it reads each file in the directory and overwrites it. Generally this will be used to further filter out stuff but don't want to wait another 30 minutes to run ```parserv2.py```

* ```vectorizer.py``` parses all file of a given directory into one large inverted index file and saves the entire dictionary as a pkl file.

* ```vectorizerv2.py``` parses all files of a given directory into separate pkl files, one per word in the directory ```data/```

* ```populate_db.py``` parses all files of a given directory into the comments DB, parsing the comments of JSON format and ```INSERT``` it in the DB