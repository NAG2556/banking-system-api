import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "super-secret-key-1234")
    SQLALCHEMY_DATABASE_URI = "sqlite:///banking.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jwt-super-secret-key-1234")
