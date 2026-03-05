import pytest
import os
from app import create_app, db
from app.models.usuario import Usuario
from werkzeug.security import generate_password_hash

@pytest.fixture
def app():
    # Usamos una base de datos temporal en memoria para no afectar tu BD real
    os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    os.environ['SECRET_KEY'] = 'test_secret'
    
    app = create_app()
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False # Desactiva CSRF si usaras Flask-WTF
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Un cliente de pruebas para simular peticiones HTTP (GET, POST)."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Un runner para comandos de CLI de Flask."""
    return app.test_cli_runner()

@pytest.fixture
def init_database(app):
    """Crea datos iniciales en la base de datos de prueba."""
    usuario_admin = Usuario(
        nombre="Admin Global",
        email="admin@studiozen.com",
        password_hash=generate_password_hash("admin123"),
        rol="ADMIN"
    )
    db.session.add(usuario_admin)
    db.session.commit()
    return db