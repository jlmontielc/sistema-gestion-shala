from werkzeug.security import generate_password_hash

from app.models.usuario import Usuario


def test_role_required_admin_con_permiso(client, db_session):
    admin = Usuario(
        nombre='Admin',
        email='a@test.com',
        password_hash=generate_password_hash('admin'),
        rol='ADMIN',
    )
    db_session.add(admin)
    db_session.commit()

    client.post('/iniciar-sesion', data={'email': 'a@test.com', 'password': 'admin'})
    response = client.get('/administracion')

    assert response.status_code == 200
    assert b'Panel de administraci' in response.data


def test_role_required_admin_sin_permiso(client, db_session):
    yogui = Usuario(
        nombre='Yogui',
        email='y@test.com',
        password_hash=generate_password_hash('yogui'),
        rol='YOGUI',
    )
    db_session.add(yogui)
    db_session.commit()

    client.post('/iniciar-sesion', data={'email': 'y@test.com', 'password': 'yogui'})
    response = client.get('/administracion')

    assert response.status_code == 302
