# app/routes/asistencia.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models.clase import Clase
from app.models.reserva import Reserva
from app.models.asistencia import Asistencia
from app.routes.decorators import role_required

asistencia_bp = Blueprint('asistencia', __name__, url_prefix='/asistencia')

@asistencia_bp.route('/tomar/<int:clase_id>', methods=['GET', 'POST'])
@login_required
@role_required('ADMIN', 'INSTRUCTOR')
def tomar_asistencia(clase_id):
    clase = Clase.query.get_or_404(clase_id)
    
    # Obtenemos solo las reservas activas (no canceladas)
    reservas = Reserva.query.filter_by(clase_id=clase_id, estado='RESERVADO').all()

    if request.method == 'POST':
        # Recorremos cada reserva para ver qué marcó el profesor
        for reserva in reservas:
            # El checkbox en HTML enviará 'on' si está marcado
            asistio_form = request.form.get(f'asistencia_{reserva.id}')
            
            estado = 'ASISTIO' if asistio_form else 'FALTO'

            # Guardamos en la tabla Asistencia
            nueva_asistencia = Asistencia(
                reserva_id=reserva.id,
                estado_asistencia=estado
            )
            db.session.add(nueva_asistencia)
            
            # Opcional: Actualizar el estado de la reserva para saber que ya pasó
            reserva.estado = 'ASISTIDO' if estado == 'ASISTIO' else 'NO_SHOW'

        db.session.commit()
        return "<h1>¡Asistencia Guardada Correctamente! ✅</h1><a href='/dashboard'>Volver al Dashboard</a>"

    return render_template('tomar_asistencia.html', clase=clase, reservas=reservas)