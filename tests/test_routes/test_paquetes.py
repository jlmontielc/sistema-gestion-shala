import pytest
from app.models.paquete import Paquete

def test_listar_paquetes(client, db_session):
    paquete = Paquete(nombre="Pack 10", precio=100, sesiones_incluidas=10)
    db_session.add(paquete)
    db_session.commit()
    response = client.get('/paquetes/listar')
    assert response.status_code == 200
    assert b'Pack 10' in response.data