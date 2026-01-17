from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash

from app import db
from app.models.usuario import Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')
        rol = request.form.get('rol')

        # Validación mínima
        if not nombre or not email or not password or not rol:
            return "Datos incompletos", 400

        password_hash = generate_password_hash(password)

        usuario = Usuario(
            nombre=nombre,
            email=email,
            password_hash=password_hash,
            rol=rol
        )

        db.session.add(usuario)
        db.session.commit()

        return redirect(url_for('auth.register'))

    return render_template('register.html')

from flask_login import login_user
from werkzeug.security import check_password_hash

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and check_password_hash(usuario.password_hash, password):
            login_user(usuario)
            return "Login exitoso"

        return "Credenciales incorrectas", 401

    return render_template('login.html')

from flask_login import login_required

@auth_bp.route('/dashboard')
@login_required
def dashboard():
    return "Dashboard general"

from flask_login import login_required
from app.routes.decorators import role_required

@auth_bp.route('/admin')
@login_required
@role_required('ADMIN')
def admin_panel():
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
