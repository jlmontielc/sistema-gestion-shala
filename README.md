# StudioZen - Sistema de Gestión de Shalas / Centros de Yoga

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)
![Vercel](https://img.shields.io/badge/Vercel-Deploy-black.svg)

**StudioZen** es una plataforma web integral para la administración de centros de yoga (shalas). Permite gestionar clases, instructores, alumnos, reservas, pagos y asistencia, con un sistema de roles claro: Administrador Global, Administrador de Shala, Instructor y Alumno (Yogui).

## Características principales

- **Autenticación y roles**: Registro e inicio de sesión con roles diferenciados.
- **Gestión de shalas**: CRUD de centros de yoga, con asignación de administradores por shala.
- **Gestión de clases**: Creación, edición y cancelación de clases (con validación de instructor por shala).
- **Reservas**: Reserva de clases con saldo, cancelación con reembolso y notificaciones automáticas.
- **Pagos**: Integración con Stripe para compra de paquetes de clases y pago de clases individuales.
- **Asistencia**: Toma de asistencia con comentarios para los alumnos; visualización de progreso mensual.
- **Notificaciones**: Sistema de notificaciones para alumnos (confirmaciones, cancelaciones, recordatorios).
- **Perfiles**: Edición de perfil personal; para instructores, datos profesionales (bio, certificaciones).
- **Panel de análisis**: Estadísticas globales y por shala (usuarios, clases, reservas, ingresos) con exportación a CSV.
- **Diseño responsivo**: Interfaz moderna y amigable gracias a Bootstrap 5.

## Tecnologías utilizadas

- **Backend**: Python 3.9+, Flask, Flask-Login, Flask-SQLAlchemy
- **Base de datos**: MySQL (con PyMySQL)
- **Frontend**: HTML, CSS, Bootstrap 5, Bootstrap Icons, Jinja2
- **Pagos**: Stripe API
- **Despliegue**: Vercel (serverless functions), Aiven (base de datos)
- **Control de versiones**: Git, GitHub

## Requisitos previos

- Python 3.9 o superior
- MySQL (local o en la nube, por ejemplo Aiven)
- Cuenta en Stripe (para pagos)
- (Opcional) Cuenta en Vercel para despliegue

## Instalación y configuración local

Sigue estos pasos para ejecutar el proyecto en tu máquina local:

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/studiozen.git
   cd studiozen

2. **Crear y activar un entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido (ajusta los valores):
   ```env
   SECRET_KEY=tu_clave_secreta
   STRIPE_SECRET_KEY=sk_test_...
   STRIPE_PUBLIC_KEY=pk_test_...
   SQLALCHEMY_DATABASE_URI=mysql+pymysql://usuario:contraseña@host:puerto/base_datos
   ```
   > **Nota**: Si usas MySQL local, la URI puede ser `mysql+pymysql://root:password@localhost:3306/studiozen`.

5. **Crear la base de datos**
   Conéctate a MySQL y ejecuta:
   ```sql
   CREATE DATABASE studiozen CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
   Luego, desde Python:
   ```bash
   flask shell
   >>> from app import db
   >>> db.create_all()
   >>> exit()
   ```

6. **Ejecutar la aplicación**
   ```bash
   python run.py
   ```
   La aplicación estará disponible en `http://localhost:5000`.

## ☁️ Despliegue en Vercel

El proyecto está configurado para desplegarse fácilmente en Vercel.

1. **Instalar la CLI de Vercel** (opcional, para pruebas locales):
   ```bash
   npm i -g vercel
   ```

2. **Asegurar la estructura de archivos**:
   - `wsgi.py` en la raíz (punto de entrada para Vercel):
     ```python
     import sys
     import traceback
     from app import create_app

     try:
     app = create_app()
     except Exception as e:
     print("Error al crear la aplicación:", file=sys.stderr)
     traceback.print_exc(file=sys.stderr)
     raise e  # Esto hará que Vercel registre el error
     ```
     
   - `vercel.json` en la raíz:
     ```json
     {
      "builds": [
      {
        "src": "wsgi.py",
        "use": "@vercel/python"
      }
      ],
      "routes": [
       {
         "src": "/(.*)",
         "dest": "wsgi.py"
        }
       ]
     }
     ```

3. **Configurar variables de entorno en Vercel**:
   En el panel de Vercel, ve a tu proyecto → Settings → Environment Variables y agrega las mismas variables que en `.env` (sin comillas).

4. **Desplegar**:
   Conecta tu repositorio a Vercel y cada push a la rama principal generará un nuevo despliegue automático.

## Estructura del proyecto

```
studiozen/
├── app/
│   ├── models/              # Modelos de base de datos
│   ├── routes/               # Controladores (auth, clases, shalas, etc.)
│   ├── templates/            # Plantillas HTML (Jinja2)
│   ├── static/               # Archivos estáticos (imagen favicon)
│   ├── factories/            # Fábrica de usuarios (Factory Method)
│   └── __init__.py           # Inicialización de la aplicación Flask
├── tests/                    # Carpeta de pruebas
|   ├── test_integration/     # Pruebas de integración (flujos completos)
|   ├── test_models/          # Pruebas de modelos (base de datos)
|   ├── test_routes/          # Pruebas de rutas (controladores)
|   ├── conftest.py           # Configuración y fixtures globales
├── run.py                    # Punto de entrada para desarrollo local
├── wsgi.py                   # Punto de entrada para Vercel
├── vercel.json               # Configuración de despliegue en Vercel
├── requirements.txt          # Dependencias Python
├── pytest.ini                # Configuración de pytest
├── .env                      # Variables de entorno (no subir a git)
└── README.md                 # Este archivo
```

## Roles de usuario

- **Administrador Global (ADMIN)**: Acceso completo a todas las funcionalidades, gestión de shalas, instructores y alumnos.
- **Administrador de Shala (ADMIN_SHALA)**: Administra una única shala (clases, instructores, alumnos, estadísticas).
- **Instructor (INSTRUCTOR)**: Crea clases, toma asistencia y añade comentarios a los alumnos.
- **Alumno (YOGUI)**: Reserva clases, compra paquetes, ve su progreso y recibe notificaciones.

## Funcionalidades clave

### Para el alumno (Yogui)
- Visualizar clases disponibles y reservar (con saldo o pago individual).
- Ver historial de reservas y cancelarlas (reembolso de saldo).
- Consultar notificaciones y marcarlas como leídas.
- Ver progreso mensual (asistencias/faltas) y comentarios de instructores.
- Comprar paquetes de clases mediante Stripe.
- Editar perfil personal.

### Para el instructor
- Crear y programar clases (asignando shala e instructor).
- Tomar asistencia de las clases, añadiendo comentarios por alumno.
- Ver calendario de sus clases.

### Para el administrador de shala
- Gestionar instructores (asignarlos a su shala).
- Gestionar alumnos (ver historial, editar saldo).
- Crear y editar paquetes de clases.
- Ver panel de análisis filtrado por su shala.

### Para el administrador global
- Crear shalas y asignar administradores de shala.
- Gestionar todos los instructores y alumnos.
- Ver análisis global de todo el sistema.

## Licencia

Este proyecto es desarrollado con fines académicos para la asignatura Ingeniería de Software de la Universidad del Zulia (LUZ). Queda prohibido su uso comercial sin autorización expresa de los autores.

## Autores

- **Jorge Montiel** - [@jlmontielc](https://github.com/jlmontielc)
- **Yainder Muñoz** - [@yainderm](https://github.com/yainderm)

## Agradecimientos

- Prof. Yaskelly Yedra, por la guía en el desarrollo del proyecto.
