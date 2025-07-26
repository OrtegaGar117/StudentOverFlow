from flask import Blueprint, request, jsonify, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Usuario  # Asegúrate que el modelo esté en models.py
from . import db

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@main.route('/login', methods=['GET'])
def login_view():
    return render_template('login.html')

@main.route('/register', methods=['GET'])
def register_view():
    return render_template('register.html')

@main.route('/foro', methods=['GET'])
def foro_view():
    return render_template('foro.html')

@main.route('/register', methods=['POST'])
def register():
    if request.is_json:
        data = request.get_json()
        nombre = data.get('nombre')
        email = data.get('email')
        contrasena = data.get('contraseña')
    else:
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        contrasena = request.form.get('contraseña')

    if not nombre or not email or not contrasena:
        return "Faltan datos", 400

    hashed_password = generate_password_hash(contrasena)

    nuevo_usuario = Usuario(
        nombre=nombre,
        email=email,
        contraseña=hashed_password
    )

    db.session.add(nuevo_usuario)
    db.session.commit()

    # Si viene de formulario, redirige a login, si es JSON responde JSON
    if request.is_json:
        return jsonify({"mensaje": "Usuario registrado con éxito"}), 201
    else:
        return render_template('login.html', mensaje="Usuario registrado con éxito")

@main.route('/login', methods=['POST'])
def login():
    data = request.json
    usuario = Usuario.query.filter_by(email=data['email']).first()

    if usuario and check_password_hash(usuario.contraseña, data['contraseña']):
        return jsonify({"mensaje": "Login exitoso", "usuario_id": usuario.id}), 200
    else:
        return jsonify({"mensaje": "Credenciales inválidas"}), 401