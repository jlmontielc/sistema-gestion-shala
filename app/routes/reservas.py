from flask import Blueprint, redirect, url_for, render_template, flash
from flask_login import login_required, current_user
from app import db
from app.models.reserva import Reserva
from app.models.clase import Clase
from app.models.notificacion import Notificacion
from app.routes.decoradores import role_required

reservas_bp = Blueprint('reservas', __name__, url_prefix='/reservas')

@reservas_bp.route('/crear/<int:clase_id>')
@login_required
@role_required('YOGUI')
def crear_reserva(clase_id):
    clase = Clase.query.get_or_404(clase_id)
    
    # 1. Saldo Insuficiente
    if current_user.saldo_clases < 1:
        flash('⛔ Saldo Insuficiente. No tienes clases disponibles. Por favor, compra un paquete para continuar.', 'error')
        return redirect(url_for('paquetes.listar_paquetes'))

    # 2. Verificar si la clase está llena
    total_reservas = Reserva.query.filter_by(clase_id=clase_id, estado='RESERVADO').count()
    if total_reservas >= clase.capacidad:
        flash('Error: La clase está llena 🚫', 'error')
        return redirect(url_for('clases.listar_clases'))

    # 3. Verificar si ya reservó
    reserva_existente = Reserva.query.filter_by(clase_id=clase_id, yogui_id=current_user.id).first()
    if reserva_existente:
        flash('Ya estás inscrito en esta clase ✅', 'info')
        return redirect(url_for('clases.listar_clases'))

    # 4. COBRAR LA ENTRADA
    current_user.saldo_clases -= 1 

    nueva_reserva = Reserva(
        clase_id=clase.id,
        yogui_id=current_user.id,
        estado='RESERVADO'
    )

    notificacion = Notificacion(
        yogui_id=current_user.id,
        titulo='Reserva confirmada',
        mensaje=(
            f"Tu reserva para \"{clase.titulo}\" del "
            f"{clase.fecha_hora.strftime('%d/%m/%Y a las %H:%M')} ha sido confirmada."
        )
    )
    
    db.session.add(nueva_reserva)
    db.session.add(notificacion)
    db.session.commit()
    
    # Éxito
    flash(f'¡Reserva Confirmada! 🎉 Se descontó 1 clase. Te quedan: {current_user.saldo_clases} clases.', 'success')
    return redirect(url_for('clases.listar_clases'))

@reservas_bp.route('/mis-reservas')
@login_required
@role_required('YOGUI')
def mis_reservas():
    # Buscamos todas las reservas de este usuario ordenadas por las más recientes
    mis_reservas = Reserva.query.filter_by(yogui_id=current_user.id).order_by(Reserva.fecha_reserva.desc()).all()
    
    # En lugar de devolver texto plano, renderizamos una plantilla bonita
    return render_template('mis_reservas.html', reservas=mis_reservas)


@reservas_bp.route('/notificaciones')
@login_required
@role_required('YOGUI')
def ver_notificaciones():
    notificaciones = (
        Notificacion.query
        .filter_by(yogui_id=current_user.id)
        .order_by(Notificacion.fecha_creacion.desc())
        .all()
    )

    return render_template('notificaciones.html', notificaciones=notificaciones)


@reservas_bp.route('/notificaciones/marcar-todas-leidas')
@login_required
@role_required('YOGUI')
def marcar_notificaciones_leidas():
    (
        Notificacion.query
        .filter_by(yogui_id=current_user.id, leida=False)
        .update({'leida': True})
    )
    db.session.commit()

    return redirect(url_for('reservas.ver_notificaciones'))

@reservas_bp.route('/cancelar/<int:reserva_id>')
@login_required
@role_required('YOGUI')
def cancelar_reserva(reserva_id):
    reserva = Reserva.query.get_or_404(reserva_id)
    
    if reserva.yogui_id != current_user.id:
        flash('Error: Esta reserva no es tuya 🚫', 'error')
        return redirect(url_for('reservas.mis_reservas'))
        
    if reserva.estado == 'CANCELADO':
        flash('La reserva ya estaba cancelada.', 'info')
        return redirect(url_for('reservas.mis_reservas'))

    # Reembolso
    reserva.estado = 'CANCELADO'
    current_user.saldo_clases += 1

    db.session.commit()
    
    flash(f'¡Reserva Cancelada! 🛑 Se devolvió 1 clase a tu cuenta. Saldo actual: {current_user.saldo_clases}.', 'success')
    return redirect(url_for('reservas.mis_reservas'))