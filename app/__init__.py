from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import DevelopmentConfig
from flask_bootstrap import Bootstrap5

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    bootstrap = Bootstrap5(app)
    db.init_app(app)

    with app.app_context():
        # Importar y registrar las rutas
        from .routes.loan_routes import loan_bp
        from .routes.config_routes import config_bp

        app.register_blueprint(loan_bp)
        app.register_blueprint(config_bp)

    return app
