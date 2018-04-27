##############
#This file contains the functions that interact with the db to put new data, delete all data etc
##############

from . import *  
import numpy as np 
import pickle 
import numpy as np 
import json
from sklearn.preprocessing import normalize
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.models.word import *
from app.irsystem.models.books import *
from app.irsystem.models.authors import *
from app.irsystem.controllers.db_change import *
from app.irsystem.controllers.db_query import *
import json
import os
import csv
import unicodedata

#Empties out all tables within the postgresql database
def empty_db():
	db.reflect()
	db.drop_all()
	print('database wiped!')

#create all tables in the models folder
def create_tables():
	db.create_all()

def put_authors_in_db(hash_factor = 10):
	#load the files 
	author_to_book = json.load(open("authors_to_books.json"))
	author_to_index = json.load(open("author_to_index.json"))



	db.session.commit()
	print("commited")

def put_books_in_db(hash_factor = 100):
	#load the files
	docs_to_words = pickle.load(open("docs_to_words_15.pkl", "rb"))						#1
	index_to_book = json.load(open("index_to_book.json"))
	print('files all opened!')

	num_doc = len(docs_to_words)
	row_i = 0
	while row_i < num_doc:
		i = 0
		hundred_scores = ''
		hundred_names   = ''
		while row_i + i < num_doc and i < hash_factor:
			if i == 0:
				hundred_scores += str(docs_to_words[row_i + i].tolist())[1:-1]
				hundred_names += index_to_book[str(row_i + i + 56000)]					#2
			else:
				hundred_scores = hundred_scores + ', ' + str(docs_to_words[row_i + i].tolist())[1:-1]
				hundred_names = hundred_names + '***' + index_to_book[str(row_i + i + 56000)] 	#3
			i+=1
		b = Books(start_index = row_i + 56000, names = hundred_names, word_scores = hundred_scores)		#4
		db.session.add(b)
		row_i += i
	print('done with books!')
	print('last row i was %s' % str(row_i + 56000))							#5
	db.session.commit()
	print('commited!')

#Create a book instance
def put_words_in_db(hash_factor = 1):
	#load the files
	words_to_docs =  pickle.load(open("words_to_docs_11.pkl", "rb"))										#1
	words_to_words = pickle.load(open("w2w.pkl", "rb"))
	index_to_word = json.load(open("index_to_word.json"))
	print('files all opened!')

	num_word = len(words_to_docs)
	for i in range(num_word):																		
		index = i + 4000																					#2
		name  = index_to_word[str(i + 4000)]																#3
		book_scores = str(words_to_docs[i].tolist())[1:-1]
		word_scores = str(words_to_words[i + 4000].tolist())[1:-1] 										#4
		w = Word(index = index, name = name, book_scores = book_scores, word_scores = word_scores)
		db.session.add(w)
		print(index)

	print('done with words!')
	db.session.commit()
	print('commited!')

