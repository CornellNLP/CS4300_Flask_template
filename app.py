from app import app

if __name__ == "__main__":
  print "Flask app running at http://0.0.0.0:5000"
  app.run(host="0.0.0.0", port=5000, debug=True)
