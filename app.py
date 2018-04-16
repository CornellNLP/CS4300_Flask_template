from app import app, socketio
import pickle
import os
import flask
from collections import defaultdict

if __name__ == "__main__":
  # load_index()  
  valid_words_file = open(os.getcwd() + "/app/utils/words.pkl","rb")
  app.config['valid_words'] = pickle.load(valid_words_file)

  idf_file = open(os.getcwd() + "/app/utils/idf.pkl", "rb")
  app.config['idfs'] = pickle.load(idf_file)

  doc_norms_file = open(os.getcwd() + "/app/utils/doc_norms.pkl", "rb")
  app.config['doc_norms'] = pickle.load(doc_norms_file)

  print "Flask app running at http://0.0.0.0:5000"
  socketio.run(app, host="0.0.0.0", port=5000, debug=True)
