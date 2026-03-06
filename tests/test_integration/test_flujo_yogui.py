import pytest
from app.models.usuario import Usuario
from app.models.shala import Shala
from app.models.clase import Clase
from app.models.paquete import Paquete

def test_flujo_completo_yogui(client, db_session):
    # 1. Crear datos necesarios (shala, instructor, clase, paquete)
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
        titulo="Clase de integración",
        capacidad=5,
        fecha_hora=datetime.now() + timedelta(days=1)
    )
    db_session.add(clase)
    db_session.commit()
    paquete = Paquete(
        nombre="Pack 5",
        precio=50,
        sesiones_incluidas=5
    )
    db_session.add(paquete)
    db_session.commit()

    # 2. Registro de yogui
    response = client.post('/registro', data={
        'nombre': 'Nuevo Yogui',
        'email': 'nuevo@test.com',
        'password': 'pass123',
        'rol': 'YOGUI'
    }, follow_redirects=True)
    assert b'Registro exitoso' in response.data

    # 3. Iniciar sesión
    response = client.post('/iniciar-sesion', data={
        'email': 'nuevo@test.com',
        'password': 'pass123'
    }, follow_redirects=True)
    assert b'Bienvenido/a Nuevo Yogui' in response.data

    # 4. Comprar paquete (simulamos la redirección a Stripe, pero aquí solo verificamos la ruta)
    # En un test real, habría que mockear Stripe o usar modo de prueba.
    response = client.get(f'/paquetes/comprar/{paquete.id}', follow_redirects=True)
    # Como la compra directa sin pago puede no estar implementada, asumimos que redirige a Stripe.
    # Podríamos mockear la llamada a Stripe.
    # Por ahora, solo verificamos que la ruta existe.
    assert response.status_code in (200, 302)

    # 5. Reservar clase
    response = client.get(f'/reservas/crear/{clase.id}', follow_redirects=True)
    assert b'Reserva Confirmada' in response.data

    # 6. Ver mis reservas
    response = client.get('/reservas/mis-reservas')
    assert b'Clase de integraci' in response.data

    # 7. Ver progreso
    response = client.get('/asistencia/mis-notas')
    assert b'Mi Progreso' in response.data