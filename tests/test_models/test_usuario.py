import pytest
from app.models.usuario import Usuario, Instructor
from app.models.shala import Shala
from app.models.notificacion import Notificacion
from werkzeug.security import generate_password_hash

def test_crear_usuario_yogui(db_session):
    usuario = Usuario(
        nombre="Yogui Test",
        email="yogui@test.com",
        password_hash=generate_password_hash("123"),
        rol="YOGUI",
        saldo_clases=5
    )
    db_session.add(usuario)
    db_session.commit()
    assert usuario.id is not None
    assert usuario.saldo_clases == 5

def test_crear_usuario_instructor_con_shala(db_session):
    shala = Shala(nombre="Shala Test", direccion="Calle 123")
    db_session.add(shala)
    db_session.commit()

    usuario = Usuario(
        nombre="Instructor Test",
        email="inst@test.com",
        password_hash=generate_password_hash("123"),
        rol="INSTRUCTOR"
    )
    db_session.add(usuario)
    db_session.commit()

    instructor = Instructor(
        id=usuario.id,
        shala_id=shala.id,
        bio="Bio de prueba"
    )
    db_session.add(instructor)
    db_session.commit()

    assert usuario.instructor == instructor
    assert instructor.usuario.nombre == "Instructor Test"
    assert instructor.shala.nombre == "Shala Test"

def test_email_unico(db_session):
    usuario1 = Usuario(
        nombre="User1",
        email="duplicado@test.com",
        password_hash="hash",
        rol="YOGUI"
    )
    db_session.add(usuario1)
    db_session.commit()

    usuario2 = Usuario(
        nombre="User2",
        email="duplicado@test.com",
        password_hash="hash",
        rol="YOGUI"
    )
    db_session.add(usuario2)
    with pytest.raises(Exception):  # SQLAlchemy lanzará excepción por unicidad
        db_session.commit()
    db_session.rollback()

def test_relacion_notificaciones(db_session):
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
        mensaje="Mensaje de prueba"
    )
    db_session.add(notif)
    db_session.commit()

    assert len(yogui.notificaciones) == 1
    assert yogui.notificaciones[0].titulo == "Test"