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
import psycopg2

project_name = "BookRec"
net_id = "Hyun Kyo Jung: hj283"


@irsystem.route('/db', methods=['GET'])
def change_db_final():
	print('start')
	# put_books_in_db(11)
	# put_words_in_db(11)
	# db.session.commit()
	# change_b2w_value(3)
	# change_w2b_value(3)
	print('all done')
	return render_template('secondpage.html', name=project_name, netid=net_id, word_cloud_message='',
		top_books_message='', word_cloud=[], top_books = [], avail_keywords = [], avail_books = [])


@irsystem.route('/debug', methods=['GET'])
def debug():

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
		top_book_message += title_input
		top_book_message += " ,"
	if keyword_input is not None:
		keyword_input = unicodedata.normalize('NFKD', keyword_input).encode('ascii', 'ignore')
		top_book_message += keyword_input

	top15_asorted = session.get('top15_asorted', None)
	top_15_book_info = get_books(top15_asorted)


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
	available_authors = json.load(open('authors.json'))
	authors_to_books = json.load(open('authors_to_books.json'))

	author_input = request.args.get('author_search')
	title_input = request.args.get('title_search')
	keyword_input = request.args.get('keyword_search')

	print("first page")
	print("title input type is : {}".format(type(title_input)))
	print("keyword input type is : {}".format(type(keyword_input)))

	if title_input is not None or keyword_input is not None or author_input is not None:
		print("enter if statement inside the first page")
		if author_input != "":
			for author in author_input.split('**'):
				for book in authors_to_books[author]:
					new_format = book[:book.rfind(' (published by) ')]
					title_input += '**' + new_format
			
		if title_input !="" or keyword_input!="":
			sim_scores = inputs_to_scores(keyword_input, title_input)
			if sim_scores is None:
				return render_template('search.html', name=project_name, netid=net_id, word_cloud_message='', top_books_message='',\
						word_cloud=[], top_books = [], avail_keywords = available_words, avail_books = available_books, avail_authors = available_authors)
			top15_asorted = scores_to_asort(sim_scores)

			session["top15_asorted"] = top15_asorted
			session["title_input"]  = title_input
			session["keyword_input"] = keyword_input
			return redirect(url_for('irsystem.secondpage'))

	return render_template('search.html', name=project_name, netid=net_id, word_cloud_message='', top_books_message='',
		word_cloud=[], top_books = [], avail_keywords = available_words, avail_books = available_books, avail_authors = available_authors)


