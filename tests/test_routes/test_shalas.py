import pytest
from werkzeug.security import generate_password_hash

from app.models.shala import Shala
from app.models.usuario import Usuario


@pytest.fixture
def admin_user(db_session):
    user = Usuario(
        nombre='Admin',
        email='admin@test.com',
        password_hash=generate_password_hash('admin'),
        rol='ADMIN',
    )
    db_session.add(user)
    db_session.commit()
    return user


def test_crear_shala_como_admin(client, admin_user):
    client.post('/iniciar-sesion', data={'email': 'admin@test.com', 'password': 'admin'})
    response = client.post(
        '/shalas/crear',
        data={'nombre': 'Shala Nueva', 'direccion': 'Calle 456', 'telefono': '987654321'},
        follow_redirects=True,
    )

    assert response.status_code == 200
    creada = Shala.query.filter_by(nombre='Shala Nueva').first()
    assert creada is not None


def test_listar_shalas(client, db_session, admin_user):
    shala = Shala(nombre='Shala Existente', direccion='Dir')
    db_session.add(shala)
    db_session.commit()

    client.post('/iniciar-sesion', data={'email': 'admin@test.com', 'password': 'admin'})
    response = client.get('/shalas/listar')

    assert response.status_code == 200
    assert b'Shala Existente' in response.data
