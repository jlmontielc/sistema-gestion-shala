import pytest
from app.models.usuario import Usuario
from app.models.shala import Shala
from app.models.clase import Clase
from app.models.reserva import Reserva
from werkzeug.security import generate_password_hash

@pytest.fixture
def yogui_user(db_session):
    user = Usuario(
        nombre="Yogui",
        email="yogui@test.com",
        password_hash=generate_password_hash("yogui"),
        rol="YOGUI",
        saldo_clases=5
    )
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def clase_con_cupo(db_session):
    shala = Shala(nombre="Shala", direccion="Dir")
    db_session.add(shala)
    db_session.commit()
    instructor = Usuario(
        nombre="Inst",
        email="inst@test.com",
        password_hash="hash",
        rol="INSTRUCTOR"
    )
    db_session.add(instructor)
    db_session.commit()
    clase = Clase(
        shala_id=shala.id,
        instructor_id=instructor.id,
        titulo="Clase con cupo",
        capacidad=2,
        fecha_hora=datetime.now() + timedelta(days=1)
    )
    db_session.add(clase)
    db_session.commit()
    return clase

def test_reservar_clase_con_saldo(client, yogui_user, clase_con_cupo):
    # Login
    client.post('/iniciar-sesion', data={'email': 'yogui@test.com', 'password': 'yogui'})
    # Reservar
    response = client.get(f'/reservas/crear/{clase_con_cupo.id}', follow_redirects=True)
    assert response.status_code == 200
    assert b'Reserva Confirmada' in response.data
    # Verificar saldo actualizado
    with client.application.app_context():
        yogui = Usuario.query.get(yogui_user.id)
        assert yogui.saldo_clases == 4  # Se restó 1

def test_reservar_clase_sin_saldo(client, yogui_user, clase_con_cupo):
    # Poner saldo en 0
    yogui_user.saldo_clases = 0
    db_session.commit()
    client.post('/iniciar-sesion', data={'email': 'yogui@test.com', 'password': 'yogui'})
    response = client.get(f'/reservas/crear/{clase_con_cupo.id}', follow_redirects=True)
    assert b'Saldo Insuficiente' in response.data

def test_cancelar_reserva(client, yogui_user, clase_con_cupo):
    # Primero crear reserva
    client.post('/iniciar-sesion', data={'email': 'yogui@test.com', 'password': 'yogui'})
    client.get(f'/reservas/crear/{clase_con_cupo.id}')
    # Luego cancelar
    reserva = Reserva.query.filter_by(yogui_id=yogui_user.id).first()
    response = client.get(f'/reservas/cancelar/{reserva.id}', follow_redirects=True)
    assert b'Reserva Cancelada' in response.data
    assert b'devuelto 1 clase' in response.data