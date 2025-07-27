from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS

db = SQLAlchemy()
login_manager = LoginManager()  #Aquí se crea el login manager

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object('instance.config.Config')

    db.init_app(app)

    login_manager.init_app(app)  #Inicializar el login manager
    login_manager.login_view = 'main.login_view'  #Vista de login si no está autenticado

    from .models import Usuario  #Importa el modelo aquí para el user_loader

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(user_id)  #Recupera el usuario por su ID

    from .routes import main
    app.register_blueprint(main)

    return app
