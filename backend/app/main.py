from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import (
    NAME,
    VERSION,
    DEBUG,
    CORS_ORIGINS
)

app = FastAPI(
    title=NAME,
    version=VERSION,
    debug=DEBUG,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def main():
    return {"message": "Welcome to the Investment Portfolio API!"}


if __name__ == "__main__":
    main()
