import pytest
import hashlib
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.config import settings
from app.models.order import OrderModel
from app.models.product_service import ProductServiceModel
from app.payment_service import (
    create_payment_link,
    create_quick_payment_link,
    verify_webhook_signature,
    handle_payment_notification
)

# Kunci server dummy untuk pengujian signature
DUMMY_SERVER_KEY = "dummy_midtrans_server_key"

# 1. Pengujian create_payment_link (Snap API)
@pytest.mark.anyio
@patch('httpx.AsyncClient.post')
async def test_create_payment_link_success(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {
        "token": "snap-token-123456789",
        "redirect_url": "https://app.sandbox.midtrans.com/snap/v2/vtweb/snap-token-123456789"
    }
    mock_post.return_value = mock_response

    db_mock = AsyncMock(spec=AsyncSession)
    product_dummy = ProductServiceModel(id="PROD-1", name="Kopi Susu Aren", price=15000.0)
    
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = product_dummy
    db_mock.execute.return_value = mock_result

    order_dummy = OrderModel(
        id="ORDER-999",
        items=[{"product_id": "PROD-1", "qty": 2, "price": 15000.0}],
        discount=5000.0,
        total=25000.0
    )

    store_info = {"expired_hours": 24}
    result = await create_payment_link(order_dummy, store_info, db_mock)

    assert result["snap_token"] == "snap-token-123456789"
    assert "snap-token-123456789" in result["payment_url"]
    assert "error" not in result

# 2. Pengujian create_quick_payment_link
@pytest.mark.anyio
@patch('httpx.AsyncClient.post')
async def test_create_quick_payment_link_success(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {
        "redirect_url": "https://app.sandbox.midtrans.com/snap/v2/vtweb/quick-token-123"
    }
    mock_post.return_value = mock_response

    customer = {"name": "Budi", "phone": "08123"}
    result = await create_quick_payment_link(20000.0, "Cuci Laundry Kiloan", customer)

    assert "quick-token-123" in result["payment_url"]
    assert "error" not in result

# 3. Pengujian verify_webhook_signature
def test_verify_webhook_signature_valid():
    order_id = "ORD-777"
    status_code = "200"
    gross_amount = "150000.00"
    
    payload_str = f"{order_id}{status_code}{gross_amount}{DUMMY_SERVER_KEY}"
    valid_signature = hashlib.sha512(payload_str.encode("utf-8")).hexdigest()

    notification = {
        "order_id": order_id,
        "status_code": status_code,
        "gross_amount": gross_amount,
        "signature_key": valid_signature
    }

    assert verify_webhook_signature(notification, DUMMY_SERVER_KEY) is True

def test_verify_webhook_signature_invalid():
    notification = {
        "order_id": "ORD-777",
        "status_code": "200",
        "gross_amount": "150000.00",
        "signature_key": "wrong_signature"
    }

    assert verify_webhook_signature(notification, DUMMY_SERVER_KEY) is False

# 4. Pengujian handle_payment_notification
@pytest.mark.anyio
@patch('app.payment_service.send_telegram_notification', new_callable=AsyncMock)
async def test_handle_notification_settlement_success(mock_send_telegram):
    db_mock = AsyncMock(spec=AsyncSession)
    
    order_dummy = OrderModel(
        id="ORD-SUCCESS",
        user_id="USER-1",
        items=[{"product_id": "PROD-1", "qty": 1, "price": 15000.0}],
        total=15000.0,
        status="pending",
        payment_status="unpaid"
    )

    mock_result_order = MagicMock()
    mock_result_order.scalars.return_value.first.return_value = order_dummy
    db_mock.execute.return_value = mock_result_order

    notification = {
        "order_id": "ORD-SUCCESS",
        "transaction_status": "settlement",
        "transaction_id": "TX-111",
        "payment_type": "qris",
        "gross_amount": "150000.00"
    }

    result = await handle_payment_notification(notification, db_mock)

    assert result["new_status"] == "confirmed"
    assert order_dummy.payment_status == "paid"
    db_mock.commit.assert_called_once()
    mock_send_telegram.assert_called_once()

# 5. Pengujian API Endpoint Webhook (POST /v1/webhooks/midtrans)
client = TestClient(app)

@patch('app.api.v1.webhooks.verify_webhook_signature')
@patch('app.api.v1.webhooks.handle_payment_notification', new_callable=AsyncMock)
def test_midtrans_webhook_endpoint_success(mock_handle, mock_verify):
    mock_verify.return_value = True
    mock_handle.return_value = {
        "order_id": "ORD-123",
        "new_status": "confirmed",
        "message": "Webhook sukses."
    }

    payload = {
        "order_id": "ORD-123",
        "transaction_status": "settlement",
        "gross_amount": "15000.00",
        "signature_key": "dummy"
    }

    response = client.post("/api/v1/webhooks/midtrans", json=payload)

    assert response.status_code == 200
    assert response.json()["new_status"] == "confirmed"
