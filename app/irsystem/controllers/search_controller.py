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

project_name = "BookRec"
net_id = "Hyun Kyo Jung: hj283"

# @irsystem.route('/', methods=['GET'])
# def delandadd():
# 	empty_db()
# 	create_tables()
# 	put_words_in_db()
# 	put_books_in_db()
# 	word_cloud_message = ''
# 	top_books_message = ''
# 	word_cloud = ['successfully added']
# 	top_books = ['successfully added']
# 	available_words = []
# 	available_books = []
# 	return render_template('search.html', name=project_name, netid=net_id, word_cloud_message=word_cloud_message, top_books_message=top_books_message, word_cloud=word_cloud, top_books = top_books)

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


@irsystem.route('/', methods=['GET'])
def search(hash_factor = 1):
	available_words = json.load(open('words.json'))
	available_words = [unicodedata.normalize('NFKD', w).encode('ascii','ignore') for w in available_words]
	available_books = json.load(open('books.json'))
	available_books = [unicodedata.normalize('NFKD', b).encode('ascii','ignore') for b in available_books]

	#author_input = request.args.get('author_search')
	title_input = request.args.get('title_search')
	keyword_input = request.args.get('keyword_search') 

	book_to_index = json.load(open("book_to_index.json"))
	book_to_index = {key.strip() : value for key, value in book_to_index.iteritems()}


	word_to_index = json.load(open("word_to_index.json"))
	book_image_url =json.load(open("ISBN_100000_to_200000.json"))
	print('all the files opened!')

	#print(len(Word.query.all()))

	if title_input == None and keyword_input == None:
		word_cloud_message = ''
		top_books_message =  ''
		word_cloud = []
		top_books = []

	elif keyword_input is not None: 
		word_cloud_message = ''
		word_cloud = []
		top_books = []
		keywords = keyword_input.split(',')
		rel_keywords = []
		for keyword in keywords:
			if keyword not in word_to_index.keys():
				top_books.append(keyword + " is not in our database.")
			else:
				rel_keywords.append(keyword)
		if len(top_books) == len(keywords): 
			top_books_message = 'All the keywords are not in our database.'
		else:
			top_books_message = "Top 10 books for the keyword are:"
			word_list = []
			ith_list = []
			print(keyword_input)
			for keyword in rel_keywords:
				print(keyword_input)
				i = word_to_index[keyword]
				w = Word.query.filter_by(index = int(i)).first()
				word_list.append(w)
				ith_list.append(int(i)) 
			for close_book in pre_db_word_to_closest_books(word_list, ith_list):
				book_title = close_book[0]
				each_book_list =[]
				each_book_list.append(book_title)
				if close_book in book_image_url:
					print("hellothere")
					isbn= book_image_url[close_book]
					print("notisbn")
					newisbn =[]
					for nums in isbn[:2] : 
						url = "http://covers.openlibrary.org/b/isbn/" + nums +"-M.jpg"
						url=url.encode('ascii','ignore')
						print(url)
						newisbn.append(url)
					link=isbn[2].encode('ascii','ignore')
					link ="http://www.goodreads.com/book/show/" + link
					newisbn.append(link)
					for nounicode in newisbn: 
						each_book_list.append(nounicode)

					each_book_list.append([])
				else: 
					errorlist = [None ,None , None ]
					each_book_list += errorlist
					
				top_books.append(each_book_list)

	else:
		top_books_message = ""
		top_books = []

		if title_input not in book_to_index.keys():
			word_cloud_message = ''
			word_cloud = ['The book is not in our database.']
		else:
			i = book_to_index[title_input]
			b = Books.query.filter_by(start_index = int(i)/hash_factor*hash_factor).first()
			word_cloud_message = 'Word cloud is: '	
			word_cloud = pre_db_book_to_closest_words(b, int(i) % hash_factor)
	return render_template('search.html', name=project_name, netid=net_id, word_cloud_message=word_cloud_message, top_books_message=top_books_message, word_cloud=word_cloud, top_books = top_books, avail_keywords = available_words, avail_books = available_books)
