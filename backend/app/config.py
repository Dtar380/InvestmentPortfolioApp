from os import getenv

def _get_bool_env(var_name: str, default: bool) -> bool:
    val = getenv(var_name)
    if val is None:
        return default
    return val.lower() in ("true", "1", "yes")

NAME = "Investment Portfolio API"
VERSION = "0.1.0"

ENV = getenv("ENV", "development")
DEBUG = _get_bool_env("DEBUG", ENV == "development")

SECRET_KEY = getenv("SECRET_KEY", "supersecretkey")
HOST = getenv("BACKEND_HOST", "0.0.0.0")
PORT = int(getenv("BACKEND_PORT", "8000"))
ALLOWED_HOSTS = getenv("ALLOWED_HOSTS", "localhost").split(",")

CORS_ORIGINS = getenv("CORS_ORIGINS", "http://localhost").split(",")

DATABASE_URL = getenv("DATABASE_URL", "postgresql:///./test.db")
