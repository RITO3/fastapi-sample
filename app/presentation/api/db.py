from databases import Database

from app.config.settings import Settings

settings = Settings()
if settings.DB_CONNECTION_STRING is not None:
    database = Database(settings.DB_CONNECTION_STRING)
else:
    raise Exception()
