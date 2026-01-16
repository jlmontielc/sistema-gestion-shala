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
