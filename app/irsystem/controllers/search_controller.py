from . import *  
import numpy as np 
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
####
from app.irsystem.models.cossim import *
from app.irsystem.models.book import *
import json
import os
import csv

project_name = "BookRec"
net_id = "Hyun Kyo Jung: hj283"

@irsystem.route('/', methods=['POST'])
def post():
	db.create_all()
	print(os.getcwd())
	with open('book_to_index.json') as book_to_index_dict:
		d = json.load(book_to_index_dict)
		for book in d.keys():
			b = Book(name = book, index = d[book])
			db.session.add(b)
		db.session.commit()

	with open('description_cosine_6140.json') as cosine_similarity_matrix:
		d = json.load(cosine_similarity_matrix)
		i = 0
		for k in d.keys():
			c = 0
			for col in d[k]:
				cossim = COSSIM(RowNo = k, ColNo = c, CellValue = col)
				db.session.add(cossim)
				c += 1
			i += 1
			print('at %s th book' % i)
		db.session.commit()

	output_message = ''
	data = []
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)

@irsystem.route('/', methods=['GET'])
def search():
	# db.create_all()
	# print(os.getcwd())
	# with open('book_to_index.json') as book_to_index_dict:
	# 	d = json.load(book_to_index_dict)
	# 	for book in d.keys():
	# 		b = Book(name = book, index = d[book])
	# 		db.session.add(b)
	# 	db.session.commit()

	# with open('description_cosine_6140.json') as cosine_similarity_matrix:
	# 	d = json.load(cosine_similarity_matrix)
	# 	i = 0
	# 	for k in d.keys():
	# 		c = 0
	# 		for col in d[k]:
	# 			cs = COSSIM(RowNo = k, ColNo = c, CellValue = col)
	# 			db.session.add(cs)
	# 			c += 1
	# 		i += 1
	# 		print('at %s th book' % i)
	# 	db.session.commit()

	title_input = request.args.get('title_search')
	keyword_input = request.args.get('keyword_search')

	book_list = [b.name for b in Book.query.all()]
	print(len(book_list))
	#user has not inputted anything yet. 
	if title_input not in book_list:	 
		print("No match!")
		print(book_list[0])
		print(len(COSSIM.query.all()))
		
	#we got user input. Now, we can find similar books.
	else : 
		print("user input is %s" % (title_input)) 

		usr_bk = Book.query.filter_by(name = title_input).first()
		usr_bk_idx = usr_bk.index
		usr_bk_name = usr_bk.name

		all_bks = COSSIM.query.filter_by(RowNo = usr_bk_idx).all()

		cos_sim_list = []
		for bk in all_bks:
			cos_sim_list.append(bk.CellValue)

		nparray = np.asarray(cos_sim_list)
		sortedarray = np.argsort(nparray)[::-1]
		topten = sortedarray[:10]  

		topten_bk = []
		for i in topten : 
			ith_sim_bk = Book.query.filter_by(index = i).first()
			topten_bk.append((ith_sim_bk.name, cos_sim_list[i]))

	if title_input not in book_list:
		data = []
		output_message = 'No match! Sorry.'
	else:
		output_message = "Top ten similar books to : " + title_input
		data = topten_bk
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)


###todo1. change tfidf model to cosine sim model.



	#How to empty the database###### 
	#db.reflect()
	#db.drop_all()
	