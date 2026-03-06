import pytest
from app.models.asistencia import Asistencia
from app.models.reserva import Reserva
from app.models.usuario import Usuario
from app.models.clase import Clase
from app.models.shala import Shala

def test_crear_asistencia(db_session):
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
        email="y@test.com",
        password_hash="hash",
        rol="YOGUI"
    )
    db_session.add(yogui)
    db_session.commit()
    clase = Clase(
        shala_id=shala.id,
        instructor_id=instructor.id,
        titulo="Clase",
        capacidad=5
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

    asistencia = Asistencia(
        reserva_id=reserva.id,
        estado_asistencia="ASISTIO",
        comentario="Muy bien"
    )
    db_session.add(asistencia)
    db_session.commit()

    assert asistencia.id is not None
    assert asistencia.comentario == "Muy bien"