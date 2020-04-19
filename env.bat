:: Set the environment type of the app (see config.py)
SET APP_SETTINGS=config.DevelopmentConfig
:: Set the DB url to a local database for development
REM SET DATABASE_URL=postgresql://localhost/hahadata
SET DATABASE_URL=postgresql://winice:password@localhost:5432/hahadata
