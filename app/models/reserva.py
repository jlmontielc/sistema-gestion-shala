from app import db
from datetime import datetime

class Reserva(db.Model):
    __tablename__ = 'reserva'

    id = db.Column(db.Integer, primary_key=True)
    clase_id = db.Column(db.Integer, db.ForeignKey('clase.id'))
    yogui_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    estado = db.Column(
        db.Enum('RESERVADO', 'CANCELADO', 'ASISTIDO', 'NO_SHOW'),
        default='RESERVADO'
    )
    fecha_reserva = db.Column(db.DateTime, default=datetime.utcnow)
    pago_id = db.Column(db.Integer, db.ForeignKey('pago.id'), nullable=True)
