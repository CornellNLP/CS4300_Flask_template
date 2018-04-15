from app import app, socketio
import pickle
import os
import flask
from collections import defaultdict



if __name__ == "__main__":
  global tf_idfs
  print("Loading TF-IDFS")
  app.config['tf_idfs'] = defaultdict(dict)
  for filename in os.listdir(os.getcwd() + "/app/utils/data"):
    # print(filename)
   		#print filename
    f = open(os.getcwd() + "/app/utils/data/" + filename,"rb")
    # print(f)
    d = pickle.load(f)
    # print(d)
    word_id = filename.split('.')[0]
    # print(word_id)
    app.config['tf_idfs'][word_id] = d
  
  print "Flask app running at http://0.0.0.0:5000"
  socketio.run(app, host="0.0.0.0", port=5000, debug=True)
