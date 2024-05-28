from flask import Flask

def create_app():
    app = Flask(__name__)

    # Registrar blueprints
    from app.api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app