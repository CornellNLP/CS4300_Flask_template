from . import *  
import numpy as np 
import pickle 
import numpy as np 
import json
#import Collections 
from sklearn.preprocessing import normalize
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
####
from app.irsystem.models.tfidf import *
from app.irsystem.models.book import *
import json
import os
import csv

project_name = "BookRec"
net_id = "Hyun Kyo Jung: hj283"


def closest_books_to_word(word_in, word_to_index, index_to_book, words_compressed, docs_compressed, k = 15):
    if word_in not in word_to_index: return "Not in vocab." 
    sims = docs_compressed.dot(words_compressed[int(word_to_index[word_in]),:])
    asort = np.argsort(-sims)[:k+1]
    return [(index_to_book[str(i)],sims[i]/sims[asort[0]]) for i in asort[1:]]

def create_books_to_wordcloud(title_in, index_to_word, book_to_index, words_compressed , docs_compressed, k = 5):
    if title_in not in book_to_index: return "Not in vocab."
    
    sims = words_compressed.dot(docs_compressed[int(book_to_index[title_in]),:])
    asort = np.argsort(-sims)[:k+1]
    print(asort)
    return [(index_to_word[i],sims[i]/sims[asort[0]])for i in asort[1:]]


@irsystem.route('/', methods=['GET'])
def search():
	###open the files
	try:
		words_compressed = pickle.load(open("words_compressed_no_stemming.pkl", "rb"))
		docs_compressed = pickle.load(open("docs_compressed_no_stemming.pkl", "rb"))

	except:
		print("failed to do pkl")
		return render_template('search.html', name=project_name, netid=net_id, word_cloud_message='cloud pkl', top_books_message='opening pkl files crashed', word_cloud=[], top_books = [])
	try:
		index_to_word = json.load(open("index_to_word.json"))
		index_to_book = json.load(open("index_to_book.json"))
	except:
		print("failed to do json")
		return render_template('search.html', name=project_name, netid=net_id, word_cloud_message='cloud json', top_books_message='opening json files crashed', word_cloud=[], top_books = [])

	word_to_index = {value : key for key , value in index_to_word.items()}
	book_to_index = {value : key for key , value in index_to_book.items()}

	title_input = request.args.get('title_search')
	keyword_input = request.args.get('keyword_search')

	#ALWAYS NEED THESE
	#word_cloud_message =
	#top_books_message = 
	#word_cloud =
	#top_books = 

	#initial
	if title_input == None and keyword_input == None:
		word_cloud_message = ''
		top_books_message =  ''
		word_cloud = []
		top_books = []

	#user clicked on keyword button. 
	elif keyword_input is not None:
		word_cloud_message = ''
		top_books_message = "Top ten books for the keyword are:"
		word_cloud = []
		top_books = closest_books_to_word(keyword_input, word_to_index, index_to_book,words_compressed, docs_compressed)

	#user cliked on title button.
	else:
		word_cloud_message = 'Word cloud is: '
		top_books_message = ""
		word_cloud = create_books_to_wordcloud(title_in, index_to_word, book_to_index, words_compressed , docs_compressed)
		top_books = []

	return render_template('search.html', name=project_name, netid=net_id, word_cloud_message=word_cloud_message, top_books_message=top_books_message, word_cloud=word_cloud, top_books = top_books)






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
	

