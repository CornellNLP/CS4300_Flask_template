from . import *  
import numpy as np 
import pickle 
import numpy as np 
import json
#import zipfile
#import Collections 
from sklearn.preprocessing import normalize
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
####
from app.irsystem.models.words import *
from app.irsystem.models.books import *
import json
import os
import csv
import unicodedata

project_name = "BookRec"
net_id = "Hyun Kyo Jung: hj283"


def db_word_to_closest_books(word, ith, k = 15):
	avg_word = np.zeros(100)
	for w, i in zip(word, ith):
		np_word = np.fromstring(w.vectors, sep= ', ')
		td_np_word = np.reshape(np_word, (100,100))
		np_word = td_np_word[i]
		avg_word += np_word
	avg_word /= len(word)
	print('before query')
	query_result = Books.query.all()
	print('after query')
	dot_products = np.zeros(len(query_result*100))
	print('before processing')
	for book in query_result:
		np_book = np.fromstring(book.vectors, sep = ', ')
		num_books = len(np_book) / 100
		td_np_book = np.reshape(np_book, (num_books, 100))
		dot_prod = np.dot(td_np_book, avg_word)
		for i in range(num_books):
			dot_products[book.start_index + i] = dot_prod[i]
	print('after processing')

	dot_products = np.absolute(dot_products)
	asort = np.argsort(-dot_products)[:k+1]

	top_k_books = []
	top_k_sim_scores = []
	for i in asort[1:]:
		near_names = Books.query.filter_by(start_index = i/100*100).first().names
		name = near_names.split('***')[i % 100]
		name =name.encode('ascii','ignore')
		top_k_books.append(name)
		top_k_sim_scores.append(dot_products[i]/dot_products[asort[0]])
	return top_k_books

def db_book_to_closest_words(book, ith, k = 5):
	np_book = np.fromstring(book.vectors, sep= ', ')
	td_np_book = np.reshape(np_book, (100,100))
	np_book = td_np_book[ith]
	query_result = Words.query.all()
	dot_products = np.zeros(len(query_result*100))
	for word in query_result:
		np_word = np.fromstring(word.vectors, sep = ', ')
		num_words = len(np_word) / 100
		td_np_word = np.reshape(np_word, (num_words, 100))
		dot_prod = np.dot(td_np_word, np_book)
		for i in range(num_words):
			dot_products[word.start_index + i] = dot_prod[i]
	asort = np.argsort(-dot_products)[:k+1]

	top_k_words = []
	for i in asort[1:]:
		near_names = Words.query.filter_by(start_index = i/100*100).first().names
		name = near_names.split('***')[i % 100]
		top_k_words.append((name, dot_products[i]/dot_products[asort[0]]))
	return top_k_words

#Empties out all tables within the postgresql database
def empty_db():
	db.reflect()
	db.drop_all()
	print('database wiped!')

#create all tables in the models folder
def create_tables():
	db.create_all()

#Create a book instance
def put_books_in_db(hash_factor = 100):
	#load the files
	docs_compressed = pickle.load(open("docs.pkl", "rb"))

	index_to_book = json.load(open("index_to_book.json"))
	words_compressed = pickle.load(open("words.pkl", "rb"))
	index_to_word = json.load(open("index_to_word.json"))
	print('files all opened!')

	num_doc = len(docs_compressed)
	row_i = 0
	while row_i < num_doc:
		i = 0
		hundred_vectors = ''
		hundred_names   = ''
		while row_i + i < num_doc and i < hash_factor:
			if i == 0:
				hundred_vectors += str(docs_compressed[row_i + i].tolist())[1:-1]
				hundred_names += index_to_book[str(row_i + i)]
			else:
				hundred_vectors = hundred_vectors + ', ' + str(docs_compressed[row_i + i].tolist())[1:-1]
				hundred_names = hundred_names + '***' + index_to_book[str(row_i + i)]
			i+=1
		b = Books(start_index = row_i, names = hundred_names, vectors = hundred_vectors)
		db.session.add(b)
		row_i += i
	print('done with books!')
	print('last row i was %s' % str(row_i-1))

	num_word = len(words_compressed)
	row_i = 0
	while row_i < num_word:
		i = 0
		hundred_vectors = ''
		hundred_names   = ''
		while row_i + i < num_word and i < hash_factor:
			if i == 0:
				hundred_vectors += str(words_compressed[row_i + i].tolist())[1:-1]
				hundred_names += index_to_word[str(row_i + i)]
			else:
				hundred_vectors = hundred_vectors + ', ' + str(words_compressed[row_i + i].tolist())[1:-1]
				hundred_names = hundred_names + '***' + index_to_word[str(row_i + i)]
			i+=1
		w = Words(start_index = row_i, names = hundred_names, vectors = hundred_vectors)
		db.session.add(w)
		row_i += i
	print('done with words!')

	db.session.commit()
	print('commited!')


@irsystem.route('/', methods=['GET'])
def delandadd():
	empty_db()
	create_tables()
	put_books_in_db()
	word_cloud_message = ''
	top_books_message = ''
	word_cloud = ['successfully added']
	top_books = ['successfully added']
	available_words = []
	available_books = []
	return render_template('search.html', name=project_name, netid=net_id, word_cloud_message=word_cloud_message, top_books_message=top_books_message, word_cloud=word_cloud, top_books = top_books)


# @irsystem.route('/', methods=['GET'])
# def search():
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



# 	if title_input == None and keyword_input == None:
# 		word_cloud_message = ''
# 		top_books_message =  ''
# 		word_cloud = []
# 		top_books = []

# 	elif keyword_input is not None: 
# 		word_cloud_message = ''
# 		word_cloud = []
# 		top_books = []
# 		keywords = keyword_input.split(' ')
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
# 			print(keyword_input)
# 			for keyword in rel_keywords:
# 				i = word_to_index[keyword]
# 				w = Words.query.filter_by(start_index = int(i)/100*100).first()
# 				word_list.append(w)
# 				ith_list.append(int(i)%100) 
# 			for close_book in db_word_to_closest_books(word_list, ith_list):
# 				each_book_list =[]
# 				each_book_list.append(close_book)
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
# 					errorlist = ["", "",""]
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
# 			b = Books.query.filter_by(start_index = int(i)/100*100).first()
# 			word_cloud_message = 'Word cloud is: '	
# 			word_cloud = db_book_to_closest_words(b, int(i) % 100)
# 	return render_template('search.html', name=project_name, netid=net_id, word_cloud_message=word_cloud_message, top_books_message=top_books_message, word_cloud=word_cloud, top_books = top_books, avail_keywords = available_words, avail_books = available_books)
