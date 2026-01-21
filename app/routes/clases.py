# app/routes/clases.py
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from app.models.clase import Clase
from app.models.shala import Shala
from app.routes.decorators import role_required

clases_bp = Blueprint('clases', __name__, url_prefix='/clases')

@clases_bp.route('/crear', methods=['GET', 'POST'])
@login_required
@role_required('ADMIN', 'INSTRUCTOR')
def crear_clase():
    if request.method == 'POST':
        # Recibir datos del formulario HTML
        titulo = request.form.get('titulo')
        descripcion = request.form.get('descripcion')
        fecha_str = request.form.get('fecha_hora') 
        duracion = request.form.get('duracion')
        capacidad = request.form.get('capacidad')
        modalidad = request.form.get('modalidad')
        link = request.form.get('room_link')
        
        # Convertir texto a fecha real
        fecha_hora = datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M')

        # IMPORTANTE: Asumimos que la Shala ID 1 existe (la crearemos en la prueba)
        nueva_clase = Clase(
            titulo=titulo,
            descripcion=descripcion,
            fecha_hora=fecha_hora,
            duracion_min=int(duracion),
            capacidad=int(capacidad),
            modalidad=modalidad,
            room_link=link,
            instructor_id=current_user.id,
            shala_id=1 
        )

        db.session.add(nueva_clase)
        db.session.commit()

        return "¡Clase creada exitosamente! <a href='/dashboard'>Volver</a>"

    return render_template('crear_clase.html')

@clases_bp.route('/listar')
@login_required
def listar_clases():
    clases = Clase.query.all()
    # Simple vista rápida para ver si funcionó
    html = "<h1>Clases Disponibles</h1><ul>"
    for c in clases:
        html += f"<li>{c.titulo} - {c.fecha_hora}</li>"
    html += "</ul>"
    return html