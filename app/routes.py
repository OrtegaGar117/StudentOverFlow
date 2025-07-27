from flask import Blueprint, request, jsonify, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Usuario, Pregunta
from . import db
from flask_login import login_required, current_user, login_user
from .forms import PreguntaForm

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


    if request.is_json:
        return jsonify({"mensaje": "Usuario registrado con éxito"}), 201
    else:
        return render_template('login.html', mensaje="Usuario registrado con éxito")

@main.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    contrasena = request.form.get('contraseña')

    if not email or not contrasena:
        return render_template('login.html', mensaje="Faltan datos")

    usuario = Usuario.query.filter_by(email=email).first()

    if usuario and check_password_hash(usuario.contraseña, contrasena):
        login_user(usuario)
        return render_template('foro.html', mensaje="Login exitoso")
    else:
        return render_template('login.html', mensaje="Credenciales inválidas")

@main.route('/crear-pregunta', methods=['GET', 'POST'])
@login_required
def crear_pregunta():
    form = PreguntaForm()
    if form.validate_on_submit():
        nueva_pregunta = Pregunta(
            titulo=form.titulo.data,
            materia=form.materia.data,
            contenido=form.contenido.data,
            id_usuario=current_user.id
        )
        db.session.add(nueva_pregunta)
        db.session.commit()
        flash('Pregunta creada con éxito', 'success')
        return redirect(url_for('main.foro_view'))
    return render_template('crear_pregunta.html', form=form)