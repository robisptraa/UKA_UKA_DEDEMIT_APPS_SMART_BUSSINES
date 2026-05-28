import re
import pytest
import time
from unittest.mock import patch, MagicMock, AsyncMock

# Dummy decorator rate limit sederhana untuk pengujian terisolasi
from bot.main import rate_limit, USER_MESSAGE_TIMESTAMPS

# 1. Pengujian Rate Limiting
@pytest.mark.anyio
async def test_rate_limiting_triggered():
    # Setup mock update dan context
    mock_update = MagicMock()
    mock_update.effective_user.id = 12345
    mock_message = AsyncMock()
    mock_update.effective_message = mock_message
    
    mock_context = MagicMock()
    
    # Fungsi handler dummy
    mock_handler = AsyncMock()
    
    # Bungkus handler dengan rate limiter
    wrapped = rate_limit(mock_handler)
    
    # Bersihkan memori timestamp user 12345
    USER_MESSAGE_TIMESTAMPS[12345] = []
    
    # Kirim 20 pesan pertama (harus lolos rate limit)
    for i in range(20):
        await wrapped(mock_update, mock_context)
        
    assert mock_handler.call_count == 20
    mock_message.reply_text.assert_not_called()
    
    # Kirim pesan ke-21 dalam menit yang sama (harus terblokir rate limit)
    await wrapped(mock_update, mock_context)
    
    # Jumlah pemanggilan handler asli tetap 20 (terblokir)
    assert mock_handler.call_count == 20
    # Mengirimkan balasan peringatan
    mock_message.reply_text.assert_called_once()
    assert "terlalu cepat mengirim pesan" in mock_message.reply_text.call_args[0][0]

# 2. Pengujian Regex Parsing Chat Order Manual
def test_order_chat_regex_parsing():
    # Pola regex yang digunakan di order_chat.py
    pattern = r"^[Oo]rder\s+(.+?)\s*-\s*(.+?)\s*-\s*(.+)$"
    
    # Skenario 1: Format valid dengan spasi bervariasi
    text_1 = "Order Hoodie Carhartt - Obet - Jl. Sudirman No. 12"
    match_1 = re.match(pattern, text_1)
    assert match_1 is not None
    assert match_1.group(1).strip() == "Hoodie Carhartt"
    assert match_1.group(2).strip() == "Obet"
    assert match_1.group(3).strip() == "Jl. Sudirman No. 12"

    # Skenario 2: Format valid case-insensitive
    text_2 = "order Kaos Stussy Vintage - Budi Skena - Gang Senggol 5"
    match_2 = re.match(pattern, text_2)
    assert match_2 is not None
    assert match_2.group(1).strip() == "Kaos Stussy Vintage"
    assert match_2.group(2).strip() == "Budi Skena"
    assert match_2.group(3).strip() == "Gang Senggol 5"

    # Skenario 3: Format tidak valid (tidak menggunakan pemisah strip '-')
    text_3 = "Order Hoodie Carhartt Obet Jl. Sudirman"
    match_3 = re.match(pattern, text_3)
    assert match_3 is None

    # Skenario 4: Format tidak valid (kurang parameter alamat)
    text_4 = "Order Hoodie Carhartt - Obet"
    match_4 = re.match(pattern, text_4)
    assert match_4 is None
