import pytest
from werkzeug.security import generate_password_hash

from app.models.usuario import Usuario


@pytest.fixture
def yogui_user(db_session):
    user = Usuario(
        nombre='Yogui',
        email='yogui@test.com',
        password_hash=generate_password_hash('yogui'),
        rol='YOGUI',
    )
    db_session.add(user)
    db_session.commit()
    return user


def test_editar_perfil_yogui(client, yogui_user):
    client.post('/iniciar-sesion', data={'email': 'yogui@test.com', 'password': 'yogui'})
    response = client.post(
        '/perfil',
        data={'nombre': 'Yogui Modificado', 'telefono': '123456'},
        follow_redirects=True,
    )

    assert 'Perfil actualizado con éxito'.encode('utf-8') in response.data
    with client.application.app_context():
        user = Usuario.query.get(yogui_user.id)
        assert user.nombre == 'Yogui Modificado'
        assert user.telefono == '123456'
