from app import db

class Shala(db.Model):
    __tablename__ = 'shala'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    direccion = db.Column(db.String(255))
    lat = db.Column(db.Numeric(10, 7))
    lng = db.Column(db.Numeric(10, 7))
    logo_url = db.Column(db.String(255))
    telefono = db.Column(db.String(30))
    descripcion = db.Column(db.Text)

    paquetes = db.relationship('Paquete', backref='shala', lazy=True)
    clases = db.relationship('Clase', backref='shala', lazy=True)
