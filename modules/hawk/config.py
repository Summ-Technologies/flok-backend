import os

# CORS through summ-web
CORS_ALLOW_ORIGINS = os.environ.get("CORS_ALLOW_ORIGINS", "").split(",")

# SQLALCHEMY
SQLALCHEMY_DATABASE_URI = os.environ.get(
    "DATABASE_URL", os.environ.get("SQLALCHEMY_DATABASE_URI")
)

# base url of public client
CLIENT_BASE_URL = os.environ["CLIENT_BASE_URL"]

# RMQ connection config
RMQ_USER = os.environ["RMQ_USER"]
RMQ_PASSWORD = os.environ["RMQ_PASSWORD"]
RMQ_HOST = os.environ["RMQ_HOST"]
RMQ_PORT = os.environ["RMQ_PORT"]

# JWT Auth
SECRET_KEY = os.environ.get("SECRET_KEY")
JWT_LIFESPAN = os.environ.get("JWT_LIFESPAN", -1)
JWT_FRESHSPAN = os.environ.get("JWT_FRESHSPAN", 5)

# Logging
tmp = os.environ.get("SUMM_LOG_FILE")
if tmp:
    SUMM_LOG_FILE = tmp

tmp = os.environ.get("SUMM_LOG_FILE_SIZE")
if tmp:
    SUMM_LOG_FILE_SIZE = tmp
