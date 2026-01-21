# app/routes/reservas.py
from flask import Blueprint, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models.reserva import Reserva
from app.models.clase import Clase
from app.routes.decorators import role_required

reservas_bp = Blueprint('reservas', __name__, url_prefix='/reservas')

@reservas_bp.route('/crear/<int:clase_id>')
@login_required
@role_required('YOGUI') # Solo los alumnos pueden reservar
def crear_reserva(clase_id):
    clase = Clase.query.get_or_404(clase_id)
    
    # 1. Verificar si la clase está llena
    # Contamos cuántas reservas activas tiene esa clase
    total_reservas = Reserva.query.filter_by(clase_id=clase_id, estado='RESERVADO').count()
    
    if total_reservas >= clase.capacidad:
        return "<h1>Error: La clase está llena 🚫</h1><a href='/clases/listar'>Volver</a>"

    # 2. Verificar si el usuario YA reservó esa clase (para no duplicar)
    reserva_existente = Reserva.query.filter_by(clase_id=clase_id, yogui_id=current_user.id).first()
    if reserva_existente:
        return "<h1>Ya estás inscrito en esta clase ✅</h1><a href='/clases/listar'>Volver</a>"

    # 3. Crear la reserva
    nueva_reserva = Reserva(
        clase_id=clase.id,
        yogui_id=current_user.id,
        estado='RESERVADO'
    )
    
    db.session.add(nueva_reserva)
    db.session.commit()
    
    return "<h1>¡Reserva Confirmada! 🎉</h1><p>Nos vemos en el mat.</p><a href='/clases/listar'>Volver al calendario</a>"

@reservas_bp.route('/mis-reservas')
@login_required
@role_required('YOGUI')
def mis_reservas():
    # Buscar todas las reservas de este usuario
    mis_reservas = Reserva.query.filter_by(yogui_id=current_user.id).all()
    
    html = "<h1>Mis Reservas</h1><ul>"
    for r in mis_reservas:
        html += f"<li>{r.clase.titulo} - {r.clase.fecha_hora} ({r.estado})</li>"
    html += "</ul><a href='/clases/listar'>Reservar más clases</a>"
    return html