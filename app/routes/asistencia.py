# app/routes/asistencia.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.clase import Clase
from app.models.reserva import Reserva
from app.models.asistencia import Asistencia
from app.routes.decoradores import role_required

asistencia_bp = Blueprint('asistencia', __name__, url_prefix='/asistencia')

@asistencia_bp.route('/tomar/<int:clase_id>', methods=['GET', 'POST'])
@login_required
@role_required('ADMIN', 'INSTRUCTOR')
def tomar_asistencia(clase_id):
    clase = Clase.query.get_or_404(clase_id)
    reservas = Reserva.query.filter_by(clase_id=clase_id, estado='RESERVADO').all()

    if request.method == 'POST':
        for reserva in reservas:
            # 1. Ver si marcó el check de asistencia
            asistio_form = request.form.get(f'asistencia_{reserva.id}')
            estado = 'ASISTIO' if asistio_form else 'FALTO'
            
            # 2. Atrapar el comentario que escribió el profe
            texto_nota = request.form.get(f'comentario_{reserva.id}')

            # 3. Guardar en la tabla
            nueva_asistencia = Asistencia(
                reserva_id=reserva.id,
                estado_asistencia=estado,
                comentario=texto_nota # Guardamos la nota aquí
            )
            db.session.add(nueva_asistencia)
            
            # Cambiamos el estado de la reserva
            reserva.estado = 'ASISTIDO' if estado == 'ASISTIO' else 'NO_SHOW'

        db.session.commit()
        return "<h1>¡Asistencia y Notas Guardadas! ✅</h1><a href='/panel'>Volver al Panel</a>"

    return render_template('tomar_asistencia.html', clase=clase, reservas=reservas)
@asistencia_bp.route('/mis-notas')
@login_required
@role_required('YOGUI')
def mis_notas():
    # Buscamos todas las asistencias asociadas a las reservas de este yogui
    asistencias = Asistencia.query.join(Reserva).filter(
        Reserva.yogui_id == current_user.id,
        Asistencia.comentario != '',
        Asistencia.comentario.isnot(None)
    ).all()
    
    html = "<h1>📈 Mi Progreso y Notas</h1><ul>"
    if not asistencias:
        html += "<p>Aún no tienes notas de tus instructores.</p>"
    else:
        for a in asistencias:
            # 👇 ESTA ES LA MAGIA NUEVA 👇
            # Buscamos la reserva y la clase manualmente usando sus IDs
            reserva = Reserva.query.get(a.reserva_id)
            clase = Clase.query.get(reserva.clase_id)
            
            # Ahora sí podemos sacar la fecha y el título sin errores
            fecha = clase.fecha_hora.strftime('%d/%m/%Y')
            html += f"<li><strong>{fecha} - {clase.titulo}:</strong> {a.comentario}</li><br>"
            
    html += "</ul><a href='/panel' style='padding: 8px 15px; background: #6c757d; color: white; text-decoration: none; border-radius: 5px;'>Volver al Panel</a>"
    return html