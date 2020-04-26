import logging
from app import app, socketio

if __name__ == "__main__":
  print("Flask app running at http://0.0.0.0:5000")
  socketio.run(app, host="0.0.0.0", port=5000)
if(__name__!="__main__"):
     gunicorn_logger = logging.getLogger('gunicorn.error')
     app.logger.handlers = gunicorn_logger.handlers
     app.logger.setLevel(gunicorn_logger.level)
