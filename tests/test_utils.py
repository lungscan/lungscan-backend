import pytest
from src.api.v1.endpoints import _allowed_file, _get_significant_pathologies

def test_allowed_file():
    allowed = {"png", "jpg", "jpeg"}
    assert _allowed_file("imagem.png", allowed)
    assert _allowed_file("foto.JPG", allowed)
    assert not _allowed_file("documento.pdf", allowed)
    assert not _allowed_file("semextensao", allowed)

def test_get_significant_pathologies():
    results = {"A": 0.7, "B": 0.3, "C": 0.5}
    assert _get_significant_pathologies(results) == {"A": 0.7, "C": 0.5}
    assert _get_significant_pathologies(results, threshold=0.6) == {"A": 0.7}
    assert _get_significant_pathologies(results, threshold=0.8) == {} 