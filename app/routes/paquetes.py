from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.paquete import Paquete
from app.routes.decoradores import role_required

paquetes_bp = Blueprint('paquetes', __name__, url_prefix='/paquetes')

@paquetes_bp.route('/crear', methods=['GET', 'POST'])
@login_required
@role_required('ADMIN', 'ADMIN_SHALA')
def crear_paquete():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        precio = request.form.get('precio')
        sesiones = request.form.get('sesiones_incluidas')

        # Creamos el paquete SIN el shala_id (quedará como global)
        nuevo_paquete = Paquete(
            nombre=nombre,
            descripcion=descripcion,
            precio=float(precio),
            sesiones_incluidas=int(sesiones)
        )

        db.session.add(nuevo_paquete)
        db.session.commit()

        flash("¡Paquete global creado exitosamente!", "success")
        return redirect(url_for('auth.panel'))

    return render_template('crear_paquete.html')

@paquetes_bp.route('/listar')
@login_required
def listar_paquetes():
    # Esta vista servirá para que el Shala vea qué vende
    # Y luego la usaremos para que el Yogui vea qué comprar
    todos_paquetes = Paquete.query.all()
    return render_template('paquetes.html', paquetes=todos_paquetes)

@paquetes_bp.route('/comprar/<int:id>')
@login_required
@role_required('YOGUI')
def comprar_paquete(id):
    # 1. Buscamos qué paquete quiere comprar
    paquete = Paquete.query.get_or_404(id)
    
    # 2. Le sumamos las clases a su saldo
    current_user.saldo_clases += paquete.sesiones_incluidas
    
    db.session.commit()
    
    # 3. Mensaje de éxito
    return f"""
    <h1>¡Compra Exitosa! 🎉</h1>
    <p>Has comprado: {paquete.nombre}</p>
    <p>Tu nuevo saldo es: <strong>{current_user.saldo_clases} clases</strong>.</p>
    <a href='/panel'>Volver al Panel</a>
    """