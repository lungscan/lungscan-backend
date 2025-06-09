from flask import Flask
from flask_cors import CORS

from src.config import DevelopmentConfig, ProductionConfig
from src.api.v1.endpoints import api_v1

def create_app(config_name="development"):
    """
    Creates and configures the Flask application.
    """
    app = Flask(__name__)

    if config_name == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": app.config.get("CORS_ORIGINS", "*")}})

    # Register blueprints
    app.register_blueprint(api_v1, url_prefix="/api/v1")

    @app.route("/")
    def index():
        return {
            "message": "Lung Scan API",
            "version": "1.0.0",
            "endpoints": {
                "analyze": "/api/v1/analyze",
                "pathologies": "/api/v1/pathologies",
                "health": "/api/v1/health",
                "random_image": "/api/v1/random-image",
            },
        }

    return app