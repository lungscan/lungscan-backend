from flask import Flask
from flask_cors import CORS

from src.config import DevelopmentConfig, ProductionConfig
from src.api.v1.endpoints import api_v1
from src.extensions import limiter

from src.model.lung_analyzer import LungAnalyzer

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

    # Initialize extensions
    limiter.init_app(app)

    # Initialize lung analyzer model
    initialize_model(app)

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

def initialize_model(app: Flask) -> None:
    """
    Initialize the lung analyzer model and attach it to the app.

    Args:
        app: Flask application instance
    """
    try:
        app.logger.info("Loading lung analyzer model...")
        model_name = app.config.get('MODEL_NAME', 'densenet121-res224-all')
        app.lung_analyzer = LungAnalyzer(model_name=model_name)
        app.logger.info("Lung analyzer model loaded successfully")

    except Exception as e:
        app.logger.error(f"Failed to load lung analyzer model: {str(e)}")
        raise RuntimeError(f"Model initialization failed: {str(e)}")