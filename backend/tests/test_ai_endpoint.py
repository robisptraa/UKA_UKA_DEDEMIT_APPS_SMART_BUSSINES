import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

# Setup FastAPI TestClient
client = TestClient(app)

@patch('app.api.v1.ai.analyze_product_image')
def test_analyze_product_endpoint_success(mock_analyze_image):
    # Setup mock return value dari Gemini AI service
    mock_analyze_image.return_value = {
        "brand": "Carhartt",
        "category": "Jacket",
        "color": "Duck Brown",
        "condition": 4,
        "year_estimate": "Vintage 90s",
        "confidence": 0.95
    }

    # Buat file mockup gambar dummy untuk diupload
    dummy_file = ("test_jacket.png", b"fake-png-file-content", "image/png")

    response = client.post(
        "/api/v1/ai/analyze-product",
        files={"file": dummy_file}
    )

    # Assertions
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["brand"] == "Carhartt"
    assert json_data["category"] == "Jacket"
    assert json_data["color"] == "Duck Brown"
    assert json_data["condition"] == 4
    assert json_data["year_estimate"] == "Vintage 90s"
    assert json_data["confidence"] == 0.95
    
    # Verifikasi pemanggilan mock
    mock_analyze_image.assert_called_once()

def test_analyze_product_endpoint_invalid_file_extension():
    # Buat file mockup dengan ekstensi yang tidak diizinkan (.pdf)
    dummy_file = ("document.pdf", b"fake-pdf-content", "application/pdf")

    response = client.post(
        "/api/v1/ai/analyze-product",
        files={"file": dummy_file}
    )

    # Harus ditolak dengan status code 400 Bad Request
    assert response.status_code == 400
    assert "Format file tidak didukung" in response.json()["detail"]

@patch('app.api.v1.ai.analyze_product_image')
def test_analyze_product_endpoint_server_error(mock_analyze_image):
    # Simulasikan error internal / timeout dari Gemini API
    mock_analyze_image.side_effect = Exception("Gemini API Timeout")

    dummy_file = ("test_jacket.png", b"fake-png-file-content", "image/png")

    response = client.post(
        "/api/v1/ai/analyze-product",
        files={"file": dummy_file}
    )

    # Harus menghasilkan status code 500 Internal Server Error
    assert response.status_code == 500
    assert "Terjadi kegagalan pemrosesan AI internal" in response.json()["detail"]
