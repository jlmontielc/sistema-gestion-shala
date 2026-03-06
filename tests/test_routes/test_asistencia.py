from datetime import datetime, timedelta

import pytest
from werkzeug.security import generate_password_hash

from app.models.asistencia import Asistencia
from app.models.clase import Clase
from app.models.reserva import Reserva
from app.models.shala import Shala
from app.models.usuario import Instructor, Usuario


@pytest.fixture
def instructor_user(db_session):
    shala = Shala(nombre='Shala Inst', direccion='Dir')
    db_session.add(shala)
    db_session.commit()

    user = Usuario(
        nombre='Inst',
        email='inst@test.com',
        password_hash=generate_password_hash('inst'),
        rol='INSTRUCTOR',
    )
    db_session.add(user)
    db_session.commit()

    perfil = Instructor(id=user.id, shala_id=shala.id, bio='bio')
    db_session.add(perfil)
    db_session.commit()
    return user


@pytest.fixture
def clase_con_reservas(db_session, instructor_user):
    clase = Clase(
        shala_id=instructor_user.instructor.shala_id,
        instructor_id=instructor_user.id,
        titulo='Clase asistencia',
        capacidad=2,
        fecha_hora=datetime.now() + timedelta(days=1),
        modalidad='PRESENCIAL',
    )
    db_session.add(clase)
    db_session.commit()

    yogui1 = Usuario(nombre='Y1', email='y1@test.com', password_hash='h', rol='YOGUI')
    yogui2 = Usuario(nombre='Y2', email='y2@test.com', password_hash='h', rol='YOGUI')
    db_session.add_all([yogui1, yogui2])
    db_session.commit()

    reserva1 = Reserva(clase_id=clase.id, yogui_id=yogui1.id, estado='RESERVADO')
    reserva2 = Reserva(clase_id=clase.id, yogui_id=yogui2.id, estado='RESERVADO')
    db_session.add_all([reserva1, reserva2])
    db_session.commit()
    return clase


def test_tomar_asistencia_como_instructor(client, instructor_user, clase_con_reservas):
    client.post('/iniciar-sesion', data={'email': 'inst@test.com', 'password': 'inst'})
    response = client.get(f'/asistencia/tomar/{clase_con_reservas.id}')
    assert response.status_code == 200
    assert b'Tomar Asistencia' in response.data

    reservas = Reserva.query.filter_by(clase_id=clase_con_reservas.id).all()
    data = {}
    for reserva in reservas:
        data[f'asistencia_{reserva.id}'] = 'on'
        data[f'comentario_{reserva.id}'] = 'Bien'

    response = client.post(
        f'/asistencia/tomar/{clase_con_reservas.id}', data=data, follow_redirects=True
    )
    assert 'Asistencia y notas guardadas'.encode('utf-8') in response.data
    assert Asistencia.query.count() == 2
