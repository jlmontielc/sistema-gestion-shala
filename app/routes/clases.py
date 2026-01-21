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
    clases = Clase.query.order_by(Clase.fecha_hora.asc()).all()
    
    # Creamos una tabla HTML sencilla
    html = """
    <h1>📅 Calendario de Clases</h1>
    <p>Bienvenido. Aquí puedes ver y reservar tus clases.</p>
    <table border="1" cellpadding="10">
        <tr>
            <th>Clase</th>
            <th>Fecha</th>
            <th>Instructor</th>
            <th>Acción</th>
        </tr>
    """
    
    for c in clases:
        html += f"""
        <tr>
            <td>{c.titulo}</td>
            <td>{c.fecha_hora}</td>
            <td>Profe ID {c.instructor_id}</td> <td>
                <a href="/reservas/crear/{c.id}">Reservar Ahora</a>
            </td>
        </tr>
        """
    
    html += "</table><br><a href='/dashboard'>Volver al inicio</a>"
    return html