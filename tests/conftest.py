import os

import pytest
from werkzeug.security import generate_password_hash

from app import create_app, db
from app.models.usuario import Usuario


@pytest.fixture
def app():
    os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    os.environ['SECRET_KEY'] = 'test_secret'

    flask_app = create_app()
    flask_app.config.update({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
    })

    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def db_session(app):
    yield db.session
    db.session.rollback()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def init_database(app):
    usuario_admin = Usuario(
        nombre='Admin Global',
        email='admin@studiozen.com',
        password_hash=generate_password_hash('admin123'),
        rol='ADMIN',
    )
    db.session.add(usuario_admin)
    db.session.commit()
    return db
