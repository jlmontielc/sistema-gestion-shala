import pytest
from datetime import datetime
from app.models.reserva import Reserva
from app.models.usuario import Usuario
from app.models.clase import Clase
from app.models.shala import Shala

def test_crear_reserva(db_session):
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
        titulo="Clase Test",
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

    assert reserva.id is not None
    assert reserva.estado == "RESERVADO"

def test_cancelar_reserva(db_session):
    # Similar a crear, luego cambiar estado a CANCELADO
    pass  # Se puede implementar después