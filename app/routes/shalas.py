from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app import db
from app.models.shala import Shala
from app.routes.decoradores import role_required

shalas_bp = Blueprint('shalas', __name__, url_prefix='/shalas')

# Ruta para crear nueva shala
@shalas_bp.route('/crear', methods=['GET', 'POST'])
@login_required
@role_required('ADMIN')
def crear_shala():
    if request.method == 'POST':
        # Recibir datos del formulario
        nombre = request.form.get('nombre')
        direccion = request.form.get('direccion')
        telefono = request.form.get('telefono')
        descripcion = request.form.get('descripcion')
        logo_url = request.form.get('logo_url')
        
        # Validaciones básicas
        if not nombre or not direccion:
            flash('Nombre y dirección son campos obligatorios', 'error')
            return redirect(url_for('shalas.crear_shala'))
        
        # Crear nueva shala
        nueva_shala = Shala(
            nombre=nombre,
            direccion=direccion,
            telefono=telefono,
            descripcion=descripcion,
            logo_url=logo_url
        )
        
        db.session.add(nueva_shala)
        db.session.commit()
        
        flash(f'✅ Shala "{nombre}" creada exitosamente', 'success')
        return redirect(url_for('shalas.listar_shalas'))
    
    return render_template('crear_shala.html')

# Ruta para listar todas las shalas
@shalas_bp.route('/listar')
@login_required
def listar_shalas():
    # Admin ve todas, instructores y yoguis ven solo activas
    if current_user.rol == 'ADMIN':
        shalas = Shala.query.all()
    else:
        # Por ahora, todos ven todas las shalas
        shalas = Shala.query.all()
    
    return render_template('listar_shalas.html', shalas=shalas)

# Ruta para ver detalle de una shala
@shalas_bp.route('/detalle/<int:id>')
@login_required
def detalle_shala(id):
    shala = Shala.query.get_or_404(id)
    
    # Obtener clases de esta shala
    from app.models.clase import Clase
    clases = Clase.query.filter_by(shala_id=id).all()
    
    return render_template('detalle_shala.html', shala=shala, clases=clases)

# Ruta para editar shala
@shalas_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('ADMIN')
def editar_shala(id):
    shala = Shala.query.get_or_404(id)
    
    if request.method == 'POST':
        # Actualizar datos
        shala.nombre = request.form.get('nombre')
        shala.direccion = request.form.get('direccion')
        shala.telefono = request.form.get('telefono')
        shala.descripcion = request.form.get('descripcion')
        shala.logo_url = request.form.get('logo_url')
        
        db.session.commit()
        flash(f'✅ Shala "{shala.nombre}" actualizada exitosamente', 'success')
        return redirect(url_for('shalas.detalle_shala', id=id))
    
    return render_template('editar_shala.html', shala=shala)

# Ruta para eliminar shala (solo ADMIN)
@shalas_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
@role_required('ADMIN')
def eliminar_shala(id):
    shala = Shala.query.get_or_404(id)
    
    # Verificar si hay clases asociadas
    if shala.clases:
        flash('❌ No se puede eliminar la shala porque tiene clases asociadas', 'error')
        return redirect(url_for('shalas.listar_shalas'))
    
    db.session.delete(shala)
    db.session.commit()
    
    flash(f'✅ Shala "{shala.nombre}" eliminada exitosamente', 'success')
    return redirect(url_for('shalas.listar_shalas'))