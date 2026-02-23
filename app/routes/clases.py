# app/routes/clases.py
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from app.models.clase import Clase
from app.models.shala import Shala
from app.routes.decoradores import role_required

clases_bp = Blueprint('clases', __name__, url_prefix='/clases')

@clases_bp.route('/crear', methods=['GET', 'POST'])
@login_required
@role_required('ADMIN', 'INSTRUCTOR')
def crear_clase():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descripcion = request.form.get('descripcion')
        fecha_str = request.form.get('fecha_hora') 
        duracion = request.form.get('duracion')
        capacidad = request.form.get('capacidad')
        modalidad = request.form.get('modalidad')
        link = request.form.get('room_link')
        
        # 👇 NUEVO: Capturamos la sede que eligió el profe aaaaa
        shala_id = request.form.get('shala_id') 
        
        fecha_hora = datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M')

        nueva_clase = Clase(
            titulo=titulo,
            descripcion=descripcion,
            fecha_hora=fecha_hora,
            duracion_min=int(duracion),
            capacidad=int(capacidad),
            modalidad=modalidad,
            room_link=link,
            instructor_id=current_user.id,
            shala_id=int(shala_id)  # 👇 ¡Adiós al "1" quemado!
        )

        db.session.add(nueva_clase)
        db.session.commit()

        return "¡Clase creada exitosamente! <a href='/panel'>Volver</a>"

    # 👇 NUEVO: Buscamos las sedes para mostrarlas en el formulario
    todas_las_shalas = Shala.query.all()
    return render_template('crear_clase.html', shalas=todas_las_shalas)


@clases_bp.route('/listar')
@login_required
def listar_clases():
    clases = Clase.query.order_by(Clase.fecha_hora.asc()).all()
    
    # Encabezado de la página
    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Lista de Clases</title>
        <style>
            body { font-family: sans-serif; padding: 20px; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
            th { background-color: #f2f2f2; }
            .btn { text-decoration: none; padding: 8px 15px; border-radius: 5px; color: white; }
            .btn-blue { background-color: #007bff; }
            .btn-green { background-color: #28a745; }
            .btn-gray { background-color: #6c757d; }
        </style>
    </head>
    <body>
        <h1>📅 Calendario de Clases</h1>
        <a href="/panel" class="btn btn-gray">⬅ Volver al Panel</a>
        
        <table>
            <thead>
                <tr>
                    <th>Clase</th>
                    <th>Fecha</th>
                    <th>Horario</th>
                    <th>Modalidad</th>
                    <th>Acción</th>
                </tr>
            </thead>
            <tbody>
    """
    
    # Lógica para mostrar botones según el Rol
    for c in clases:
        boton_accion = ""
        
        # SI ERES ALUMNO (YOGUI) -> Ves botón de RESERVAR
        if current_user.rol == 'YOGUI':
            boton_accion = f'<a href="/reservas/crear/{c.id}" class="btn btn-blue">Reservar Lugar</a>'
            
        # SI ERES INSTRUCTOR O ADMIN -> Ves botón de TOMAR ASISTENCIA
        elif current_user.rol in ['INSTRUCTOR', 'ADMIN']:
            boton_accion = f'<a href="/asistencia/tomar/{c.id}" class="btn btn-green">📋 Tomar Lista</a>'

        html += f"""
        <tr>
            <td><strong>{c.titulo}</strong></td>
            <td>{c.fecha_hora.strftime('%d/%m/%Y')}</td>
            <td>{c.fecha_hora.strftime('%H:%M')} ({c.duracion_min} min)</td>
            <td>{c.modalidad}</td>
            <td>
                {boton_accion}
            </td>
        </tr>
        """
    
    html += """
            </tbody>
        </table>
    </body>
    </html>
    """
    return html