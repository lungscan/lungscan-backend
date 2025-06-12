from flask import Flask, jsonify
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

    # Error handlers
    @app.errorhandler(400)
    def handle_400(error):
        return jsonify({
            "error": "Bad Request",
            "message": error.description if hasattr(error, "description") else "Invalid request"
        }), 400

    @app.errorhandler(401)
    def handle_401(error):
        return jsonify({
            "error": "Unauthorized",
            "message": error.description if hasattr(error, "description") else "Authentication required"
        }), 401

    @app.errorhandler(404)
    def handle_404(error):
        return jsonify({
            "error": "Not Found",
            "message": error.description if hasattr(error, "description") else "The requested resource was not found"
        }), 404

    @app.errorhandler(413)
    def handle_413(error):
        return jsonify({
            "error": "Payload Too Large",
            "message": "The uploaded file is too large"
        }), 413

    @app.errorhandler(415)
    def handle_415(error):
        return jsonify({
            "error": "Unsupported Media Type",
            "message": "The media type of the request is not supported"
        }), 415

    @app.errorhandler(500)
    def handle_500(error):
        return jsonify({
            "error": "Internal Server Error",
            "message": "An internal server error occurred"
        }), 500

    @app.errorhandler(Exception)
    def handle_exception(error):
        app.logger.exception("Unhandled Exception: %s", str(error))
        return jsonify({
            "error": "Internal Server Error",
            "message": "An unexpected error occurred"
        }), 500

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