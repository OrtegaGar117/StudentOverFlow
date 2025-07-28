from flask import Blueprint, request, jsonify, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Usuario, Pregunta
from . import db # Objeto de base de datos (SQLAlchemy)
from flask_login import login_required, current_user, login_user
from .forms import PreguntaForm

#Definimos un blueprint para las rutas principales
main = Blueprint('main', __name__)

#Página de inicio
@main.route('/', methods=['GET'])
def home():
    return render_template('index.html')

#Vista de login
@main.route('/login', methods=['GET'])
def login_view():
    return render_template('login.html')

#Vista de registro
@main.route('/register', methods=['GET'])
def register_view():
    return render_template('register.html')

#Vista del foro
@main.route('/foro', methods=['GET'])
def foro_view():
    return render_template('foro.html')

#Registro para nuevos usuarios
@main.route('/register', methods=['POST'])
def register():
    #Permite registrar nuevos usuarios, tanto desde un formulario HTML como desde una solicitud JSON.
    if request.is_json:
        data = request.get_json()
        nombre = data.get('nombre')
        email = data.get('email')
        contrasena = data.get('contraseña')
    else:
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        contrasena = request.form.get('contraseña')

    #Verificamos que los datos estén presentes
    if not nombre or not email or not contrasena:
        return "Faltan datos", 400
    
    #Verificamos si el usuario ya existe
    hashed_password = generate_password_hash(contrasena)
    
    #Se crea un nuevo usuario y se guarda en la base de datos
    nuevo_usuario = Usuario(
        nombre=nombre,
        email=email,
        contraseña=hashed_password
    )

    db.session.add(nuevo_usuario)
    db.session.commit()

    #Si la solicitud es JSON, respondemos con un mensaje JSON, de lo contrario, redirigimos al formulario de login
    if request.is_json:
        return jsonify({"mensaje": "Usuario registrado con éxito"}), 201
    else:
        return render_template('login.html', mensaje="Usuario registrado con éxito")

#Inicio de sesión 
@main.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    contrasena = request.form.get('contraseña')

    #Verificamos que los datos estén presentes
    if not email or not contrasena:
        return render_template('login.html', mensaje="Faltan datos")
    
    #Buscamos al usuario por su email
    usuario = Usuario.query.filter_by(email=email).first()
    
    #verificamos la contraseña con y realizamos el login 
    if usuario and check_password_hash(usuario.contraseña, contrasena):
        login_user(usuario)
        return render_template('foro.html', mensaje="Login exitoso")
    else:
        return render_template('login.html', mensaje="Credenciales inválidas")

#Creamos una nueva pregunta
@main.route('/crear-pregunta', methods=['GET', 'POST'])
@login_required #Solo los usuarios autenticados pueden crear preguntas
def crear_pregunta():
    form = PreguntaForm()
    if form.validate_on_submit():
        nueva_pregunta = Pregunta(
            titulo=form.titulo.data,
            materia=form.materia.data,
            contenido=form.contenido.data,
            id_usuario=current_user.id #Relaciona la pregunta con el usaurio actual
        )
        db.session.add(nueva_pregunta)
        db.session.commit()

        #Mensaje de éxito y redireccionamos al foro
        flash('Pregunta creada con éxito', 'success')
        return redirect(url_for('main.foro_view'))
    
    #Si no es una solicitud POST, mostramos el formulario
    return render_template('crear_pregunta.html', form=form)