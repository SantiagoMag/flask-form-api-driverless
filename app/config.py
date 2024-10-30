import os

class Config:
    SECRET_KEY = 'mi_clave_secreta'
    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://UserML:ML.2024#@10.10.101.210/BD_DemoH2O?driver=ODBC+Driver+17+for+SQL+Server'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    SQLALCHEMY_ECHO = True
class DevelopmentConfig(Config):
    DEBUG = True