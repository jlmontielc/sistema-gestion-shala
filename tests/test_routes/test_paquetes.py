from werkzeug.security import generate_password_hash

from app.models.paquete import Paquete
from app.models.usuario import Usuario


def test_listar_paquetes(client, db_session):
    yogui = Usuario(
        nombre='Yogui',
        email='yogui@test.com',
        password_hash=generate_password_hash('yogui'),
        rol='YOGUI',
    )
    paquete = Paquete(nombre='Pack 10', precio=100, sesiones_incluidas=10)

    db_session.add_all([yogui, paquete])
    db_session.commit()

    client.post('/iniciar-sesion', data={'email': 'yogui@test.com', 'password': 'yogui'})
    response = client.get('/paquetes/listar')

    assert response.status_code == 200
    assert b'Pack 10' in response.data
