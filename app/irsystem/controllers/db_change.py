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
from app.irsystem.models.words import *
from app.irsystem.models.books import *
from app.irsystem.models.authors import *
from app.irsystem.controllers.db_change import *
from app.irsystem.controllers.db_query import *
import json
import os
import csv
import unicodedata

#change this function to change column values of some table
def change_column_value():
	index_to_book = json.load(open('index_to_book.json'))
	for i in range(55000,59646):
		name = index_to_book[unicode(str(i),'utf-8')]
		book_object = Books.query.filter_by(index = i).first()
		book_object.name = name
		print(i)
	print('done')
	db.session.flush()
	db.session.commit()
	print('55,000 - 59,646 Committed!')

#Empties out all tables within the postgresql database
def empty_db():
	db.reflect()
	db.drop_all()
	print('database wiped!')

#create all tables in the models folder
def create_tables():
	db.create_all()

def put_books_in_db(round):
	#load the files
	d2w_file_string_begin = 'docs_to_words_'
	file_string_end       = '.pkl'
	d2w_file_string       = d2w_file_string_begin + str(round+1) + file_string_end
	docs_to_words = pickle.load(open(d2w_file_string, "rb"))				
	index_to_book = json.load(open("index_to_book.json"))
	book_to_author = json.load(open('book_to_author.json'))
	index_to_word = json.load(open('index_to_word.json'))
	book_info = json.load(open('book_info.json'))
	docs = pickle.load(open('docs.pkl', 'rb'))
	print('files all opened!')

	num_doc = len(docs_to_words)
	row_i = 0
	for i in range(num_doc):
		index = i + 4000 * round 																		
		name = index_to_book[str(i + 4000 * round)]											
		author = book_to_author[name]													
		word_cloud = ''
		for top_word_i in np.argsort(-docs_to_words[i])[:5]:
			word_cloud = word_cloud + '***' + (index_to_word[str(top_word_i)])
		word_cloud = word_cloud[3:]
		row_i += 1
		info_list = book_info[name]
		vector = str(docs[i + 4000 * round].tolist())[1:-1]
		description = info_list[u'description']
		avg_rating = info_list[u'average_rating']
		isbn10 = info_list[u'ISBN10']
		isbn13 = info_list[u'ISBN13']
		link = info_list[u'link']

		#isbn, avg_rating, and description are null for now
		book = Books(index = index, name = name, author = author, word_cloud = word_cloud, description = description, vector = vector, 
			         avg_rating = avg_rating, isbn10 = isbn10, isbn13 = isbn13, link = link)
		db.session.add(book)
	print('done with books!')
	print('last row for the books was %s' % str(row_i + 4000 * round))											


	
#Create a book instance
def put_words_in_db(round):
	#load the files
	w2d_file_string_begin = 'words_to_docs_'
	file_string_end = '.pkl'
	w2d_file_string = w2d_file_string_begin + str(round+1) + file_string_end
	words_to_docs =  pickle.load(open(w2d_file_string, "rb"))										
	index_to_word = json.load(open("index_to_word.json"))
	print('files all opened!')

	num_word = len(words_to_docs)
	row_i = 0
	for i in range(num_word):																		
		index = i + 400 * round																					
		name  = index_to_word[str(i + 400 * round)]																
		book_scores = str(words_to_docs[i].tolist())[1:-1]
		w = Words(index = index, name = name, book_scores = book_scores)
		db.session.add(w)
		row_i += 1

	print('last row for the words was %s' % str(row_i + 400 * round))												
	print('done with words!')



def test1():
	w = Words(index = 0, name = 'warm', book_scores = '12381123897')
	db.session.add(w)

def test2():
	w = Words(index = 1, name = 'cool', book_scores = '239847289')
	db.session.add(w)


