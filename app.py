# from app import app, socketio
# import socketio
from flask import *
import string
from rankings import get_top, restaurant_to_index
import logging # from ta
from rankings import filterRestaurants, getCosineRestaurants
app = Flask(__name__, template_folder='app/templates')

gunicorn_logger = logging.getLogger('gunicorn.error') # from ta
app.logger.handlers = gunicorn_logger.handlers # from ta
app.logger.setLevel(gunicorn_logger.level) # from ta

app.logger.critical("line 14")

# get user input
@app.route("/", methods=["GET"])
def query():
  data = []
  output_message = ''

  app.logger.critical("app")
  restaurant_query = request.args.get('fav_name')
  app.logger.critical(restaurant_query)
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
      top_restaurants = get_top(restaurant_query, price_query, cuisine_query, ambiance_query, 3, False, None)
      output_message = "Your search: " + restaurant_query
      data = top_restaurants
    # restaurant_query is not in the data
    else:
      output_message = "Your search " + restaurant_query + " is not in the dataset. Please enter its information"
      review_query = request.args.get('user_review')
      #filter the restaurants that are relevant to the user's search
      rel_restaurants = filterRestaurants(price_query, cuisine_query)
      cosine_sim_restaurants = getCosineRestaurants(review_query, rel_restaurants)
      top_restaurants = get_top("", price_query, cusine_query, ambiance_query, 3, True, cosine_sim_restaurants)
      #output_message = "Your search " + restaurant_query + " is not in the dataset. Please try another restaurant"
    app.logger.critical("output_message") # from ta
    app.logger.critical(output_message) # from ta
    app.logger.critical("data") # from ta
    app.logger.critical(data) # from ta
  return render_template('search.html', output_message=output_message, data=data)

if __name__ == "__main__":
  print("Flask app running at http://0.0.0.0:5000")
  socketio.run(app, host="0.0.0.0", port=5000)
