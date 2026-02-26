from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models.usuario import Usuario, Instructor
from app.models.reserva import Reserva
from app.models.pago import Pago
from app.models.clase import Clase
from app.routes.decoradores import role_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')
        rol = request.form.get('rol')

        if not nombre or not email or not password or not rol:
            flash("Datos incompletos", "error")
            return redirect(url_for('auth.registro'))

        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            flash("El correo electrónico ya está registrado", "error")
            return redirect(url_for('auth.registro'))

        password_hash = generate_password_hash(password)

        usuario = Usuario(
            nombre=nombre,
            email=email,
            password_hash=password_hash,
            rol=rol
        )

        db.session.add(usuario)
        db.session.commit()

        flash("Registro exitoso. Por favor inicia sesión.", "success")
        return redirect(url_for('auth.iniciar_sesion'))

    return render_template('registro.html')

@auth_bp.route('/iniciar-sesion', methods=['GET', 'POST'])
def iniciar_sesion():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and check_password_hash(usuario.password_hash, password):
            login_user(usuario)
            flash(f"¡Bienvenido/a {usuario.nombre}!", "success")
            return redirect(url_for('auth.panel'))

        flash("Credenciales incorrectas", "error")
        return redirect(url_for('auth.iniciar_sesion'))

    return render_template('iniciar_sesion.html')

@auth_bp.route('/panel')
@login_required
def panel():
    return render_template('panel.html', usuario=current_user)  # ✅ CAMBIADO: user → usuario

@auth_bp.route('/administracion')
@login_required
@role_required('ADMIN')
def administracion():
    return "Panel de administración"

@auth_bp.route('/gestion-clases')
@login_required
@role_required('ADMIN', 'INSTRUCTOR')
def gestion_clases():
    return "Gestión de clases"

@auth_bp.route('/mis-reservas')
@login_required
@role_required('YOGUI')
def mis_reservas():
    return "Mis reservas"

@auth_bp.route('/cerrar-sesion')
@login_required
def cerrar_sesion():
    logout_user()
    flash("Sesión cerrada correctamente", "info")
    return redirect(url_for('auth.iniciar_sesion'))

@auth_bp.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    if request.method == 'POST':
        # Guardamos los datos básicos para cualquier usuario
        current_user.nombre = request.form.get('nombre')
        current_user.telefono = request.form.get('telefono')
        
        # Si es Instructor, guardamos su biografía y certificaciones
        if current_user.rol == 'INSTRUCTOR':
            bio = request.form.get('bio')
            certificaciones = request.form.get('certificaciones')
            
            # Verificamos si ya tiene un perfil de instructor creado en la base de datos
            if not current_user.instructor:
                # Si es su primera vez, le creamos el perfil extendido
                nuevo_perfil = Instructor(id=current_user.id, bio=bio, certificaciones=certificaciones)
                db.session.add(nuevo_perfil)
            else:
                # Si ya lo tenía, simplemente lo actualizamos
                current_user.instructor.bio = bio
                current_user.instructor.certificaciones = certificaciones

        db.session.commit()
        flash("¡Perfil actualizado con éxito!", "success")
        return redirect(url_for('auth.panel'))

    return render_template('perfil.html')

@auth_bp.route('/instructor/<int:id>')
@login_required
def ver_instructor(id):
    # Buscamos al usuario por su ID
    instructor_user = Usuario.query.get_or_404(id)
    
    # Verificamos que sea un instructor o un administrador
    if instructor_user.rol not in ['INSTRUCTOR', 'ADMIN']:
        flash("El usuario no es un instructor válido.", "error")
        return redirect(url_for('auth.panel'))
        
    return render_template('perfil_instructor.html', instructor=instructor_user)

# ==========================================
# GESTIÓN DE YOGUIS (ADMIN)
# ==========================================
@auth_bp.route('/admin/yoguis')
@login_required
@role_required('ADMIN')
def listar_yoguis():
    yoguis = Usuario.query.filter_by(rol='YOGUI').all()
    return render_template('listar_yoguis.html', yoguis=yoguis)

@auth_bp.route('/admin/yogui/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('ADMIN')
def detalle_yogui(id):
    yogui = Usuario.query.get_or_404(id)
    
    if request.method == 'POST':
        # Guardar cambios editados por el admin
        yogui.nombre = request.form.get('nombre')
        yogui.email = request.form.get('email')
        yogui.telefono = request.form.get('telefono')
        yogui.saldo_clases = int(request.form.get('saldo_clases', 0))
        db.session.commit()
        flash('Datos del alumno actualizados correctamente.', 'success')
        return redirect(url_for('auth.detalle_yogui', id=id))
        
    reservas = Reserva.query.filter_by(yogui_id=id).order_by(Reserva.fecha_reserva.desc()).all()
    pagos = Pago.query.filter_by(yogui_id=id).order_by(Pago.fecha_pago.desc()).all()
    
    return render_template('detalle_yogui.html', yogui=yogui, reservas=reservas, pagos=pagos)

@auth_bp.route('/admin/yogui/eliminar/<int:id>', methods=['POST'])
@login_required
@role_required('ADMIN')
def eliminar_yogui(id):
    yogui = Usuario.query.get_or_404(id)
    if Reserva.query.filter_by(yogui_id=id).first() or Pago.query.filter_by(yogui_id=id).first():
        flash('No se puede eliminar este alumno porque tiene historial de reservas o pagos. Edita su nombre a "Inactivo" en su lugar.', 'error')
    else:
        db.session.delete(yogui)
        db.session.commit()
        flash('Alumno eliminado del sistema.', 'success')
    return redirect(url_for('auth.listar_yoguis'))

# ==========================================
# GESTIÓN DE INSTRUCTORES (ADMIN)
# ==========================================
@auth_bp.route('/admin/instructores')
@login_required
@role_required('ADMIN')
def listar_instructores():
    instructores = Usuario.query.filter_by(rol='INSTRUCTOR').all()
    return render_template('listar_instructores.html', instructores=instructores)

@auth_bp.route('/admin/instructor/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('ADMIN')
def detalle_instructor_admin(id):
    instructor = Usuario.query.get_or_404(id)
    
    if request.method == 'POST':
        instructor.nombre = request.form.get('nombre')
        instructor.email = request.form.get('email')
        instructor.telefono = request.form.get('telefono')
        
        bio = request.form.get('bio')
        certificaciones = request.form.get('certificaciones')
        
        if not instructor.instructor:
            nuevo_perfil = Instructor(id=instructor.id, bio=bio, certificaciones=certificaciones)
            db.session.add(nuevo_perfil)
        else:
            instructor.instructor.bio = bio
            instructor.instructor.certificaciones = certificaciones
            
        db.session.commit()
        flash('Perfil del instructor actualizado correctamente.', 'success')
        return redirect(url_for('auth.detalle_instructor_admin', id=id))
        
    clases = Clase.query.filter_by(instructor_id=id).order_by(Clase.fecha_hora.desc()).all()
    return render_template('detalle_instructor_admin.html', instructor=instructor, clases=clases)