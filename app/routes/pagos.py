from flask import Blueprint, request, redirect, url_for, current_app, render_template, flash, abort
from flask_login import login_required, current_user
from app import db
from app.models import Clase, Reserva, Pago, Paquete
from decimal import Decimal
import stripe

pagos_bp = Blueprint('pagos', __name__)

@pagos_bp.route('/pagar/<int:clase_id>', methods=['POST'])
@login_required
def iniciar_pago(clase_id):
    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']

    clase = Clase.query.get_or_404(clase_id)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': clase.titulo,
                },
                'unit_amount': int(getattr(clase, 'precio', 0) * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('pagos.pago_exitoso', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('pagos.pago_cancelado', _external=True),
        metadata={
            'usuario_id': current_user.id,
            'clase_id': clase.id
        }
    )

    return redirect(session.url)

@pagos_bp.route('/crear-sesion-pago')  # ✅ Español
@login_required
def crear_sesion_pago():  # ✅ Español
    paquete_id = request.args.get('paquete_id')
    if not paquete_id:
        abort(400)

    paquete = Paquete.query.get_or_404(paquete_id)

    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': paquete.nombre,
                },
                'unit_amount': int(paquete.precio * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('pagos.pago_exitoso', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('pagos.pago_cancelado', _external=True),
        metadata={
            'usuario_id': current_user.id,
            'paquete_id': paquete.id
        }
    )

    return redirect(session.url, code=303)

@pagos_bp.route('/pago-exitoso')  # ✅ Español
@login_required
def pago_exitoso():  # ✅ Español
    session_id = request.args.get('session_id')
    if not session_id:
        flash('No se recibió información de pago.', 'danger')
        return redirect(url_for('auth.panel'))

    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
    try:
        session = stripe.checkout.Session.retrieve(session_id, expand=['payment_intent'])
    except Exception:
        flash('Error al verificar la sesión de pago.', 'danger')
        return redirect(url_for('auth.panel'))

    metadata = session.get('metadata', {}) or {}
    amount_cents = None
    payment_intent = session.get('payment_intent')
    if payment_intent and isinstance(payment_intent, dict):
        amount_cents = payment_intent.get('amount_received')
    if not amount_cents:
        amount_cents = session.get('amount_total')

    monto = Decimal(0)
    if amount_cents:
        monto = Decimal(amount_cents) / Decimal(100)

    pago = Pago(
        yogui_id=current_user.id,
        paquete_id=metadata.get('paquete_id'),
        monto=monto,
        metodo_pago='STRIPE',
        estado='COMPLETADO'
    )

    db.session.add(pago)
    db.session.commit()

    if metadata.get('paquete_id'):
        paquete = Paquete.query.get(metadata.get('paquete_id'))
        if paquete:
            current_user.saldo_clases = (current_user.saldo_clases or 0) + (paquete.sesiones_incluidas or 0)
            db.session.commit()
        flash('Compra de paquete completada. Gracias.', 'success')
        return render_template('pago_exitoso.html', paquete=paquete, saldo=current_user.saldo_clases)

    clase_id = metadata.get('clase_id')
    if clase_id:
        reserva = Reserva(
            clase_id=clase_id,
            yogui_id=current_user.id,
            estado='RESERVADO',
            pago_id=pago.id
        )
        db.session.add(reserva)
        db.session.commit()
        flash('Reserva confirmada. Nos vemos en clase.', 'success')
        return render_template('pago_exitoso.html')

    flash('Pago procesado, pero no se pudo asociar a ninguna acción.', 'warning')
    return render_template('pago_exitoso.html')

@pagos_bp.route('/pago-cancelado')  # ✅ Español
@login_required
def pago_cancelado():  # ✅ Español
    return render_template('pago_cancelado.html')