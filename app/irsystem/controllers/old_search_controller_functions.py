##old functions 

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


def put_books_and_words_in_db(hash_factor = 100):
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