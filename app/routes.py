from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Usuario  # Asegúrate que el modelo esté en models.py
from . import db

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def home():
    return jsonify({"mensaje": "API funcionando"}), 200

@main.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed_password = generate_password_hash(data['contraseña'])

    nuevo_usuario = Usuario(
        nombre=data['nombre'],
        email=data['email'],
        contraseña=hashed_password
    )

    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({"mensaje": "Usuario registrado con éxito"}), 201

@main.route('/login', methods=['POST'])
def login():
    data = request.json
    usuario = Usuario.query.filter_by(email=data['email']).first()

    if usuario and check_password_hash(usuario.contraseña, data['contraseña']):
        return jsonify({"mensaje": "Login exitoso", "usuario_id": usuario.id}), 200
    else:
        return jsonify({"mensaje": "Credenciales inválidas"}), 401