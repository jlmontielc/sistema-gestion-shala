from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict

from app.models.usuario import Usuario


@dataclass(frozen=True)
class DatosCreacionUsuario:
    nombre: str
    email: str
    password_hash: str


class UsuarioFactory:
    """Factory Method para crear usuarios por rol."""

    _creadores: Dict[str, Callable[[DatosCreacionUsuario], Usuario]] = {
        'YOGUI': lambda datos: Usuario(
            nombre=datos.nombre,
            email=datos.email,
            password_hash=datos.password_hash,
            rol='YOGUI',
            saldo_clases=0,
        ),
        'INSTRUCTOR': lambda datos: Usuario(
            nombre=datos.nombre,
            email=datos.email,
            password_hash=datos.password_hash,
            rol='INSTRUCTOR',
        ),
        'ADMIN_SHALA': lambda datos: Usuario(
            nombre=datos.nombre,
            email=datos.email,
            password_hash=datos.password_hash,
            rol='ADMIN_SHALA',
        ),
        'ADMIN': lambda datos: Usuario(
            nombre=datos.nombre,
            email=datos.email,
            password_hash=datos.password_hash,
            rol='ADMIN',
        ),
    }

    @classmethod
    def crear_usuario(
        cls,
        rol: str,
        *,
        nombre: str,
        email: str,
        password_hash: str,
    ) -> Usuario:
        creador = cls._creadores.get(rol)
        if not creador:
            raise ValueError(f"Rol inválido para creación: {rol}")

        return creador(
            DatosCreacionUsuario(
                nombre=nombre,
                email=email,
                password_hash=password_hash,
            )
        )