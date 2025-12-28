from os import getenv

NAME = "Investment Portfolio API"
VERSION = "0.1.0"

ENV = getenv("ENV", "development")
DEBUG = getenv("DEBUG", ENV == "development")

SECRET_KEY = getenv("SECRET_KEY", "supersecretkey")
ALLOWED_HOSTS = getenv("ALLOWED_HOSTS", "localhost").split(",")

CORS_ORIGINS = getenv("CORS_ORIGINS", "http://localhost").split(",")

DATABASE_URL = getenv("DATABASE_URL", "postgresql:///./test.db")
