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

@irsystem.route('/debug', methods=['GET'])
def debug():
	b = Words.query.filter_by(name = u'wrong').first()
	print(b.name)
	print(b.index)
	print(b.book_scores)
	#print(b.word_cloud)
	return render_template('secondpage.html', name=project_name, netid=net_id, word_cloud_message='',
		top_books_message='', word_cloud=[], top_books = [], avail_keywords = [], avail_books = [])


@irsystem.route('/secondpage', methods=['GET'])
def secondpage():
	print("enter second page ")
	title_input = session.get('title_input', None)
	keyword_input = session.get('keyword_input', None)
	top_book_message = ""
	if title_input is not None :
		title_input = unicodedata.normalize('NFKD', title_input).encode('ascii', 'ignore')
		title_input_list = title_input.split("**") 
		print("title_input_list")
		print(title_input_list)
		for title in title_input_list : 
			if title == "": 
				top_book_message += title 
			else : 
				top_book_message += title 
				top_book_message += ", "
	if keyword_input is not None:
		keyword_input = unicodedata.normalize('NFKD', keyword_input).encode('ascii', 'ignore')
		keyword_input_list = keyword_input.split("**")
		for key in keyword_input_list : 
			if key =="" : 
				top_book_message += key 
			else : 
				top_book_message += key 
				top_book_message += ", "
	top_book_message = top_book_message[:-2]
	top15_asorted = session.get('top15_asorted', None)
	top_15_book_info = get_books(top15_asorted)
	print(top_15_book_info[0])

	#encode everything to make sure that the output is the correct ouput format

	arr=["<i>", "</i>", "<i/>","<br />","</b>", "<b>", "<strong>", "<a href=https://", "</blockquote>"
	"<em>" , "</em>", "<emAVA>" , "<sub>",  "</sub>", "<sup>",  "</sup>", "<hr>", "</hr>",  "<p>", "</p>", 
     "</strong>", "<em>", "</em>", "<p>","</p>","<div>", "<u>", "</u>", "<a>", "</a>", "</div>"] 

	for result in top_15_book_info:
		for i in range(6):
			if result[i] is None:
				result[i] = ''
			else:
				result[i] = unicodedata.normalize('NFKD', result[i]).encode('ascii','ignore')
		for idx in range(len(result[6])) :
			result[6][idx] = unicodedata.normalize('NFKD', result[6][idx]).encode('ascii','ignore')
		if result[3] != "" :
			result[3] = "http://www.goodreads.com/book/show/" + result[3]
		else :
			result[3] =""
		result[2] = "http://covers.openlibrary.org/b/isbn/" + result[2] + "-M.jpg"
		result[1] = "http://covers.openlibrary.org/b/isbn/" + result[1] + "-M.jpg"
		for i in range(0, len(arr)-1):
			result[5] = result[5].replace(arr[i],"")


	return render_template('secondpage.html', name=project_name, netid=net_id, word_cloud_message='',
		top_books_message=top_book_message, word_cloud=[], top_books = top_15_book_info, avail_keywords = [], avail_books = [])


@irsystem.route('/main', methods=['GET'])
def search():
	available_words = json.load(open('words.json'))
	available_books = json.load(open('books.json'))

	title_input = request.args.get('title_search')
	keyword_input = request.args.get('keyword_search')

	print("first page")
	print(title_input)
	print(keyword_input)

	if title_input is not None or keyword_input is not None :
		print("enter if statement inside the first page")
	
		if title_input !="" or keyword_input!="":
			w = word_to_closest_books(keyword_input)
			b = book_to_closest_books(title_input)
			if w is None or b is None : 
				print("This input and output is invalid try another")
				error_message = "The Input is Invalid Please Use the Autocomplete Functionality"
				return render_template('search.html', name=project_name, netid=net_id, word_cloud_message='', top_books_message='',
						word_cloud=[], top_books = [], error_message = error_message,  avail_keywords = available_words, avail_books = available_books)
			top15_asorted = combine_two_scores(w, b)
			session["top15_asorted"] = top15_asorted
			session["title_input"]  = title_input
			session["keyword_input"] = keyword_input
			return redirect(url_for('irsystem.secondpage'))

		else:
			
			return render_template('search.html', name=project_name, netid=net_id, word_cloud_message='', top_books_message='',\
			word_cloud=[], top_books = [], error_message = "", avail_keywords = available_words, avail_books = available_books)

	return render_template('search.html', name=project_name, netid=net_id, word_cloud_message='', top_books_message='',
		word_cloud=[], top_books = [], error_message = "",  avail_keywords = available_words, avail_books = available_books)


