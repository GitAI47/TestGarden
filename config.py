import os

class Config:
    # Voor sessions, flash messages, etc.
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key"

    # Later kun je dit gebruiken voor echte database
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
