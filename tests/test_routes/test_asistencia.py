import pytest
from app.models.usuario import Usuario
from app.models.shala import Shala
from app.models.clase import Clase
from app.models.reserva import Reserva
from app.models.asistencia import Asistencia
from werkzeug.security import generate_password_hash

@pytest.fixture
def instructor_user(db_session):
    user = Usuario(
        nombre="Inst",
        email="inst@test.com",
        password_hash=generate_password_hash("inst"),
        rol="INSTRUCTOR"
    )
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def clase_con_reservas(db_session, instructor_user):
    shala = Shala(nombre="Shala", direccion="Dir")
    db_session.add(shala)
    db_session.commit()
    clase = Clase(
        shala_id=shala.id,
        instructor_id=instructor_user.id,
        titulo="Clase asistencia",
        capacidad=2
    )
    db_session.add(clase)
    db_session.commit()
    # Crear yoguis y reservas
    yogui1 = Usuario(nombre="Y1", email="y1@test.com", password_hash="h", rol="YOGUI")
    yogui2 = Usuario(nombre="Y2", email="y2@test.com", password_hash="h", rol="YOGUI")
    db_session.add_all([yogui1, yogui2])
    db_session.commit()
    reserva1 = Reserva(clase_id=clase.id, yogui_id=yogui1.id, estado="RESERVADO")
    reserva2 = Reserva(clase_id=clase.id, yogui_id=yogui2.id, estado="RESERVADO")
    db_session.add_all([reserva1, reserva2])
    db_session.commit()
    return clase

def test_tomar_asistencia_como_instructor(client, instructor_user, clase_con_reservas):
    client.post('/iniciar-sesion', data={'email': 'inst@test.com', 'password': 'inst'})
    response = client.get(f'/asistencia/tomar/{clase_con_reservas.id}')
    assert response.status_code == 200
    assert b'Tomar Asistencia' in response.data

    # POST con asistencia
    reservas = Reserva.query.filter_by(clase_id=clase_con_reservas.id).all()
    data = {}
    for r in reservas:
        data[f'asistencia_{r.id}'] = 'on'  # marcamos a todos como asistieron
        data[f'comentario_{r.id}'] = 'Bien'
    response = client.post(f'/asistencia/tomar/{clase_con_reservas.id}', data=data, follow_redirects=True)
    assert b'Asistencia Guardada' in response.data

def test_mis_notas_como_yogui(client, db_session):
    # Crear yogui y algunas asistencias
    # ...
    pass