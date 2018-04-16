<<<<<<< HEAD
from app import app, socketio
import pickle
import os
import flask
from collections import defaultdict

# def load_index():
#   print("Loading Inverted Index")
#   app.config['index'] = defaultdict(dict)
#   for filename in os.listdir(os.getcwd() + "/app/utils/data"):
#     # print(filename)
#    		#print filename
#     f = open(os.getcwd() + "/app/utils/data/" + filename,"rb")
#     # print(f)
#     d = pickle.load(f)
#     # print(d)
#     word_id = filename.split('.')[0]
#     # print(word_id)
#     app.config['index'][word_id] = d

# def load_idfs():

=======
from app import app
>>>>>>> frontend2

if __name__ == "__main__":
  # load_index()  
  valid_words_file = open(os.getcwd() + "/app/utils/words.pkl","rb")
  app.config['valid_words'] = pickle.load(valid_words_file)

  idf_file = open(os.getcwd() + "/app/utils/idf.pkl", "rb")
  app.config['idfs'] = pickle.load(idf_file)

  doc_norms_file = open(os.getcwd() + "/app/utils/doc_norms.pkl", "rb")
  app.config['doc_norms'] = pickle.load(doc_norms_file)

  print "Flask app running at http://0.0.0.0:5000"
<<<<<<< HEAD
  socketio.run(app, host="0.0.0.0", port=5000, debug=True)
=======
  app.run(host="0.0.0.0", port=5000, debug=True)
>>>>>>> frontend2
