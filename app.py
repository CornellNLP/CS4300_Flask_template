from app import app, socketio
from flask import *
import string
from rankings import get_top, restaurant_to_index
import logging # from ta

app = Flask(__name__, template_folder='app/templates')

gunicorn_logger = logging.getLogger('gunicorn.error') # from ta
app.logger.handlers = gunicorn_logger.handlers # from ta
app.logger.setLevel(gunicorn_logger.level) # from ta

# get user input
@app.route("/")
def query():
  data = []
  output_message = ''

  restaurant_query = request.args.get('fav_name')
  price_query = request.args.get('max_price')
  cuisine_query = request.args.get('cuisine')
  ambiance_query = request.args.get('ambiance')
  if cuisine_query == None:
    cuisine_query = ""
  if ambiance_query == None:
    ambiance_query = ""
  # if there is an input
  if restaurant_query:
    restaurant_query = string.capwords(restaurant_query)
    # if restaurant_query is in the data
    if restaurant_query in restaurant_to_index.keys():
      top_restaurants = get_top(restaurant_query, price_query, cuisine_query, ambiance_query, 3)
      output_message = "Your search: " + restaurant_query
      data = top_restaurants
    # restaurant_query is not in the data
    else:
      output_message = "Your search " + restaurant_query + " is not in the dataset. Please try another restaurant"
    app.logger.critical("output_message") # from ta
    app.logger.critical(output_message) # from ta
    app.logger.critical("data") # from ta
    app.logger.critical(data) # from ta
  return render_template('search.html', output_message=output_message, data=data)

if __name__ == "__main__":
  print("Flask app running at http://0.0.0.0:5000")
  socketio.run(app, host="0.0.0.0", port=5000)
