from app import app, socketio

from flask import *

app = Flask(__name__)

# get user input
@app.route("/")
def query():
  restaurant = request.args.get('fav_name')
  if restaurant:
    return request.args.get('fav_name')
  else:
    # return app.send_static_file('/app/static/search.html')
    return ""


if __name__ == "__main__":
  print("Flask app running at http://0.0.0.0:5000")
  socketio.run(app, host="0.0.0.0", port=5000)
