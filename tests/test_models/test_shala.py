import pytest
from app.models.shala import Shala
from app.models.usuario import Usuario
from app.models.paquete import Paquete
from app.models.clase import Clase

def test_crear_shala(db_session):
    shala = Shala(
        nombre="Shala Central",
        direccion="Av. Principal 123",
        telefono="123456789"
    )
    db_session.add(shala)
    db_session.commit()
    assert shala.id is not None

def test_relacion_paquetes(db_session):
    shala = Shala(nombre="Shala", direccion="Dir")
    db_session.add(shala)
    db_session.commit()

    paquete = Paquete(
        shala_id=shala.id,
        nombre="Pack 10 clases",
        precio=100.0,
        sesiones_incluidas=10
    )
    db_session.add(paquete)
    db_session.commit()

    assert shala.paquetes[0].nombre == "Pack 10 clases"

def test_relacion_clases(db_session):
    shala = Shala(nombre="Shala", direccion="Dir")
    db_session.add(shala)
    db_session.commit()

    # Necesitamos un instructor (usuario) para la clase
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
        titulo="Prueba de clase",
        capacidad=10
    )
    db_session.add(clase)
    db_session.commit()

    assert shala.clases[0].titulo == "Prueba de clase"