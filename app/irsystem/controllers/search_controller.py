from . import *  
import numpy as np 
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


@irsystem.route('/', methods=['GET'])
def search():
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

	book_list = [book.name for book in Book.query.all()]
	print(len(book_list))

	title_input = request.args.get('title_search')
	keyword_input = request.args.get('keyword_search')

	#user has not inputted anything yet. 
	if title_input not in book_list:	 
		output_message = 'the book not in the database'

	#we got user input. Now, we can find similar books.
	else : 
		print("user input is %s" % (title_input)) 

		usr_bk = Book.query.filter_by(name = title_input).first()
		usr_bk_idx = usr_bk.index
		usr_bk_name = usr_bk.name

		# all_bks = TFIDF.query.filter_by(RowNo = usr_bk_idx).all()

		# cos_sim_list = []
		# for bk in all_bks:
		# 	cos_sim_list.append(bk.CellValue)

		# nparray = np.asarray(cos_sim_list)
		# sortedarray = np.argsort(nparray)[::-1]
		# topten = sortedarray[:10]  

		# topten_bk = []
		# for i in topten : 
		# 	ith_sim_bk = Book.query.filter_by(index = i).first()
		# 	topten_bk.append((ith_sim_bk.name, cos_sim_list[i]))

		topten_bk = [1,2,3,4,5]

	if title_input not in book_list:
		data = [1,2,3]
		output_message = 'the book not in the database'
	else:
		output_message = "Top ten similar books to : " + title_input
		data = topten_bk
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)

@irsystem.route('/delete', methods=['GET'])
def search():
	db.reflect()
	db.drop_all()
	output_message = 'emptied out the database!'
	data = ['really?', 'did you really though?']
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)

@irsystem.route('/add', methods=['GET'])
def search():
	db.reflect()
	db.drop_all()
	output_message = 'emptied out the database!'
	data = ['really?', 'did you really though?']
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)



###todo1. change tfidf model to cosine sim model.



	##How to empty the database###### 
	##db.reflect()
	##db.drop_all()
	

