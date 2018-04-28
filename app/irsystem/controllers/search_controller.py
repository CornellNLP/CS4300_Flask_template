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

project_name = "BookRec"
net_id = "Hyun Kyo Jung: hj283"

@irsystem.route('/secondpage', methods=['GET'])
def secondpage():
	return render_template('secondpage.html')


@irsystem.route('/test', methods=['GET'])
def db_test():
	#empty_db()
	#create_tables()
	#test1()
	# test2()
	# print('added!')
	# db.session.commit()
	# print('commited!')
	# print(len(Books.query.filter_by(index=12000).all()))
	# print(len(Words.query.filter_by(index=1200).all()))
	return render_template('secondpage.html')


@irsystem.route('/main', methods=['GET'])
def delandadd():
	#put_words_in_db(10)
	# put_books_in_db(14)
	# db.session.flush()
	# db.session.commit()
	print('committed!')
	word_cloud_message = ''
	top_books_message = ''
	word_cloud = ['successfully added']
	top_books = ['successfully added']
	available_words = []
	available_books = []
	return render_template('search.html', name=project_name, netid=net_id, word_cloud_message=word_cloud_message, top_books_message=top_books_message, word_cloud=word_cloud, top_books = top_books)

# @irsystem.route('/', methods=['GET'])
# def add_words_chunks():
# 	put_books_in_db()
# 	word_cloud_message = ''
# 	top_books_message = ''
# 	word_cloud = ['successfully added']
# 	top_books = ['successfully added']
# 	available_words = []
# 	available_books = []
# 	return render_template('search.html', name=project_name, netid=net_id, word_cloud_message=word_cloud_message, top_books_message=top_books_message, word_cloud=word_cloud, top_books = top_books)

# @irsystem.route('/secondpage', methods=['GET'])
# def secondpage():
# 	return render_template("secondpage.html")
	
# @irsystem.route('/main', methods=['GET'])
# def search():
# 	#opening files and processing. Delete if not needed.
# 	available_words = json.load(open('words.json'))
# 	available_words = [unicodedata.normalize('NFKD', w).encode('ascii','ignore') for w in available_words]
# 	available_books = json.load(open('books.json'))
# 	available_books = [unicodedata.normalize('NFKD', b).encode('ascii','ignore') for b in available_books]
# 	title_input = request.args.get('title_search')
# 	keyword_input = request.args.get('keyword_search')
# 	book_to_index = json.load(open("book_to_index.json"))
# 	book_to_index = {key.strip() : value for key, value in book_to_index.iteritems()}
# 	word_to_index = json.load(open("word_to_index.json"))
# 	book_image_url =json.load(open("ISBN_100000_to_200000.json"))

# 	#USER hit the go button!
# 	if keyword_input is not None or title_input is not None:
# 		word_cloud_message = ''
# 		word_cloud = []
# 		top_books = []
# 		keywords = keyword_input.split(',')
# 		rel_keywords = []
# 		for keyword in keywords:
# 			if keyword not in word_to_index.keys():
# 				top_books.append(keyword + " is not in our database.")
# 			else:
# 				rel_keywords.append(keyword)
# 		if len(top_books) == len(keywords):
# 			top_books_message = 'All the keywords are not in our database.'
# 		else:
# 			top_books_message = "Top 10 books for the keyword are:"
# 			word_list = []
# 			ith_list = []
# 			for keyword in rel_keywords:
# 				i = word_to_index[keyword]
# 				w = Word.query.filter_by(index = int(i)).first()
# 				word_list.append(w)

# 				ith_list.append(int(i)) 
# 			for close_book in pre_db_word_to_closest_books(word_list, ith_list):
# 				book_title = close_book[0]
# 				each_book_list =[]
# 				each_book_list.append(book_title)
# 				if close_book in book_image_url:
# 					print("hellothere")
# 					isbn= book_image_url[close_book]
# 					print("notisbn")
# 					newisbn =[]
# 					for nums in isbn[:2] :
# 						url = "http://covers.openlibrary.org/b/isbn/" + nums +"-M.jpg"
# 						url=url.encode('ascii','ignore')
# 						print(url)
# 						newisbn.append(url)
# 					link=isbn[2].encode('ascii','ignore')
# 					link ="http://www.goodreads.com/book/show/" + link
# 					newisbn.append(link)
# 					for nounicode in newisbn:
# 						each_book_list.append(nounicode)

# 					each_book_list.append([])
# 				else:
# 					errorlist = [None ,None , None ]
# 					each_book_list += errorlist

# 				top_books.append(each_book_list)

# 	else:
# 		top_books_message = ""
# 		top_books = []

# 		if title_input not in book_to_index.keys():
# 			word_cloud_message = ''
# 			word_cloud = ['The book is not in our database.']
# 		else:
# 			i = book_to_index[title_input]
# 			b = Books.query.filter_by(index = int(i)).first()
# 			word_cloud_message = 'Word cloud is: '	
# 			word_cloud = pre_db_book_to_closest_words(b, int(i))
# 	return render_template('search.html', name=project_name, netid=net_id, word_cloud_message='', top_books_message='', word_cloud=[], top_books = [], avail_keywords = available_words, avail_books = available_books)
