from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS 

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:7224398197.@db.egrhwmrtjufguzfryokz.supabase.co:5432/postgres'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .routes import main 
    app.register_blueprint(main)

    return app