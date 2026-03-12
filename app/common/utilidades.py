def rol_nombre(rol):
    nombres = {
        "ADMIN": "Administrador",
        "ADMIN_SHALA": "Shala",
        "INSTRUCTOR": "Instructor",
        "YOGUI": "Yogui",
    }
    return nombres.get(rol, rol)
