import pytest
from app.models.usuario import Usuario
from werkzeug.security import generate_password_hash

@pytest.fixture
def admin_user(db_session):
    user = Usuario(
        nombre="Admin",
        email="admin@test.com",
        password_hash=generate_password_hash("admin"),
        rol="ADMIN"
    )
    db_session.add(user)
    db_session.commit()
    return user

def test_dashboard_analisis_como_admin(client, admin_user):
    client.post('/iniciar-sesion', data={'email': 'admin@test.com', 'password': 'admin'})
    response = client.get('/analisis/')
    assert response.status_code == 200
    assert b'Panel de An' in response.data  # 'Panel de Análisis'