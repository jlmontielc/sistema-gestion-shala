from app import db
from datetime import datetime
from flask_login import UserMixin

class Usuario(UserMixin, db.Model):

    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    telefono = db.Column(db.String(30))
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.Enum('ADMIN', 'INSTRUCTOR', 'YOGUI'), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    saldo_clases = db.Column(db.Integer, default=0)

    instructor = db.relationship('Instructor', backref='usuario', uselist=False)

    def __repr__(self):
        return f"<Usuario {self.email}>"

class Instructor(db.Model):
    __tablename__ = 'instructor'

    id = db.Column(db.Integer, db.ForeignKey('usuario.id'), primary_key=True)
    bio = db.Column(db.Text)
    certificaciones = db.Column(db.Text)
