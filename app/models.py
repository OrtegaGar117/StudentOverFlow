import uuid #Generamos IDs únicos 
from datetime import datetime #Registramos la fecha de creación 
from . import db
from flask_login import UserMixin 

#Modelo de usuario (tabla:usuarios)
class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    #Generamos un ID único para cada usuario
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    contraseña = db.Column(db.String, nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    #Relaciones con otras tablas
    preguntas = db.relationship('Pregunta', backref='autor', lazy=True)
    respuestas = db.relationship('Respuesta', backref='autor', lazy=True)
 
#Modelo de pregunta (tabla:preguntas)
class Pregunta(db.Model):
    __tablename__ = 'preguntas'
    #Generamos un ID único para cada pregunta
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    id_usuario = db.Column(db.String, db.ForeignKey('usuarios.id'), nullable=False)
    titulo = db.Column(db.String, nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    materia = db.Column(db.String, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    #Relación con respuestas
    respuestas = db.relationship('Respuesta', backref='pregunta', lazy=True)

#Modelo de respuesta (tabla:respuestas)
class Respuesta(db.Model):
    __tablename__ = 'respuestas'
    #Generamos un ID único para cada respuesta
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    id_pregunta = db.Column(db.String, db.ForeignKey('preguntas.id'), nullable=False)
    id_usuario = db.Column(db.String, db.ForeignKey('usuarios.id'), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    es_aceptada = db.Column(db.Boolean, default=False)

#Modelo de voto (tabla:votos)
class Voto(db.Model):
    __tablename__ = 'votos'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    id_usuario = db.Column(db.String, db.ForeignKey('usuarios.id'), nullable=False)
    tipo = db.Column(db.String, nullable=False)  # 'positivo' o 'negativo'
    #Relaciones con preguntas y respuestas
    id_pregunta = db.Column(db.String, db.ForeignKey('preguntas.id'), nullable=True)
    id_respuesta = db.Column(db.String, db.ForeignKey('respuestas.id'), nullable=True)
