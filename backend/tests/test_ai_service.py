import pytest
from unittest.mock import patch, MagicMock
from app.ai_service import (
    analyze_product_image,
    generate_item_description,
    validate_payment_proof,
    analyze_receipt_expense,
    analyze_business_performance,
    generate_customer_reply,
    generate_customer_sentiment
)

# String base64 1x1 pixel PNG transparan yang valid untuk pengujian
VALID_BASE64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="

# 1. Pengujian analyze_product_image
@patch('google.generativeai.GenerativeModel')
def test_analyze_product_image_success(mock_model_class):
    mock_model_instance = MagicMock()
    mock_model_class.return_value = mock_model_instance
    
    mock_response = MagicMock()
    mock_response.text = (
        '{"item_name": "Nasi Goreng Rendang", "category": "Kuliner", '
        '"condition": 5, "estimated_price": 25000.0, "details": "Porsi 1 piring", "confidence": 0.95}'
    )
    mock_model_instance.generate_content.return_value = mock_response
    
    result = analyze_product_image(VALID_BASE64, "kafe")
    
    assert result["item_name"] == "Nasi Goreng Rendang"
    assert result["category"] == "Kuliner"
    assert result["condition"] == 5
    assert result["estimated_price"] == 25000.0
    assert result["details"] == "Porsi 1 piring"
    assert result["confidence"] == 0.95

@patch('google.generativeai.GenerativeModel')
def test_analyze_product_image_failure(mock_model_class):
    mock_model_instance = MagicMock()
    mock_model_class.return_value = mock_model_instance
    mock_model_instance.generate_content.side_effect = Exception("API Timeout")
    
    result = analyze_product_image(VALID_BASE64, "salon")
    
    assert result["item_name"] == "Item Baru"
    assert result["condition"] == 5
    assert "error" in result
    assert result["error"] == "API Timeout"

# 2. Pengujian generate_item_description
@patch('google.generativeai.GenerativeModel')
def test_generate_item_description_success(mock_model_class):
    mock_model_instance = MagicMock()
    mock_model_class.return_value = mock_model_instance
    
    mock_response = MagicMock()
    mock_response.text = (
        '{"caption_whatsapp": "Halo Kak! Ready Nasi Goreng di Toko Budi.", '
        '"caption_instagram": "Promo Nasi Goreng enak parah!", '
        '"caption_tiktok": "Sikat Nasi Goreng Budi 🔥", '
        '"suggested_hashtags": ["#nasgor", "#makan enak"], '
        '"promo_text": "Diskon 10% hari ini", '
        '"recommended_price": "Rp 25.000"}'
    )
    mock_model_instance.generate_content.return_value = mock_response
    
    item_data = {
        "item_name": "Nasi Goreng",
        "store_name": "Toko Budi",
        "price": 25000.0
    }
    
    result = generate_item_description(item_data, "kafe")
    
    assert "Ready Nasi Goreng" in result["caption_whatsapp"]
    assert "Promo Nasi Goreng" in result["caption_instagram"]
    assert "#nasgor" in result["suggested_hashtags"]
    assert result["promo_text"] == "Diskon 10% hari ini"

# 3. Pengujian validate_payment_proof
@patch('google.generativeai.GenerativeModel')
def test_validate_payment_proof_valid(mock_model_class):
    mock_model_instance = MagicMock()
    mock_model_class.return_value = mock_model_instance
    
    mock_response = MagicMock()
    mock_response.text = (
        '{"sender_name": "Ahmad", "amount": 150000.0, "bank_or_wallet": "BCA", '
        '"transaction_date": "28 Mei 2026", "ref_number": "TX123", "confidence": 0.99}'
    )
    mock_model_instance.generate_content.return_value = mock_response
    
    result = validate_payment_proof(VALID_BASE64, 150000.0)
    
    assert result["is_valid"] is True
    assert result["extracted_data"]["sender_name"] == "Ahmad"
    assert result["extracted_data"]["amount"] == 150000.0
    assert result["mismatch_reason"] is None

@patch('google.generativeai.GenerativeModel')
def test_validate_payment_proof_invalid_outside_tolerance(mock_model_class):
    mock_model_instance = MagicMock()
    mock_model_class.return_value = mock_model_instance
    
    mock_response = MagicMock()
    mock_response.text = (
        '{"sender_name": "Ahmad", "amount": 148000.0, "bank_or_wallet": "BCA", '
        '"transaction_date": "28 Mei 2026", "ref_number": "TX123", "confidence": 0.99}'
    )
    mock_model_instance.generate_content.return_value = mock_response
    
    result = validate_payment_proof(VALID_BASE64, 150000.0)
    
    assert result["is_valid"] is False
    assert result["extracted_data"]["amount"] == 148000.0
    assert "mismatch_reason" in result
    assert "tidak cocok dengan yang diharapkan" in result["mismatch_reason"]

# 4. Pengujian analyze_receipt_expense
@patch('google.generativeai.GenerativeModel')
def test_analyze_receipt_expense_success(mock_model_class):
    mock_model_instance = MagicMock()
    mock_model_class.return_value = mock_model_instance
    
    mock_response = MagicMock()
    mock_response.text = (
        '{"merchant": "Indomaret", "total": 45000.0, "date": "2026-05-28", '
        '"items": ["Susu", "Roti"], "suggested_expense_category": "stok"}'
    )
    mock_model_instance.generate_content.return_value = mock_response
    
    result = analyze_receipt_expense(VALID_BASE64)
    
    assert result["merchant"] == "Indomaret"
    assert result["total"] == 45000.0
    assert "Susu" in result["items"]
    assert result["suggested_expense_category"] == "stok"

# 5. Pengujian analyze_business_performance
@patch('google.generativeai.GenerativeModel')
def test_analyze_business_performance_success(mock_model_class):
    mock_model_instance = MagicMock()
    mock_model_class.return_value = mock_model_instance
    
    mock_response = MagicMock()
    mock_response.text = (
        '{"top_products": ["Kopi Susu"], "slow_moving_items": ["Espresso"], '
        '"peak_hours": "08:00 - 10:00", "customer_insights": "Pembeli menyukai kopi manis.", '
        '"restock_recommendations": "Restock susu segar.", "revenue_trend": "Meningkat", '
        '"weekly_summary_text": "Performa toko Anda berjalan sangat baik minggu ini."}'
    )
    mock_model_instance.generate_content.return_value = mock_response
    
    result = analyze_business_performance({"sales": []})
    
    assert "Kopi Susu" in result["top_products"]
    assert "Espresso" in result["slow_moving_items"]
    assert result["peak_hours"] == "08:00 - 10:00"
    assert "sangat baik minggu ini" in result["weekly_summary_text"]

# 6. Pengujian generate_customer_reply
@patch('google.generativeai.GenerativeModel')
def test_generate_customer_reply_success(mock_model_class):
    mock_model_instance = MagicMock()
    mock_model_class.return_value = mock_model_instance
    
    mock_response = MagicMock()
    mock_response.text = "Halo Kak! Produk ready ya silakan diorder."
    mock_model_instance.generate_content.return_value = mock_response
    
    result = generate_customer_reply({"customer_message": "Apakah barang ready?"})
    
    assert "silakan diorder" in result

# 7. Pengujian generate_customer_sentiment
@patch('google.generativeai.GenerativeModel')
def test_generate_customer_sentiment_success(mock_model_class):
    mock_model_instance = MagicMock()
    mock_model_class.return_value = mock_model_instance
    
    mock_response = MagicMock()
    mock_response.text = (
        '{"overall_score": 4.5, "key_positives": ["Sangat cepat", "Ramah"], '
        '"key_complaints": [], "action_items": ["Pertahankan"]}'
    )
    mock_model_instance.generate_content.return_value = mock_response
    
    result = generate_customer_sentiment(["Sangat memuaskan!", "Pelayanan ramah"])
    
    assert result["overall_score"] == 4.5
    assert "Sangat cepat" in result["key_positives"]
    assert len(result["key_complaints"]) == 0
    assert "Pertahankan" in result["action_items"]
