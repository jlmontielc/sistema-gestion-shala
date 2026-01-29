import pymysql
pymysql.install_as_MySQLdb()
import os

from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'ingsw25-26'
    app.config['STRIPE_SECRET_KEY'] = 'sk_test_51SsJBOLcnrKrJeA63aAbKy7BRvZobSApPItz5Wz4TunsF6bhaQbOKwqLJ99KUhdLTAjwsMKjxRAwaZPlC1kJV5fL00Au3aMmkf'
    app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51SsJBOLcnrKrJeA6pIdtW8IgrF2SoZ7DyvCCzyDUF2e2QfXh5JQZ8ZeNNSF7RA9lOUt1VF3wG0X7rxeuJnPoBmG700cOnxIVQo'
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        'mysql://root:WPfIdZtSOMtimSnSDNhKnKImtkpgZuSi@turntable.proxy.rlwy.net:56208/railway'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    @app.route("/")
    def home():
        return redirect(url_for('auth.iniciar_sesion'))  # ✅ Español

    # Registrar blueprints
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)
 
    from app.routes.clases import clases_bp
    app.register_blueprint(clases_bp)
    
    from app.routes.reservas import reservas_bp
    app.register_blueprint(reservas_bp)

    from app.routes.asistencia import asistencia_bp
    app.register_blueprint(asistencia_bp)

    from app.routes.paquetes import paquetes_bp
    app.register_blueprint(paquetes_bp)
    
    from app.routes.pagos import pagos_bp
    app.register_blueprint(pagos_bp)

    from app.routes.analisis import analisis_bp
    app.register_blueprint(analisis_bp)

    from app.routes.shalas import shalas_bp
    app.register_blueprint(shalas_bp)

    # ✅ CORREGIDO: Español
    login_manager = LoginManager()
    login_manager.login_view = 'auth.iniciar_sesion'  # ✅ Español
    login_manager.init_app(app)

    from app.models.usuario import Usuario

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    return app