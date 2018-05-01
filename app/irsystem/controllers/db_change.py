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
def change_b2w_value(version):
	first = 'docs_to_words_'
	end = '.pkl'
	final = first + str(version) + end
	book_to_word  = pickle.load(open(final, 'rb'))
	offset = 5000*(version-1)
	for i in range(0,5000):
		#name = index_to_book[unicode(str(i+offset),'utf-8')]
		book_object = Books.query.filter_by(index = i+offset).first()
		book_object.word_scores = str(book_to_word[i].tolist())[1:-1]

	print('b2w done')
	offset += 5000
	print('last one is {}'.format(str(offset)))
	db.session.flush()
	db.session.commit()
	print('b2w Committed!')

	#change this function to change column values of some table
def change_w2b_value(version):
	first = 'words_to_docs_'
	end = '.pkl'
	final = first + str(version) + end
	word_to_book = pickle.load(open(final, 'rb'))
	offset = 400*(version-1)
	for i in range(0,400):
		#name = index_to_book[unicode(str(i+offset),'utf-8')]
		word_object = Words.query.filter_by(index = i+offset).first()
		word_object.book_scores = str(word_to_book[i].tolist())[1:-1]

	print('w2b done')
	offset += 400
	print('last one is {}'.format(str(offset)))
	db.session.flush()
	db.session.commit()
	print('w2b Committed!')

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
	index_to_book = json.load(open("index_to_book.json"))
	book_info = json.load(open('book_info.json'))
	docs = pickle.load(open('docs.pkl', 'rb'))
	print('files all opened!')

	num_doc = len(docs)
	row_i = 0
	for i in range(6000*(round-1),num_doc):
		unicode_index = unicode(str(i),'utf-8')
		name = index_to_book[unicode_index][:index_to_book[unicode_index].rfind(' (published by)')]
		author = name[name.rfind('(by)')+5:]
		info_list = book_info[index_to_book[unicode_index]]
		vector = str(docs[i].tolist())[1:-1]
		description = info_list[u'description']
		avg_rating = info_list[u'average_rating']
		isbn10 = info_list[u'ISBN10']
		isbn13 = info_list[u'ISBN13']
		link = info_list[u'link']
		row_i = i+1
		book = Books(index = i, name = name, author = author, description = description, vector = vector, 
			         avg_rating = avg_rating, isbn10 = isbn10, isbn13 = isbn13, link = link)
		db.session.add(book)
	print('done with books!')
	print('last row for the books was %s' % str(row_i))											

	
#Create a book instance
def put_words_in_db(round):
	#load the files
	words 		  = pickle.load(open('words.pkl')) 
	index_to_word = json.load(open("index_to_word.json"))
	print('files all opened!')

	num_word = len(words)
	row_i = 0
	for i in range(500*(round-1),num_word):		
		name  = index_to_word[unicode(str(i),'utf-8')]													
		vector = str(words[i].tolist())[1:-1]
		w = Words(index = i, name = name, vector = vector)
		db.session.add(w)
		row_i = i+1
	print('done with words!')
	print('last row for the words was %s' % str(row_i))												



def test1():
	w = Words(index = 0, name = 'warm', book_scores = '12381123897')
	db.session.add(w)

def test2():
	w = Words(index = 1, name = 'cool', book_scores = '239847289')
	db.session.add(w)


