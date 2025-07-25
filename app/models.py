import uuid
from datetime import datetime
from . import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    contraseña = db.Column(db.String, nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    preguntas = db.relationship('Pregunta', backref='autor', lazy=True)
    respuestas = db.relationship('Respuesta', backref='autor', lazy=True)

class Pregunta(db.Model):
    __tablename__ = 'preguntas'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    id_usuario = db.Column(db.String, db.ForeignKey('usuarios.id'), nullable=False)
    titulo = db.Column(db.String, nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    materia = db.Column(db.String, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    respuestas = db.relationship('Respuesta', backref='pregunta', lazy=True)

class Respuesta(db.Model):
    __tablename__ = 'respuestas'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    id_pregunta = db.Column(db.String, db.ForeignKey('preguntas.id'), nullable=False)
    id_usuario = db.Column(db.String, db.ForeignKey('usuarios.id'), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    es_aceptada = db.Column(db.Boolean, default=False)

class Voto(db.Model):
    __tablename__ = 'votos'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    id_usuario = db.Column(db.String, db.ForeignKey('usuarios.id'), nullable=False)
    tipo = db.Column(db.String, nullable=False)  # 'positivo' o 'negativo'
    id_pregunta = db.Column(db.String, db.ForeignKey('preguntas.id'), nullable=True)
    id_respuesta = db.Column(db.String, db.ForeignKey('respuestas.id'), nullable=True)
