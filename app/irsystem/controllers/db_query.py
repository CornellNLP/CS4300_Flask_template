############
#This file contains functions that drive user's search by querying the database
############

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

def pre_db_word_to_closest_books(word, ith, k = 15):
	#this can be better
	length = len(np.fromstring(word[0].book_scores, sep= ', '))
	avg_word = np.zeros(length)
	for w, i in zip(word, ith):
		np_word = np.fromstring(w.book_scores, sep= ', ')
		avg_word += np_word
	avg_word /= len(word)
	#argsort avg_word and take top  k 
	avg_word = np.absolute(avg_word)
	asort = np.argsort(-avg_word)[:k+1]
	
	top_k_books = []
	#do we still have to do this? excluding the first one 
	for i in asort[1:]:
		near_names = Books.query.filter_by(start_index = i/100*100).first().names
		name = near_names.split('***')[i % 100]
		name = name.encode("ascii", "ignore") 
		top_k_books.append((name, avg_word[i]/avg_word[asort[0]]))
	return top_k_books

def pre_db_book_to_closest_words(book, ith, k = 5):
	book_to_word_scores = np.fromstring(book.word_scores, sep= ', ')
	two_d_scores = np.reshape(book_to_word_scores, (100,100))
	book_to_word_scores = two_d_scores[ith]

	asort = np.argsort(-book_to_word_scores)[:k+1]
	top_k_words = []
	for i in asort[1:]:
		name = Word.query.filter_by(index = i).first().name
		top_k_words.append((name, book_to_word_scores[i]/book_to_word_scores[asort[0]]))
	return top_k_words

	# query_result = Word.query.all()
	# dot_products = np.zeros(len(query_result*100))
	# for word in query_result:
	# 	np_word = np.fromstring(word.vectors, sep = ', ')
	# 	num_words = len(np_word) / 100
	# 	td_np_word = np.reshape(np_word, (num_words, 100))
	# 	dot_prod = np.dot(td_np_word, book_to_word_scores)
	# 	for i in range(num_words):
	# 		dot_products[word.start_index + i] = dot_prod[i]
	# asort = np.argsort(-dot_products)[:k+1]

	# top_k_words = []
	# for i in asort[1:]:
	# 	near_names = Word.query.filter_by(start_index = i/100*100).first().names
	# 	name = near_names.split('***')[i % 100]
	# 	top_k_words.append((name, dot_products[i]/dot_products[asort[0]]))
	# return top_k_words
