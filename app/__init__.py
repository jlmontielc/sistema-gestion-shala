from flask import Flask

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def home():
        return "Sistema de Gestión de Shalas funcionando"
    
    return app
