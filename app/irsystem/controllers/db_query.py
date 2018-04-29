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
from app.irsystem.models.words import *
from app.irsystem.models.books import *
from app.irsystem.models.authors import *
from app.irsystem.controllers.db_change import *
from app.irsystem.controllers.db_query import *
import json
import os
import csv
import unicodedata


#words: user's keyword input! 
def word_to_closest_books(words, length = 59646):
	print('input to word_to_closest_books is : {}'.format(words))
	if words == '':
		return np.zeros(length)
	print(words.split(';'))
	keyword_query_objects = [Words.query.filter_by(name = word).first() for word in words.split(';')] ###this delimeter might change
	print(keyword_query_objects)
	sum_sim_scores = np.zeros(length)
	for keyword in keyword_query_objects:
		sum_sim_scores += np.fromstring(keyword.book_scores, sep=', ')
	return sum_sim_scores/len(words.split(';'))

#book: user's book title input
def book_to_closest_books(book, length = 59646):
	print('input to book_to_closest_books is : {}'.format(type(book)))
	if book == '':
		return np.zeros(length)
	book_query_object = Books.query.filter_by(name=book).first()
	book_vector = np.fromstring(book_query_object.vector, sep=', ')
	sim_scores = np.zeros(length)
	for book in Books.query.all():
		index = book.index
		ith_book_vector = np.fromstring(book.vector, sep = ', ')
		sim_scores[index] = ith_book_vector.dot(book_vector)
	return sim_scores

def combine_two_scores(scores_from_word_input, scores_from_book_input, k = 15):	
	print('entered combined_two_scores method')
	sum_scores = np.zeros(len(scores_from_book_input)) + scores_from_book_input + scores_from_word_input
	if (scores_from_book_input[0] != 0.0 and scores_from_word_input[0] != 0.0): sum_scores /= 2
	asort = np.argsort(-sum_scores)
	#When there's a book input, we will exclude the book itself (need the while loop since there might be mutliple) 
	if scores_from_book_input[0] != 0.0:
		print('inside first if statement')
		index = 1
		prev = sum_scores[asort[index-1]]
		curr = sum_scores[asort[index]]
		while prev == curr:
			print('inside the first while loop')
			index += 1
			prev = sum_scores[asort[index-1]]
			curr = sum_scores[asort[index]]
		asort = asort[index:]
	#exluding the same books (those with the same exact similarity scores)	
	length = 0
	new_asort = []
	prev = -1
	index = 0
	while length < k:
		print('inside the second while loop')
		if sum_scores[asort[index]] != prev:
			new_asort.append((asort[index], round(sum_scores[asort[index]], 4)*100))
			length += 1
		prev = sum_scores[asort[index]]
		index += 1
	return new_asort

def get_books(asorted_list):
	print('entered get_books method')
	top_k_books = []
	for tup in asorted_list:
		book_list = []
		book_query_object = Books.query.filter_by(index = tup[0]).first()
		book_list.append(book_query_object.name)							##1. Bookname
		book_list.append(book_query_object.isbn10)							##2. ISBN10
		book_list.append(book_query_object.isbn13)							##3. ISBN13
		book_list.append(book_query_object.link)							##4. Link
		book_list.append(book_query_object.author)							##5. author
		book_list.append(book_query_object.description)						##6. description
		book_list.append(book_query_object.word_cloud.split('***'))			##7. word cloud
		book_list.append(book_query_object.avg_rating)						##8. average rating
		book_list.append(tup[1])											##9. Similarity Score
		top_k_books.append(book_list)
	return top_k_books

def book_to_closest_words(book, k = 100):
	sim_scores = np.fromstring(book.word_scores, sep= ', ')
	top_k_words_tup = []
	asorted = np.argsort(-sim_scores)[:k]
	for i in asorted:
		top_k_words_tup.append((Words.query.filter_by(index = i).first().name, round(sim_scores[i], 2)))
	return top_k_words_tup
