from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.routes.decoradores import role_required

analisis_bp = Blueprint('analisis', __name__, url_prefix='/analisis')

@analisis_bp.route('/')
@login_required
@role_required('ADMIN', 'ADMIN_SHALA')
def dashboard():
    
    from app.models.usuario import Usuario
    from app.models.reserva import Reserva
    from app.models.clase import Clase
    from app.models.pago import Pago
    
    
    if current_user.rol == 'ADMIN_SHALA':
        if not current_user.shala_id:
            flash('Aún no tienes una sede asignada.', 'error')
            return redirect(url_for('auth.panel'))

        clases_ids = db.session.query(Clase.id).filter(Clase.shala_id == current_user.shala_id).subquery()
        total_usuarios = Usuario.query.count()
        total_clases = Clase.query.filter_by(shala_id=current_user.shala_id).count()
        total_reservas = Reserva.query.filter(Reserva.clase_id.in_(clases_ids)).count()
        reservas_activas = Reserva.query.filter(Reserva.estado == 'RESERVADO', Reserva.clase_id.in_(clases_ids)).count()
        pagos_completados = db.session.query(db.func.sum(Pago.monto)).join(Usuario, Usuario.id == Pago.yogui_id).filter(Pago.estado == 'COMPLETADO').scalar() or 0
        usuarios_yoguis = Usuario.query.filter_by(rol='YOGUI').count()
        usuarios_instructores = Usuario.query.join(Usuario.instructor).filter_by(shala_id=current_user.shala_id).count()
        usuarios_admins = Usuario.query.filter(Usuario.rol.in_(['ADMIN', 'ADMIN_SHALA'])).count()
        clases_data = Clase.query.filter_by(shala_id=current_user.shala_id).limit(10).all()
    else:
        total_usuarios = Usuario.query.count()
        total_clases = Clase.query.count()
        total_reservas = Reserva.query.count()
        reservas_activas = Reserva.query.filter_by(estado='RESERVADO').count()
        pagos_completados = db.session.query(db.func.sum(Pago.monto)).filter_by(estado='COMPLETADO').scalar() or 0
        usuarios_yoguis = Usuario.query.filter_by(rol='YOGUI').count()
        usuarios_instructores = Usuario.query.filter_by(rol='INSTRUCTOR').count()
        usuarios_admins = Usuario.query.filter(Usuario.rol.in_(['ADMIN', 'ADMIN_SHALA'])).count()
        clases_data = Clase.query.limit(10).all()
    
    return render_template('analisis.html',
        total_usuarios=total_usuarios,
        total_clases=total_clases,
        total_reservas=total_reservas,
        reservas_activas=reservas_activas,
        ingresos_totales=float(pagos_completados) if pagos_completados else 0,
        usuarios_yoguis=usuarios_yoguis,
        usuarios_instructores=usuarios_instructores,
        usuarios_admins=usuarios_admins,
        clases_data=clases_data
    )