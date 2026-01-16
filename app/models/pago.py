from app import db
from datetime import datetime

class Pago(db.Model):
    __tablename__ = 'pago'

    id = db.Column(db.Integer, primary_key=True)
    yogui_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    paquete_id = db.Column(db.Integer, db.ForeignKey('paquete.id'))
    monto = db.Column(db.Numeric(10, 2))
    metodo_pago = db.Column(db.String(80))
    estado = db.Column(
        db.Enum('PENDIENTE', 'COMPLETADO', 'REEMBOLSADO'),
        default='PENDIENTE'
    )
    fecha_pago = db.Column(db.DateTime, default=datetime.utcnow)
