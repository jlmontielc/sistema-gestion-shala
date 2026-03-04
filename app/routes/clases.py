# app/routes/clases.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from app.models.usuario import Usuario, Instructor
from app.models.clase import Clase
from app.models.shala import Shala
from app.routes.decoradores import role_required

clases_bp = Blueprint('clases', __name__, url_prefix='/clases')

@clases_bp.route('/crear', methods=['GET', 'POST'])
@login_required
@role_required('ADMIN', 'ADMIN_SHALA', 'INSTRUCTOR')
def crear_clase():
    instructores_query = Usuario.query.filter_by(rol='INSTRUCTOR').join(Usuario.instructor)
    if current_user.rol == 'ADMIN_SHALA' and current_user.shala_id:
        instructores_query = instructores_query.filter(Instructor.shala_id == current_user.shala_id)
    instructores_disponibles = instructores_query.all()

    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descripcion = request.form.get('descripcion')
        fecha_str = request.form.get('fecha_hora') 
        duracion = request.form.get('duracion')
        capacidad = request.form.get('capacidad')
        modalidad = request.form.get('modalidad')
        link = request.form.get('room_link')
        shala_id = request.form.get('shala_id') 
        
        # 👇 NUEVO: Capturamos el instructor que el Admin eligió en el formulario
        instructor_id = request.form.get('instructor_id')

        instructor = Usuario.query.filter_by(id=int(instructor_id), rol='INSTRUCTOR').first() if instructor_id else None
        if not instructor or not instructor.instructor:
            flash('Debes seleccionar un instructor válido.', 'error')
            return render_template('crear_clase.html', shalas=Shala.query.all(), instructores=instructores_disponibles)

        if current_user.rol == 'ADMIN_SHALA' and current_user.shala_id != int(shala_id):
            flash('Solo puedes crear clases en tu propia shala.', 'error')
            return render_template('crear_clase.html', shalas=Shala.query.filter_by(id=current_user.shala_id).all(), instructores=instructores_disponibles)
        
        if instructor.instructor.shala_id != int(shala_id):
            flash('El instructor seleccionado no pertenece al shala elegido.', 'error')
            return render_template('crear_clase.html', shalas=Shala.query.all(), instructores=instructores_disponibles) 
        
        fecha_hora = datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M')

        nueva_clase = Clase(
            titulo=titulo,
            descripcion=descripcion,
            fecha_hora=fecha_hora,
            duracion_min=int(duracion),
            capacidad=int(capacidad),
            modalidad=modalidad,
            room_link=link,
            # 👇 NUEVO: Guardamos al instructor elegido, NO al usuario actual
            instructor_id=int(instructor_id),
            shala_id=int(shala_id)
        )

        db.session.add(nueva_clase)
        db.session.commit()

        return "¡Clase creada exitosamente! <a href='/panel'>Volver</a>"

    # Buscamos las sedes y TODOS los instructores para mostrarlos en el formulario
    if current_user.rol == 'ADMIN_SHALA' and current_user.shala_id:
        todas_las_shalas = Shala.query.filter_by(id=current_user.shala_id).all()
    else:
        todas_las_shalas = Shala.query.all()
    todos_los_instructores = instructores_disponibles
    
    return render_template('crear_clase.html', shalas=todas_las_shalas, instructores=todos_los_instructores)


@clases_bp.route('/listar')
@login_required
def listar_clases():
    clases_db = Clase.query.order_by(Clase.fecha_hora.asc()).all()
    from app.models.usuario import Usuario
    
    # Preparamos los datos ordenados para mandarlos a la plantilla
    clases_data = []
    for c in clases_db:
        instructor = Usuario.query.get(c.instructor_id)
        nombre_profe = instructor.nombre if instructor else "Por definir"
        clases_data.append({
            'id': c.id,
            'titulo': c.titulo,
            'instructor_id': c.instructor_id,
            'nombre_profe': nombre_profe,
            'fecha_hora': c.fecha_hora,
            'duracion_min': c.duracion_min,
            'modalidad': c.modalidad
        })
        
    return render_template('listar_clases.html', clases=clases_data)