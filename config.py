import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres.mnjkqaykkrlatiokegux:1Adminpassword!2@aws-0-eu-west-3.pooler.supabase.com:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "devkey"
