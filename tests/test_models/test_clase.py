import pytest
from datetime import datetime, timedelta
from app.models.clase import Clase
from app.models.shala import Shala
from app.models.usuario import Usuario
from app.models.reserva import Reserva

def test_crear_clase(db_session):
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
        titulo="Prueba de clase 1",
        fecha_hora=datetime.now() + timedelta(days=1),
        duracion_min=60,
        capacidad=15,
        modalidad="PRESENCIAL"
    )
    db_session.add(clase)
    db_session.commit()

    assert clase.id is not None
    assert clase.titulo == "Prueba de clase 1"

def test_relacion_reservas(db_session):
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
    yogui = Usuario(
        nombre="Yogui",
        email="yogui@test.com",
        password_hash="hash",
        rol="YOGUI"
    )
    db_session.add(yogui)
    db_session.commit()

    clase = Clase(
        shala_id=shala.id,
        instructor_id=instructor.id,
        titulo="Prueba de clase 2",
        capacidad=10
    )
    db_session.add(clase)
    db_session.commit()

    reserva = Reserva(
        clase_id=clase.id,
        yogui_id=yogui.id,
        estado="RESERVADO"
    )
    db_session.add(reserva)
    db_session.commit()

    assert len(clase.reservas) == 1
    assert clase.reservas[0].yogui_id == yogui.id