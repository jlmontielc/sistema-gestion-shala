
import pymysql
pymysql.install_as_MySQLdb()
import os
from dotenv import load_dotenv

from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()


def create_app():
    load_dotenv()
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['STRIPE_SECRET_KEY'] = os.environ.get('STRIPE_SECRET_KEY')
    app.config['STRIPE_PUBLIC_KEY'] = os.environ.get('STRIPE_PUBLIC_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', 'False') == 'True'

    db.init_app(app)

    @app.route("/")
    def home():
        return redirect(url_for('auth.iniciar_sesion')) 

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

    login_manager = LoginManager()
    login_manager.login_view = 'auth.iniciar_sesion' 
    login_manager.init_app(app)

    from app.models.usuario import Usuario

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    return app