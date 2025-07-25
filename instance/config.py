import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-secreta-desarrollo'
    
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('SUPABASE_DB_URI') or \
        'postgresql://postgres:7224398197.@db.egrhwmrtjufguzfryokz.supabase.co:5432/postgres'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
