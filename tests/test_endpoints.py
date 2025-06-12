import io
import pytest

def test_health(client):
    resp = client.get("/api/v1/health")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "healthy"
    assert "timestamp" in data

def test_get_pathologies(client):
    resp = client.get("/api/v1/pathologies")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["success"] is True
    assert isinstance(data["pathologies"], list)
    assert data["count"] == len(data["pathologies"])

def test_analyze_lung_scan(client):
    # Cria uma imagem fake (bytes)
    img_bytes = io.BytesIO(b"fake image data")
    data = {"image": (img_bytes, "test.jpg")}
    resp = client.post("/api/v1/analyze", data=data, content_type="multipart/form-data")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["success"] is True
    assert "predictions" in data
    assert "pathologies_detected" in data
    assert "model_info" in data

def test_analyze_lung_scan_no_file(client):
    resp = client.post("/api/v1/analyze", data={}, content_type="multipart/form-data")
    assert resp.status_code == 400
    data = resp.get_json()
    assert data["error"] == "No image file provided"

def test_analyze_lung_scan_invalid_type(client):
    fake_file = io.BytesIO(b"fake data")
    data = {"image": (fake_file, "test.txt")}
    resp = client.post("/api/v1/analyze", data=data, content_type="multipart/form-data")
    assert resp.status_code == 400
    data = resp.get_json()
    assert data["error"] == "Invalid file type"

def test_get_images_folder_nao_existe(client, monkeypatch):
    # Monkeypatch para simular pasta inexistente
    monkeypatch.setattr("os.path.exists", lambda x: False)
    resp = client.get("/api/v1/get_images")
    assert resp.status_code == 404
    data = resp.get_json()
    assert "Images folder not found" in data["error"] 