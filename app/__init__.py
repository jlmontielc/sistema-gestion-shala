import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask, app, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'ingsw25-26'

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        'mysql://root:WPfIdZtSOMtimSnSDNhKnKImtkpgZuSi@turntable.proxy.rlwy.net:56208/railway'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from flask import redirect, url_for

    @app.route("/")
    def home():
        return redirect(url_for('auth.register'))

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from app.models.usuario import Usuario

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    return app
