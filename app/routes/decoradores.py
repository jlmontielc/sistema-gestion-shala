from flask_login import current_user
from flask import abort, flash, redirect, url_for
from functools import wraps

def role_required(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Por favor, inicia sesión para acceder a esta página.", "warning")
                return redirect(url_for('auth.iniciar_sesion'))
            if current_user.rol not in roles:
                flash("No tienes permiso para acceder a esta página.", "error")
                return redirect(url_for('auth.panel'))
            return func(*args, **kwargs)
        return wrapper
    return decorator