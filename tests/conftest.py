import pytest
from flask import Flask
from src.api.v1.endpoints import api_v1
from src.extensions import limiter

class DummyLungAnalyzer:
    model_name = "dummy-model"
    def get_pathologies(self):
        return ["Pneumonia", "Fibrose", "COVID-19"]
    def analyze(self, image_data):
        return {"Pneumonia": 0.8, "Fibrose": 0.2, "COVID-19": 0.6}

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.register_blueprint(api_v1, url_prefix="/api/v1")
    app.lung_analyzer = DummyLungAnalyzer()
    limiter.init_app(app)
    yield app

@pytest.fixture
def client(app):
    return app.test_client() 