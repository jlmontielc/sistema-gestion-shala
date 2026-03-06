import pytest
from app.models.usuario import Usuario
from app.models.shala import Shala
from app.models.clase import Clase
from app.models.instructor import Instructor
from werkzeug.security import generate_password_hash

def login_test_user(client, email, password):
    return client.post('/iniciar-sesion', data={
        'email': email,
        'password': password
    }, follow_redirects=True)

@pytest.fixture
def admin_user(db_session):
    user = Usuario(
        nombre="Admin",
        email="admin@test.com",
        password_hash=generate_password_hash("admin"),
        rol="ADMIN"
    )
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def shala_test(db_session):
    shala = Shala(nombre="Shala Test", direccion="Dir")
    db_session.add(shala)
    db_session.commit()
    return shala

@pytest.fixture
def instructor_user(db_session, shala_test):
    user = Usuario(
        nombre="Instructor",
        email="inst@test.com",
        password_hash=generate_password_hash("inst"),
        rol="INSTRUCTOR"
    )
    db_session.add(user)
    db_session.commit()
    instructor = Instructor(
        id=user.id,
        shala_id=shala_test.id,
        bio="Bio"
    )
    db_session.add(instructor)
    db_session.commit()
    return user

def test_crear_clase_como_admin(client, admin_user, shala_test, instructor_user):
    # Login como admin
    response = login_test_user(client, "admin@test.com", "admin")
    assert response.status_code == 200

    # POST a crear clase
    response = client.post('/clases/crear', data={
        'titulo': 'Clase de prueba',
        'descripcion': 'Descripción',
        'fecha_hora': '2025-12-31T10:00',
        'duracion': 60,
        'capacidad': 10,
        'modalidad': 'PRESENCIAL',
        'shala_id': shala_test.id,
        'instructor_id': instructor_user.id
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Clase creada exitosamente' in response.data

def test_crear_clase_sin_permiso(client, shala_test, instructor_user):
    # Sin login
    response = client.post('/clases/crear', data={
        'titulo': 'Clase sin permiso',
        'fecha_hora': '2025-12-31T10:00',
        'duracion': 60,
        'capacidad': 10,
        'modalidad': 'PRESENCIAL',
        'shala_id': shala_test.id,
        'instructor_id': instructor_user.id
    }, follow_redirects=True)
    # Debe redirigir al login o mostrar error
    assert response.status_code == 200
    assert b'Iniciar sesi' in response.data or b'Por favor, inicia sesi' in response.data

def test_listar_clases(client, db_session):
    # Crear algunas clases en la BD
    # ... (setup)
    response = client.get('/clases/listar')
    assert response.status_code == 200
    assert b'Calendario de Clases' in response.data