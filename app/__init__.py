from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        'mysql://root:WPfIdZtSOMtimSnSDNhKnKImtkpgZuSi@turntable.proxy.rlwy.net:56208/railway'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    @app.route("/")
    def home():
        return "Sistema de Gestión de Shalas funcionando"

    return app
