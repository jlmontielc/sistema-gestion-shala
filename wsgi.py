import sys
import traceback
from app import create_app

try:
    app = create_app()
except Exception as e:
    print("Error al crear la aplicación:", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
    raise e  # Esto hará que Vercel registre el error