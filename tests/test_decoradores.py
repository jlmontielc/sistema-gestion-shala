import pytest
from flask import Flask
from flask_login import LoginManager, login_user
from app.routes.decoradores import role_required
from app.models.usuario import Usuario

@pytest.fixture
def test_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test'
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    @app.route('/test-admin')
    @role_required('ADMIN')
    def test_admin():
        return 'OK'

    @app.route('/test-admin-shala')
    @role_required('ADMIN_SHALA')
    def test_admin_shala():
        return 'OK'

    return app

def test_role_required_admin_con_permiso(test_app, client, db_session):
    # Crear usuario admin
    admin = Usuario(
        nombre="Admin",
        email="a@test.com",
        password_hash="hash",
        rol="ADMIN"
    )
    db_session.add(admin)
    db_session.commit()

    with test_app.test_request_context():
        login_user(admin)
        response = client.get('/test-admin')
        assert response.status_code == 200
        assert response.data == b'OK'

def test_role_required_admin_sin_permiso(test_app, client, db_session):
    yogui = Usuario(
        nombre="Yogui",
        email="y@test.com",
        password_hash="hash",
        rol="YOGUI"
    )
    db_session.add(yogui)
    db_session.commit()

    with test_app.test_request_context():
        login_user(yogui)
        response = client.get('/test-admin')
        assert response.status_code == 302  # Redirige a panel