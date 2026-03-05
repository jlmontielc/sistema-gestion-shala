from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.routes.decoradores import role_required
import io
import csv
from flask import Response

analisis_bp = Blueprint('analisis', __name__, url_prefix='/analisis')

@analisis_bp.route('/')
@login_required
@role_required('ADMIN', 'ADMIN_SHALA')
def dashboard():
    
    from app.models.usuario import Usuario
    from app.models.reserva import Reserva
    from app.models.clase import Clase
    from app.models.pago import Pago
    from app.models.paquete import Paquete
    
    
    if current_user.rol == 'ADMIN_SHALA':
        if not current_user.shala_id:
            flash('Aún no tienes una sede asignada.', 'error')
            return redirect(url_for('auth.panel'))

        clases_ids = db.session.query(Clase.id).filter(Clase.shala_id == current_user.shala_id).subquery()
        total_usuarios = Usuario.query.filter_by(shala_id=current_user.shala_id).count()
        total_clases = Clase.query.filter_by(shala_id=current_user.shala_id).count()
        total_reservas = Reserva.query.filter(Reserva.clase_id.in_(clases_ids)).count()
        reservas_activas = Reserva.query.filter(Reserva.estado == 'RESERVADO', Reserva.clase_id.in_(clases_ids)).count()
        pagos_completados = db.session.query(db.func.sum(Pago.monto)).join(Paquete, Paquete.id == Pago.paquete_id).filter(
            Pago.estado == 'COMPLETADO',
            Paquete.shala_id == current_user.shala_id
        ).scalar() or 0
        usuarios_yoguis = Usuario.query.filter_by(rol='YOGUI', shala_id=current_user.shala_id).count()
        usuarios_instructores = Usuario.query.join(Usuario.instructor).filter_by(shala_id=current_user.shala_id).count()
        usuarios_admins = Usuario.query.filter(
            Usuario.rol.in_(['ADMIN', 'ADMIN_SHALA']),
            Usuario.shala_id == current_user.shala_id
        ).count()
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

@analisis_bp.route('/exportar-usuarios')
@login_required
@role_required('ADMIN', 'ADMIN_SHALA')
def exportar_usuarios():
    from app.models.usuario import Usuario
    
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['ID', 'Nombre', 'Email', 'Rol', 'Saldo Clases'])
    
    if current_user.rol == 'ADMIN_SHALA':
        usuarios = Usuario.query.filter_by(shala_id=current_user.shala_id).all()
    else:
        usuarios = Usuario.query.all()
    
    for u in usuarios:
        cw.writerow([u.id, u.nombre, u.email, u.rol, u.saldo_clases])
    
    return Response(
        si.getvalue(), 
        mimetype="text/csv", 
        headers={"Content-Disposition": "attachment;filename=usuarios.csv"}
    )

@analisis_bp.route('/exportar-reservas')
@login_required
@role_required('ADMIN', 'ADMIN_SHALA')
def exportar_reservas():
    from app.models.reserva import Reserva
    from app.models.clase import Clase
    
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['ID', 'Clase', 'ID Alumno', 'Estado', 'Fecha'])
    
    if current_user.rol == 'ADMIN_SHALA':
        reservas = Reserva.query.join(Clase).filter(Clase.shala_id == current_user.shala_id).all()
    else:
        reservas = Reserva.query.all()
    
    for r in reservas:
        cw.writerow([r.id, r.clase.titulo, r.yogui_id, r.estado, r.fecha_reserva.strftime('%d/%m/%Y %H:%M')])
        
    return Response(
        si.getvalue(), 
        mimetype="text/csv", 
        headers={"Content-Disposition": "attachment;filename=reservas.csv"}
    )

@analisis_bp.route('/reporte-ingresos')
@login_required
@role_required('ADMIN', 'ADMIN_SHALA')
def reporte_ingresos():
    from app.models.pago import Pago
    from app.models.paquete import Paquete
    
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['ID', 'Monto ($)', 'Metodo', 'Estado', 'Fecha'])
    
    if current_user.rol == 'ADMIN_SHALA':
        pagos = Pago.query.join(Paquete).filter(Paquete.shala_id == current_user.shala_id).order_by(Pago.fecha_pago.desc()).all()
    else:
        pagos = Pago.query.order_by(Pago.fecha_pago.desc()).all()
    
    for p in pagos:
        cw.writerow([p.id, p.monto, p.metodo_pago, p.estado, p.fecha_pago.strftime('%d/%m/%Y %H:%M')])
        
    return Response(
        si.getvalue(), 
        mimetype="text/csv", 
        headers={"Content-Disposition": "attachment;filename=ingresos.csv"}
    )