from app import app, socketio
import pickle
import os
import flask
from collections import defaultdict

def load_index():
  print("Loading Inverted Index")
  app.config['index'] = defaultdict(dict)
  for filename in os.listdir(os.getcwd() + "/app/utils/data"):
    # print(filename)
   		#print filename
    f = open(os.getcwd() + "/app/utils/data/" + filename,"rb")
    # print(f)
    d = pickle.load(f)
    # print(d)
    word_id = filename.split('.')[0]
    # print(word_id)
    app.config['index'][word_id] = d

  

if __name__ == "__main__":
  load_index()  
  print "Flask app running at http://0.0.0.0:5000"
  socketio.run(app, host="0.0.0.0", port=5000, debug=True)
