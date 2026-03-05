# app/routes/asistencia.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from datetime import datetime
from app.models.clase import Clase
from app.models.reserva import Reserva
from app.models.asistencia import Asistencia
from app.routes.decoradores import role_required

asistencia_bp = Blueprint('asistencia', __name__, url_prefix='/asistencia')

@asistencia_bp.route('/tomar/<int:clase_id>', methods=['GET', 'POST'])
@login_required
@role_required('ADMIN', 'ADMIN_SHALA', 'INSTRUCTOR')
def tomar_asistencia(clase_id):
    clase = Clase.query.get_or_404(clase_id)
    
    if current_user.rol == 'INSTRUCTOR' and clase.instructor_id != current_user.id:
        flash("Solo el instructor asignado a esta clase puede tomar asistencia.", "error")
        return redirect(url_for('clases.listar_clases'))
    
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
        flash("¡Asistencia y notas guardadas correctamente! ✅", "success")
        return redirect(url_for('clases.listar_clases'))

    return render_template('tomar_asistencia.html', clase=clase, reservas=reservas)
@asistencia_bp.route('/mis-notas')
@login_required
@role_required('YOGUI')
def mis_notas():
    # Traemos TODAS las asistencias de este yogui (con o sin comentario)
    asistencias_db = Asistencia.query.join(Reserva).filter(
        Reserva.yogui_id == current_user.id
    ).all()

    # Averiguamos el mes y año actual
    hoy = datetime.now()
    mes_actual = hoy.month
    ano_actual = hoy.year

    asistencias_mes = 0
    faltas_mes = 0
    notas_mostrar = []

    for a in asistencias_db:
        # Buscamos la reserva y la clase manualmente (como hicimos antes para evitar errores)
        reserva = Reserva.query.get(a.reserva_id)
        clase = Clase.query.get(reserva.clase_id)

        # 1. Cálculos de estadísticas (Solo sumamos si la clase fue de este mes y este año)
        if clase.fecha_hora.month == mes_actual and clase.fecha_hora.year == ano_actual:
            if a.estado_asistencia == 'ASISTIO':
                asistencias_mes += 1
            elif a.estado_asistencia == 'FALTO':
                faltas_mes += 1

        # 2. Historial de comentarios (Guardamos los que tengan texto para mostrarlos)
        if a.comentario and a.comentario.strip() != '':
            notas_mostrar.append({
                'fecha': clase.fecha_hora.strftime('%d/%m/%Y'),
                'titulo': clase.titulo,
                'comentario': a.comentario
            })

    # Invertimos la lista para que el comentario más reciente salga de primero
    notas_mostrar.reverse()

    # Calculamos la tasa de asistencia
    total_clases = asistencias_mes + faltas_mes
    tasa = int((asistencias_mes / total_clases) * 100) if total_clases > 0 else 0

    meses = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    nombre_mes = meses[mes_actual]

    # Ahora en lugar de devolver texto plano, llamamos a un archivo HTML
    return render_template('mis_notas.html', 
                           nombre_mes=nombre_mes, 
                           asistencias=asistencias_mes, 
                           faltas=faltas_mes, 
                           tasa=tasa, 
                           notas=notas_mostrar)