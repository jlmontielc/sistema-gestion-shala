from datetime import datetime, timedelta

from app.models.clase import Clase
from app.models.paquete import Paquete
from app.models.shala import Shala
from app.models.usuario import Usuario


def test_flujo_completo_yogui(client, db_session):
    shala = Shala(nombre='Shala', direccion='Dir')
    db_session.add(shala)
    db_session.commit()

    instructor = Usuario(
        nombre='Inst',
        email='inst@test.com',
        password_hash='hash',
        rol='INSTRUCTOR',
    )
    db_session.add(instructor)
    db_session.commit()

    clase = Clase(
        shala_id=shala.id,
        instructor_id=instructor.id,
        titulo='Clase de integración',
        capacidad=5,
        fecha_hora=datetime.now() + timedelta(days=1),
    )
    paquete = Paquete(nombre='Pack 5', precio=50, sesiones_incluidas=5)
    db_session.add_all([clase, paquete])
    db_session.commit()

    response = client.post(
        '/registro',
        data={
            'nombre': 'Nuevo Yogui',
            'email': 'nuevo@test.com',
            'password': 'pass123',
            'rol': 'YOGUI',
        },
        follow_redirects=True,
    )
    assert b'Registro exitoso' in response.data

    response = client.post(
        '/iniciar-sesion',
        data={'email': 'nuevo@test.com', 'password': 'pass123'},
        follow_redirects=True,
    )
    assert b'Bienvenido/a Nuevo Yogui' in response.data

    response = client.get(f'/paquetes/comprar/{paquete.id}', follow_redirects=True)
    assert response.status_code == 200
    assert b'Compra Exitosa' in response.data

    response = client.get(f'/reservas/crear/{clase.id}', follow_redirects=True)
    assert b'Reserva Confirmada' in response.data

    response = client.get('/reservas/mis-reservas')
    assert b'Clase de integraci' in response.data

    response = client.get('/asistencia/mis-notas')
    assert b'Mi Progreso' in response.data
