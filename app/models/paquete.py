from app import db

class Paquete(db.Model):
    __tablename__ = 'paquete'

    id = db.Column(db.Integer, primary_key=True)
    shala_id = db.Column(db.Integer, db.ForeignKey('shala.id'))
    nombre = db.Column(db.String(120))
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Numeric(10, 2))
    sesiones_incluidas = db.Column(db.Integer)
    validez_dias = db.Column(db.Integer)
    activo = db.Column(db.Boolean, default=True)
