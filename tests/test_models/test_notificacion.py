import pytest
from app.models.notificacion import Notificacion
from app.models.usuario import Usuario

def test_crear_notificacion(db_session):
    yogui = Usuario(
        nombre="Yogui",
        email="y@test.com",
        password_hash="hash",
        rol="YOGUI"
    )
    db_session.add(yogui)
    db_session.commit()

    notif = Notificacion(
        yogui_id=yogui.id,
        titulo="Reserva confirmada",
        mensaje="Tu clase ha sido confirmada."
    )
    db_session.add(notif)
    db_session.commit()

    assert notif.id is not None
    assert notif.leida is False

def test_marcar_como_leida(db_session):
    yogui = Usuario(
        nombre="Yogui",
        email="y@test.com",
        password_hash="hash",
        rol="YOGUI"
    )
    db_session.add(yogui)
    db_session.commit()

    notif = Notificacion(
        yogui_id=yogui.id,
        titulo="Test",
        mensaje="Mensaje"
    )
    db_session.add(notif)
    db_session.commit()

    notif.leida = True
    db_session.commit()
    assert notif.leida is True