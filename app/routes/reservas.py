# app/routes/reservas.py
from flask import Blueprint, redirect, url_for, render_template
from flask_login import login_required, current_user
from app import db
from app.models.reserva import Reserva
from app.models.clase import Clase
from app.models.notificacion import Notificacion
from app.routes.decoradores import role_required

reservas_bp = Blueprint('reservas', __name__, url_prefix='/reservas')

@reservas_bp.route('/crear/<int:clase_id>')
@login_required
@role_required('YOGUI') # Solo los alumnos pueden reservar
def crear_reserva(clase_id):
    clase = Clase.query.get_or_404(clase_id)
    
    # --- 1. NUEVO: EL CANDADO DE SEGURIDAD (Cobro) ---
    if current_user.saldo_clases < 1:
        return """
        <h1>⛔ Saldo Insuficiente</h1>
        <p>No tienes clases disponibles en tu cuenta.</p>
        <p>Por favor, compra un paquete para continuar.</p>
        <br>
        <a href='/paquetes/listar'>🛒 Ir a Comprar Paquetes</a> | <a href='/panel'>Volver</a>
        """

    # 2. Verificar si la clase está llena (Lógica antigua)
    total_reservas = Reserva.query.filter_by(clase_id=clase_id, estado='RESERVADO').count()
    if total_reservas >= clase.capacidad:
        return "<h1>Error: La clase está llena 🚫</h1><a href='/clases/listar'>Volver</a>"

    # 3. Verificar si ya reservó (Lógica antigua)
    reserva_existente = Reserva.query.filter_by(clase_id=clase_id, yogui_id=current_user.id).first()
    if reserva_existente:
        return "<h1>Ya estás inscrito en esta clase ✅</h1><a href='/clases/listar'>Volver</a>"

    # --- 4. NUEVO: COBRAR LA ENTRADA ---
    # Le restamos 1 al saldo del usuario
    current_user.saldo_clases -= 1 

    # Creamos la reserva
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
    
    return f"""
    <h1>¡Reserva Confirmada! 🎉</h1>
    <p>Te esperamos en el mat.</p>
    <hr>
    <p>➖ Se ha descontado 1 clase de tu cuenta.</p>
    <p>Te quedan: <strong>{current_user.saldo_clases} clases</strong> disponibles.</p>
    <a href='/clases/listar'>Volver al calendario</a>
    """

@reservas_bp.route('/mis-reservas')
@login_required
@role_required('YOGUI')
def mis_reservas():
    # Buscar todas las reservas de este usuario
    mis_reservas = Reserva.query.filter_by(yogui_id=current_user.id).all()
    
    html = "<h1>Mis Reservas</h1><ul>"
    for r in mis_reservas:
        # Si la reserva está activa, mostramos el botón de cancelar
        boton_cancelar = ""
        if r.estado == 'RESERVADO':
            boton_cancelar = f" <a href='/reservas/cancelar/{r.id}' style='color: white; background-color: red; padding: 2px 5px; text-decoration: none; border-radius: 3px; font-size: 12px;'>❌ Cancelar</a>"
            
        html += f"<li>{r.clase.titulo} - {r.clase.fecha_hora.strftime('%d/%m/%Y %H:%M')} ({r.estado}){boton_cancelar}</li><br>"
        
    html += "</ul><a href='/clases/listar'>Reservar más clases</a> | <a href='/panel'>Volver al Panel</a>"
    return html


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
    # 1. Buscamos la reserva en la base de datos
    reserva = Reserva.query.get_or_404(reserva_id)
    
    # 2. Seguridad: Verificamos que sea del usuario actual
    if reserva.yogui_id != current_user.id:
        return "<h1>Error: Esta reserva no es tuya 🚫</h1><a href='/reservas/mis-reservas'>Volver</a>"
        
    # 3. Seguridad: Evitar que cancele algo ya cancelado y gane saldo infinito
    if reserva.estado == 'CANCELADO':
        return "<h1>La reserva ya estaba cancelada.</h1><a href='/reservas/mis-reservas'>Volver</a>"

    # 4. HACEMOS EL REEMBOLSO:
    reserva.estado = 'CANCELADO'          # Cambiamos el estado
    current_user.saldo_clases += 1        # Le devolvemos 1 clase a su cartera

    # Guardamos los cambios en la base de datos
    db.session.commit()
    
    return f"""
    <h1>¡Reserva Cancelada! 🛑</h1>
    <p>Se ha devuelto 1 clase a tu cuenta.</p>
    <p>Tu saldo actual es: <strong>{current_user.saldo_clases} clases</strong>.</p>
    <br>
    <a href='/reservas/mis-reservas'>Volver a mis reservas</a> | <a href='/panel'>Volver al panel</a>
    """
