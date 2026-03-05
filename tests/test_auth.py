import pytest
from app.models.usuario import Usuario

def test_iniciar_sesion_exitoso(client, init_database):
    """Prueba que un usuario existente pueda iniciar sesión."""
    # Hacemos un POST a la ruta de login con el usuario que creamos en el fixture init_database
    response = client.post('/iniciar-sesion', data={
        'email': 'admin@studiozen.com',
        'password': 'admin123'
    }, follow_redirects=True)
    
    # Comprobamos que la respuesta HTTP sea correcta y que haya un mensaje de éxito
    assert response.status_code == 200
    assert b'Bienvenido/a Admin Global' in response.data

def test_iniciar_sesion_fallido(client, init_database):
    """Prueba el inicio de sesión con contraseña incorrecta."""
    response = client.post('/iniciar-sesion', data={
        'email': 'admin@studiozen.com',
        'password': 'clave_equivocada'
    }, follow_redirects=True)
    
    assert b'Credenciales incorrectas' in response.data

def test_registro_nuevo_yogui(client, app):
    """Prueba que un nuevo alumno (Yogui) se pueda registrar correctamente."""
    with app.app_context():
        # Antes de la petición, no debe existir el usuario
        assert Usuario.query.filter_by(email='nuevo@test.com').first() is None

    response = client.post('/registro', data={
        'nombre': 'Nuevo Yogui',
        'email': 'nuevo@test.com',
        'password': 'password123',
        'rol': 'YOGUI'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Registro exitoso' in response.data

    with app.app_context():
        # Después de la petición, el usuario debe existir en la BD
        nuevo_user = Usuario.query.filter_by(email='nuevo@test.com').first()
        assert nuevo_user is not None
        assert nuevo_user.rol == 'YOGUI'