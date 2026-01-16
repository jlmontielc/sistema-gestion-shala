from app import db
from datetime import datetime

class Asistencia(db.Model):
    __tablename__ = 'asistencia'

    id = db.Column(db.Integer, primary_key=True)
    reserva_id = db.Column(db.Integer, db.ForeignKey('reserva.id'))
    estado_asistencia = db.Column(db.Enum('ASISTIO', 'FALTO'))
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
