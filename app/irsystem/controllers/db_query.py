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
def word_to_closest_books(words):
	keyword_query_objects = [Words.query.filter_by(name = word).first() for word in words.split(',')] ###this delimeter might change
	sum_sim_scores = np.zeros(len(np.fromstring(keyword_query_objects[0].book_scores, sep = ', ')))
	for keyword in keyword_query_objects:
		sum_sim_scores += np.fromstring(keyword.book_scores, sep=', ')
	return sum_sim_scores

#book: user's book title input
def book_to_closest_books(book):
	book_query_object = Books.query.filter_by(name=book).first()
	return np.fromstring(book_query_object.book_scores, sep=', ')

def combine_result(scores_from_word_input, scores_from_book_input, k = 15):
	sum_scores = np.zeros(len(scores_from_book_input)) + scores_from_book_input + scores_from_word_input
	asort = np.argsort(-sum_scores)[:k]
	top_k_books = []
	for i in asort:
		book_list = []
		book_query_object = Books.query.filter_by(index = i).first()
		book_list.append(book_query_object.name)
		book_list.append(book_query_object.ISBN10)
		book_list.append(book_query_object.ISBN13)
		book_list.append(book_query_object.link)
		top_k_books.append(book_list)
	return top_k_books

def book_to_closest_words(book, k = 5):
	sim_scores = np.fromstring(book.word_scores, sep= ', ')
	top_k_words = []
	for i in np.argsort(-sim_scores)[:k]:
		top_k_words.append(Words.query.filter_by(index = i).first().name)
	return top_k_words
