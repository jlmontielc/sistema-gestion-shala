from app import db

class Clase(db.Model):
    __tablename__ = 'clase'

    id = db.Column(db.Integer, primary_key=True)
    shala_id = db.Column(db.Integer, db.ForeignKey('shala.id'))
    instructor_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    titulo = db.Column(db.String(150))
    descripcion = db.Column(db.Text)
    fecha_hora = db.Column(db.DateTime)
    duracion_min = db.Column(db.Integer)
    capacidad = db.Column(db.Integer)
    modalidad = db.Column(db.Enum('PRESENCIAL', 'ONLINE'))
    room_link = db.Column(db.String(255))

    reservas = db.relationship('Reserva', backref='clase', lazy=True)
