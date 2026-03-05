import pytest
from app.factories.usuario_factory import UsuarioFactory

def test_crear_usuario_yogui():
    usuario = UsuarioFactory.crear_usuario(
        'YOGUI', 
        nombre="Yogui de Prueba", 
        email="yogui@test.com", 
        password_hash="hash_secreto"
    )
    
    assert usuario.rol == 'YOGUI'
    assert usuario.nombre == "Yogui de Prueba"
    assert usuario.email == "yogui@test.com"
    assert usuario.saldo_clases == 0  # El factory debe inicializarlo en 0

def test_crear_usuario_instructor():
    usuario = UsuarioFactory.crear_usuario(
        'INSTRUCTOR', 
        nombre="Profe de Yoga", 
        email="profe@test.com", 
        password_hash="hash_secreto"
    )
    
    assert usuario.rol == 'INSTRUCTOR'


def test_crear_usuario_rol_invalido():
    with pytest.raises(ValueError) as excinfo:
        UsuarioFactory.crear_usuario('ROL_FALSO', nombre="Fake", email="f@test.com", password_hash="123")
    
    assert "Rol inválido para creación" in str(excinfo.value)