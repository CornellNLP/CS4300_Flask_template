### Utils

## This is a list of files that will deal with our dataset from the raw 30 GB files to a cohesive dataset

* ```parserv2.py``` there is no v1 because that was a terrible parser. This file takes in a single parameter, ```filename``` which is the raw, unprocessed file downloaded from [https://files.pushshift.io/reddit/comments/]. it will return a ```.json``` file in the same directory of the same name as the filename.

* ```subset_parser.py``` will parse all files of a given directory, which are ideally parsed JSONs from ```parserv2.py```. Basically it reads each file in the directory and overwrites it. Generally this will be used to further filter out stuff but don't want to wait another 30 minutes to run ```parserv2.py```

* ```vectorizer.py``` parses all file of a given directory into one large inverted index file and saves the entire dictionary as a pkl file.

* ```vectorizerv2.py``` parses all files of a given directory into separate pkl files, one per word in the directory ```data/``` DONT USE THIS UNLESS YOU WANT TO FUCK UP YOUR HARD DRIVE


* ```tfidf_calculator.py``` calculates tf/idf values. **REQUIRES ```inv_index.pkl```, run ```vectorizer.py``` first** as the pkl file is gitignored!

Generally, the order would be to parse all raw files first using ```parserv2.py``` >> run ```subset_parser.py``` on directory with all parsed files, then a ```vectorizer``` script on the same directory, and also to run ```populate_db.py```



### Database setup

* Our database on GCP is at ```"postgresql://postgres:alpine@35.188.248.54:5432/learnddit"```. Add your IP to "Authorizations" on the SQL page.

* Add that URL to config settings as ```DATABASE_URL```

* Run the three commands in the README (```python manage.py db init```, ```python manage.py db migrate```, ```python manage.py db upgrade```)

* ```populate_db.py``` parses all files of a given directory into the comments DB, parsing the comments of JSON format and ```INSERT``` it in the DB. This takes a while. Like leave this running overnight.

* https://cloud.google.com/sql/docs/postgres/connect-admin-ip
