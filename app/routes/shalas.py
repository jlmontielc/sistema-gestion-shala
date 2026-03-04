from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.shala import Shala
from app.routes.decoradores import role_required

shalas_bp = Blueprint('shalas', __name__, url_prefix='/shalas')

@shalas_bp.route('/crear', methods=['GET', 'POST'])
@login_required
@role_required('ADMIN', 'ADMIN_SHALA')
def crear_shala():

    if current_user.rol == 'ADMIN_SHALA' and current_user.shala_id is not None:
        flash('Ya tienes una Shala asignada. No puedes crear otra.', 'error')
        return redirect(url_for('shalas.listar_shalas'))

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        direccion = request.form.get('direccion')
        telefono = request.form.get('telefono')
        descripcion = request.form.get('descripcion')
        logo_url = request.form.get('logo_url')
        
        if not nombre or not direccion:
            flash('Nombre y dirección son campos obligatorios', 'error')
            return redirect(url_for('shalas.crear_shala'))
        
        nueva_shala = Shala(
            nombre=nombre,
            direccion=direccion,
            telefono=telefono,
            descripcion=descripcion,
            logo_url=logo_url,
            admin_shala_id=current_user.id if current_user.rol == 'ADMIN_SHALA' else None
        )
        
        db.session.add(nueva_shala)
        db.session.flush()

        if current_user.rol == 'ADMIN_SHALA':
            current_user.shala_id = nueva_shala.id

        db.session.commit()
        
        flash(f'✅ Shala "{nombre}" creada exitosamente', 'success')
        return redirect(url_for('shalas.listar_shalas'))
    
    return render_template('crear_shala.html')

@shalas_bp.route('/listar')
@login_required
def listar_shalas():

    if current_user.rol == 'ADMIN':
        shalas = Shala.query.all()
    elif current_user.rol == 'ADMIN_SHALA':
        shalas = Shala.query.filter_by(admin_shala_id=current_user.id).all()
    else:
        shalas = Shala.query.all()
    
    return render_template('listar_shalas.html', shalas=shalas)

@shalas_bp.route('/detalle/<int:id>')
@login_required
def detalle_shala(id):
    shala = Shala.query.get_or_404(id)

    if current_user.rol == 'ADMIN_SHALA' and shala.admin_shala_id != current_user.id:
        flash('No tienes acceso a esta sede.', 'error')
        return redirect(url_for('shalas.listar_shalas'))
    
    from app.models.clase import Clase
    clases = Clase.query.filter_by(shala_id=id).all()
    
    return render_template('detalle_shala.html', shala=shala, clases=clases)

@shalas_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('ADMIN', 'ADMIN_SHALA')
def editar_shala(id):
    shala = Shala.query.get_or_404(id)

    if current_user.rol == 'ADMIN_SHALA' and shala.admin_shala_id != current_user.id:
        flash('No puedes editar esta sede.', 'error')
        return redirect(url_for('shalas.listar_shalas'))
    
    if request.method == 'POST':

        shala.nombre = request.form.get('nombre')
        shala.direccion = request.form.get('direccion')
        shala.telefono = request.form.get('telefono')
        shala.descripcion = request.form.get('descripcion')
        shala.logo_url = request.form.get('logo_url')
        
        db.session.commit()
        flash(f'✅ Shala "{shala.nombre}" actualizada exitosamente', 'success')
        return redirect(url_for('shalas.detalle_shala', id=id))
    
    return render_template('editar_shala.html', shala=shala)

@shalas_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
@role_required('ADMIN')
def eliminar_shala(id):
    shala = Shala.query.get_or_404(id)
    
    if shala.clases:
        flash('❌ No se puede eliminar la shala porque tiene clases asociadas', 'error')
        return redirect(url_for('shalas.listar_shalas'))
    
    db.session.delete(shala)
    db.session.commit()
    
    flash(f'✅ Shala "{shala.nombre}" eliminada exitosamente', 'success')
    return redirect(url_for('shalas.listar_shalas'))