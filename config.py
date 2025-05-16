import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost:5432/jo_billeterie'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "devkey"
