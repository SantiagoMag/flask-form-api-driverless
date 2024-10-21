import os

class Config:
    SECRET_KEY = 'mi_clave_secreta'
    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True