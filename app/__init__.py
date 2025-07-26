from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS 

db = SQLAlchemy()

def create_app():

    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object('instance.config.Config')

    db.init_app(app)

    from .routes import main 
    app.register_blueprint(main)

    return app