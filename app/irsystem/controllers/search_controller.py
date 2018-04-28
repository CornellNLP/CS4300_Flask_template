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
	print("enter second page ")
	results = session.get('result', None)
	title_input = session.get('title_input', None) 
	keyword_input = session.get('keyword_input', None)
	top_book_message = ""
	if title_input is not None : 
		title_input = title_input.encode('ascii', 'gignore')
		top_book_message += title_input 
	if keyword_input is not None: 
		keyword_input = keyword_input.encode('ascii', 'ignore')
		top_book_message += keyword_input
	
	#encode everything to make sure that the output is the correct ouput format 

	for result in results :
		link=result[3].encode('ascii','ignore')
		link ="http://www.goodreads.com/book/show/" + link
		result[1] = result[1].encode('ascii','ignore') 
		result[2] = result[2].encode('ascii','ignore') 
		url = "http://covers.openlibrary.org/b/isbn/" + result[1]  + '-M.jpg'
		url2 = "http://covers.openlibrary.org/b/isbn/" + result[2]  + '-M.jpg'
		url=url.encode('ascii','ignore') 
		url2=url2.encode('ascii','ignore') 
		result[1] = result[1].encode('ascii', 'ignore')
		result[1] = url  
		result[2] = url2 
		result[3] = link 

	return render_template('secondpage.html', name=project_name, netid=net_id, word_cloud_message='', 
		top_books_message=top_book_message, word_cloud=[], top_books = results, avail_keywords = [], avail_books = [])
 
	
@irsystem.route('/main', methods=['GET'])
def search():
	available_words = json.load(open('words.json'))
	available_words = [unicodedata.normalize('NFKD', w).encode('ascii','ignore') for w in available_words]
	available_books = json.load(open('books.json'))
	available_books = [unicodedata.normalize('NFKD', b).encode('ascii','ignore') for b in available_books]

	#author_input = request.args.get('author_search')
	title_input = request.args.get('title_search')
	keyword_input = request.args.get('keyword_search')
	title_input = request.args.get('title_search')
	keyword_input = request.args.get('keyword_search') 
	print("first page")

	if title_input is not None or keyword_input is not None :
		w = word_to_closest_books(keyword_input)
		b = book_to_closest_books(title_input)
		result = combine_result(w, b) 
		session["result"] = result 
		session["title_input"]  = title_input 
		session["keyword_input"] = keyword_input
		return redirect(url_for('irsystem.secondpage'))
	return render_template('search.html', name=project_name, netid=net_id, word_cloud_message='', top_books_message='', 
		word_cloud=[], top_books = [], avail_keywords = available_words, avail_books = available_books)

