import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Different environments for the app to run in

class Config(object):
  DEBUG = False
  CSRF_ENABLED = True
  CSRF_SESSION_KEY = "secret"
  SECRET_KEY = "not_this"

  MONGO_URI = 'mongodb://heroku_64g4q22c:fd0pjea0drkj8qd7k4k94slbne@ds337418.mlab.com:37418/heroku_64g4q22c?retryWrites=false'
  MONGO_DBNAME = 'heroku_64g4q22c'
  MONGO_DBCOLLECTION = 'debates'

class ProductionConfig(Config):
  DEBUG = False

class StagingConfig(Config):
  DEVELOPMENT = True
  DEBUG = True

class DevelopmentConfig(Config):
  DEVELOPMENT = True
  DEBUG = True

class TestingConfig(Config):
  TESTING = True
