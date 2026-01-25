from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models.usuario import Usuario
from app.routes.decoradores import role_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')
        rol = request.form.get('rol')

        # Validación mínima
        if not nombre or not email or not password or not rol:
            flash("Datos incompletos", "error")
            return redirect(url_for('auth.registro'))

        # Verificar si el email ya existe
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
    return render_template('panel.html', user=current_user)  # ✅ Ya está bien

@auth_bp.route('/administracion')
@login_required
@role_required('ADMIN')
def administracion():
    return render_template('administracion.html')

@auth_bp.route('/gestion-clases')
@login_required
@role_required('ADMIN', 'INSTRUCTOR')
def gestion_clases():
    return render_template('gestion_clases.html')

@auth_bp.route('/mis-reservas')
@login_required
@role_required('YOGUI')
def mis_reservas():
    return render_template('mis_reservas.html')

@auth_bp.route('/cerrar-sesion')
@login_required
def cerrar_sesion():
    logout_user()
    flash("Sesión cerrada correctamente", "info")
    return redirect(url_for('auth.iniciar_sesion'))