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
from app.irsystem.models.word import *
from app.irsystem.models.book import *
import json
import os
import csv

project_name = "BookRec"
net_id = "Hyun Kyo Jung: hj283"

def closest_books_to_word(word_in, word_to_index, index_to_book, words_compressed, docs_compressed, k = 15):
    if word_in not in word_to_index: return ["Not in vocab."] 
    sims = docs_compressed.dot(words_compressed[int(word_to_index[word_in]),:])
    asort = np.argsort(-sims)[:k+1]
    return [(index_to_book[str(i)],sims[i]/sims[asort[0]]) for i in asort[1:]]

def create_books_to_wordcloud(title_in, index_to_word, book_to_index, words_compressed , docs_compressed, k = 5):
    if str(title_in) not in book_to_index: return ["Not in vocab."]
    sims = words_compressed.dot(docs_compressed[int(book_to_index[title_in]),:])
    asort = np.argsort(-sims)[:k+1]
    return [(index_to_word[str(i)],sims[i]/sims[asort[0]])for i in asort[1:]]

# Ability to add multiple words 
def closest_books_to_many_words(word_in, word_to_index, index_to_book, words_compressed , docs_compressed, k = 15):
    msg = ""
    sims = np.zeros(docs_compressed.shape[0])
    count = 0
    for w in word_in:
        if w not in word_to_index: 
        	msg = w + "is not in the vocab"
        else:
            count += 1
            sims += docs_compressed.dot(words_compressed[int(word_to_index[w]),:])
    if count == 0 : return ["None of the words are in our vocab"]
    #sims=sims/count
    asort = np.argsort(-sims)[:k+1] 
    lst = [(index_to_book[str(i)],sims[i]/sims[asort[0]]) for i in asort[1:]]
    lst.append(msg)
    return lst

def db_word_to_closest_books(word, k = 15):
	np_word = np.fromstring(word.vector, sep= ', ')
	print('before query')
	query_result = Book.query.all()
	print('after query')
	dot_products = np.zeros(len(query_result))
	print('before processing')
	for book in query_result:
		np_book = np.fromstring(book.vector, sep = ', ')
		dot_prod = np_word.dot(np_book)
		dot_products[book.index] = dot_prod
	print('after processing')
	asort = np.argsort(-dot_products)[:k+1]
	return [(Book.query.filter_by(index = i).first().name, dot_products[i]/dot_products[asort[0]]) for i in asort[1:]]

def db_book_to_closest_words(book, k = 5):
	np_book = np.fromstring(book.vector, sep= ', ')
	query_result = Word.query.all()
	dot_products = np.zeros(len(query_result))
	for word in query_result:
		np_word = np.fromstring(word.vector, sep = ', ')
		dot_prod = np_book.dot(np_word)
		dot_products[word.index] = dot_prod
	asort = np.argsort(-dot_products)[:k+1]
	return [(Word.query.filter_by(index = i).first().name, dot_products[i]/dot_products[asort[0]]) for i in asort[1:]]

#Empties out all tables within the postgresql database
def empty_db():
	db.reflect()
	db.drop_all()
	print('database wiped!')

#create all tables in the models folder
def create_tables():
	db.create_all()

#Create a book instance
def put_books_in_db():
	#load the files
	docs_compressed = pickle.load(open("docs.pkl", "rb"))
	index_to_book = json.load(open("index_to_book.json"))
	words_compressed = pickle.load(open("words.pkl", "rb"))
	index_to_word = json.load(open("index_to_word.json"))
	print('files all opened!')

	row_i = 0
	for book in docs_compressed:
		v = str(book.tolist())[1:-1] #this will be in the format of '-0.8465, -0.28475, 0.3731, ...'
		b = Book(index = row_i, name = index_to_book[str(row_i)], vector = v)
		db.session.add(b)
		row_i += 1
	print('done with books')

	row_i = 0
	for word in words_compressed:
		v = str(word.tolist())[1:-1] #this will be in the format of '-0.8465, -0.28475, 0.3731, ...'
		w = Word(index = row_i, name = index_to_word[str(row_i)], vector = v)
		db.session.add(w)
		row_i += 1
	print('done with words')

	db.session.commit()
	print('commited!')



# @irsystem.route('/', methods=['GET'])
# def search():
# 	create_tables()
# 	put_books_in_db()


@irsystem.route('/', methods=['GET'])
def search():
	title_input = request.args.get('title_search')
	keyword_input = request.args.get('keyword_search')

	if title_input == None and keyword_input == None:
		print('hey')
		word_cloud_message = ''
		top_books_message =  ''
		word_cloud = []
		top_books = []

	elif keyword_input is not None: 
		print('before query')
		w = Word.query.filter_by(name = keyword_input).first()
		print('after query')
		word_cloud_message = ''
		word_cloud = []
		if w is None: 
			print('hey?')
			top_books_message = ''
			top_books = ["The keyword is not in our database."]
		else:
			top_books_message = "Top 15 books for the keyword are:"
			print('before function call')
			top_books = db_word_to_closest_books(w)
			print('after function call')

	else:
		b = Book.query.filter_by(name = title_input).first()
		top_books_message = ""
		top_books = []
		if b is None:
			word_cloud_message = ''
			word_cloud = ['The book is not in our database.']
		else:
			word_cloud_message = 'Word cloud is: '	
			word_cloud = db_book_to_closest_words(b)

	return render_template('search.html', name=project_name, netid=net_id, word_cloud_message=word_cloud_message, top_books_message=top_books_message, word_cloud=word_cloud, top_books = top_books)



# TODO : need to normalize the docs_compressed 
# @irsystem.route('/', methods=['GET'])
# def search():
# 	###open the files
# 	empty_db()
# 	index_to_book = json.load(open("index_to_book.json"))
# 	index_to_word = json.load(open("index_to_word.json"))	

# 	word_to_index = {value : key for key , value in index_to_word.items()}
# 	book_to_index = {value : key for key , value in index_to_book.items()}
# 	words_compressed = pickle.load(open("words.pkl", "rb"))
# 	docs_compressed = pickle.load(open("docs.pkl", "rb"))


# 	title_input = request.args.get('title_search')
# 	keyword_input = request.args.get('keyword_search')

	
# 	#ALWAYS NEED THESE
# 	#word_cloud_message =
# 	#top_books_message = 
# 	#word_cloud =
# 	#top_books = 

# 	#initial
# 	if title_input == None and keyword_input == None:
# 		word_cloud_message = ''
# 		top_books_message =  ''
# 		word_cloud = []
# 		top_books = []


# 	elif keyword_input is not None: 
# 		word_cloud_message = ''
# 		top_books_message = "Top 15 books for the keyword are:"
# 		word_cloud = []
# 		lst = keyword_input.split(" ")

# 		top_books = closest_books_to_many_words(lst, word_to_index, index_to_book,words_compressed, docs_compressed)

# 	else:
# 		word_cloud_message = 'Word cloud is: '
# 		top_books_message = ""
# 		word_cloud = create_books_to_wordcloud(title_input, index_to_word, book_to_index, words_compressed , docs_compressed)
# 		top_books = []

# 	return render_template('search.html', name=project_name, netid=net_id, word_cloud_message=word_cloud_message, top_books_message=top_books_message, word_cloud=word_cloud, top_books = top_books)

  
	#############inserting into the database#####################################################
	# db.create_all()
	# print(os.getcwd())
	# with open('book_to_index.json') as book_to_index_dict:
	# 	d = json.load(book_to_index_dict)
	# 	for book in d.keys():
	# 		b = Book(name = book, index = d[book])
	# 		db.session.add(b)
	# 	db.session.commit()

	# with open('description_cosine_small.csv') as cosine_similarity_matrix_csv:
	# 	matrix_reader = csv.reader(cosine_similarity_matrix_csv, delimiter = ' ', quotechar='|')
	# 	r = 0
	# 	for row in matrix_reader:
	# 		c = 0
	# 		for col in row:
	# 			tfidf = TFIDF(RowNo = r, ColNo = c, CellValue = col)
	# 			c += 1
	# 			db.session.add(tfidf)
	# 		r += 1
	# db.session.commit()
	#############################################################################################



	##How to empty the database###### 
	##db.reflect()
	##db.drop_all()
	

