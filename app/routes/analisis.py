from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app import db
from app.routes.decoradores import role_required

analisis_bp = Blueprint('analisis', __name__, url_prefix='/analisis')

@analisis_bp.route('/')
@login_required
@role_required('ADMIN')
def dashboard():
    """Panel de análisis básico para administradores"""
    
    # Obtener datos directamente con SQL si es necesario
    from app.models.usuario import Usuario
    from app.models.reserva import Reserva
    from app.models.clase import Clase
    from app.models.paquete import Paquete
    from app.models.pago import Pago
    
    # Estadísticas básicas
    total_usuarios = Usuario.query.count()
    total_clases = Clase.query.count()
    total_reservas = Reserva.query.count()
    
    # Reservas activas
    reservas_activas = Reserva.query.filter_by(estado='RESERVADO').count()
    
    # Ingresos totales
    pagos_completados = db.session.query(db.func.sum(Pago.monto)).filter_by(estado='COMPLETADO').scalar() or 0
    
    # Usuarios por rol
    usuarios_yoguis = Usuario.query.filter_by(rol='YOGUI').count()
    usuarios_instructores = Usuario.query.filter_by(rol='INSTRUCTOR').count()
    usuarios_admins = Usuario.query.filter_by(rol='ADMIN').count()
    
    # Clases más populares (simplificado)
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