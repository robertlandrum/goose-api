# settings.py

from starlette.config import Config

config = Config(".env")

MONGO_URL = config('MONGO_URL', default="mongo://localhost")
