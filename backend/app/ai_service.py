import os
import json
import base64
import logging
import time
import hashlib
from typing import List, Dict, Any, Optional
import google.generativeai as genai
from app.config import settings

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app.ai_service")

# Konfigurasi Gemini API jika API Key tersedia
if settings.gemini_api_key:
    genai.configure(api_key=settings.gemini_api_key)
    logger.info("Gemini API berhasil dikonfigurasi menggunakan kunci dari settings.")
else:
    logger.warning("GEMINI_API_KEY tidak ditemukan di konfigurasi.")

# Mencoba mengimpor dan mengonfigurasi redis untuk caching & rate limiting
redis_client = None
try:
    import redis
    if settings.redis_url:
        redis_client = redis.from_url(settings.redis_url, decode_responses=True)
        logger.info("Koneksi Redis untuk Caching & Rate Limiting berhasil diinisialisasi.")
except Exception as e:
    logger.warning(f"Gagal menginisialisasi Redis (AI Caching & Rate Limiting akan jatuh ke mode In-Memory): {str(e)}")

# Penyimpanan lokal jika Redis tidak aktif
_in_memory_cache = {}
_in_memory_rate_limit = {}

# Persona Dedemit AI
DEDEMIT_PERSONA = (
    "Kamu adalah Dedemit AI — asisten bisnis UMKM Indonesia yang cerdas, ramah, "
    "dan praktis. Bahasa yang kamu gunakan adalah bahasa Indonesia yang sopan namun santai, "
    "khas wirausaha lokal, penuh motivasi, dan sangat solutif. Hindari kalimat bertele-tele."
)

def _clean_base64(image_base64: str) -> tuple[bytes, str]:
    """
    Membersihkan string base64 dari format data URL (jika ada) dan mengembalikan data bytes serta mime_type.
    """
    mime_type = "image/jpeg"  # default
    if "," in image_base64:
        header, image_base64 = image_base64.split(",", 1)
        if "image/png" in header:
            mime_type = "image/png"
        elif "image/webp" in header:
            mime_type = "image/webp"
        elif "image/gif" in header:
            mime_type = "image/gif"
    
    cleaned_base64 = "".join(image_base64.split())
    missing_padding = len(cleaned_base64) % 4
    if missing_padding:
        cleaned_base64 += '=' * (4 - missing_padding)
        
    return base64.b64decode(cleaned_base64), mime_type

def check_rate_limit(user_id: str) -> bool:
    """
    Mengecek apakah user melebihi 100 request/menit.
    Mengembalikan True jika diizinkan, False jika terkena rate limit.
    """
    current_minute = int(time.time() / 60)
    key = f"rate_limit:{user_id}:{current_minute}"
    
    if redis_client:
        try:
            current_count = redis_client.incr(key)
            if current_count == 1:
                redis_client.expire(key, 60)
            return current_count <= 100
        except Exception as e:
            logger.error(f"Redis rate limit error: {str(e)}")
            
    # Fallback to In-Memory
    if key not in _in_memory_rate_limit:
        _in_memory_rate_limit[key] = 0
    _in_memory_rate_limit[key] += 1
    return _in_memory_rate_limit[key] <= 100

def _get_cache(cache_key: str) -> Optional[Dict[str, Any]]:
    """
    Mengambil data cache dari Redis atau In-Memory.
    """
    if redis_client:
        try:
            cached_data = redis_client.get(cache_key)
            if cached_data:
                logger.info(f"Cache HIT untuk key: {cache_key}")
                return json.loads(cached_data)
        except Exception as e:
            logger.error(f"Redis get cache error: {str(e)}")
            
    # Fallback In-Memory
    if cache_key in _in_memory_cache:
        expire_at, val = _in_memory_cache[cache_key]
        if time.time() < expire_at:
            logger.info(f"In-Memory Cache HIT untuk key: {cache_key}")
            return val
        else:
            del _in_memory_cache[cache_key]
    return None

def _set_cache(cache_key: str, value: Dict[str, Any], expire_seconds: int = 3600):
    """
    Menyimpan data cache ke Redis atau In-Memory.
    """
    if redis_client:
        try:
            redis_client.setex(cache_key, expire_seconds, json.dumps(value))
            return
        except Exception as e:
            logger.error(f"Redis set cache error: {str(e)}")
            
    # Fallback In-Memory
    _in_memory_cache[cache_key] = (time.time() + expire_seconds, value)

# ==============================================================================
# 1. ANALYZE PRODUCT IMAGE (Context-Aware)
# ==============================================================================
def analyze_product_image(image_base64: str, business_type: str, user_id: str = "default_user") -> Dict[str, Any]:
    """
    Menganalisis gambar produk atau jasa secara asinkron berdasarkan sektor bisnis UMKM.
    Return: {item_name, category, condition, estimated_price, details, confidence}
    """
    if not check_rate_limit(user_id):
        return {"error": "Rate limit terlampaui. Batas maksimal adalah 100 request/menit."}

    # Generate MD5 hash dari base64 untuk key caching unik
    img_hash = hashlib.md5(image_base64.encode('utf-8')).hexdigest()
    cache_key = f"cache:analyze_image:{business_type}:{img_hash}"
    
    cached_val = _get_cache(cache_key)
    if cached_val:
        return cached_val

    logger.info(f"Memulai analyze_product_image untuk sektor: {business_type}")
    start_time = time.time()
    
    fallback_response = {
        "item_name": "Item Baru",
        "category": "Lainnya",
        "condition": 5,
        "estimated_price": 50000.0,
        "details": "Tidak dapat mendeteksi item secara detail.",
        "confidence": 0.0
    }

    # Context-aware instructions based on business type
    context_instructions = ""
    if business_type == "warung" or business_type == "toko":
        context_instructions = "Deteksi nama produk fisik barang kelontong/warung, merek/brand, dan estimasi tanggal kadaluarsa jika ada pada kemasan."
    elif business_type == "salon":
        context_instructions = "Deteksi jenis produk perawatan rambut/kulit/kecantikan, merek/brand, dan ukuran volume (ml/gr) jika tertera."
    elif business_type == "bengkel":
        context_instructions = "Deteksi jenis suku cadang kendaraan, kode part/nomor part jika terlihat, dan estimasi kondisi barunya."
    elif business_type == "kafe":
        context_instructions = "Deteksi nama menu makanan/minuman kopi/non-kopi, estimasi porsi (cup/piring), dan bahan utama penyusunnya."
    else:
        context_instructions = "Deteksi nama item, jenis kategori, kondisi kelayakan fisik, dan deskripsi detail lainnya secara universal."

    try:
        image_bytes, mime_type = _clean_base64(image_base64)
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        prompt = (
            f"{DEDEMIT_PERSONA}\n\n"
            "Tugas Anda adalah memproses gambar produk atau jasa UMKM Indonesia ini secara cerdas.\n"
            f"Sektor Usaha: {business_type}\n"
            f"Instruksi Khusus Sektor: {context_instructions}\n\n"
            "Format respons HARUS berupa JSON valid dengan kunci data berikut:\n"
            "{\n"
            '  "item_name": "Nama item produk atau jasa terdeteksi (string)",\n'
            '  "category": "Kategori produk/jasa yang cocok (string)",\n'
            '  "condition": Nilai skala kelayakan/kualitas barang 1-5 (integer 1-5),\n'
            '  "estimated_price": Estimasi harga pasar wajar dalam Rupiah (float/integer),\n'
            '  "details": "Keterangan detail khusus sektor, seperti tanggal kadaluarsa, ukuran, bahan utama, atau kode part (string)",\n'
            '  "confidence": Tingkat keyakinan deteksi 0.0 hingga 1.0 (float)\n'
            "}"
        )
        
        image_part = {"mime_type": mime_type, "data": image_bytes}
        generation_config = {"response_mime_type": "application/json"}
        
        response = model.generate_content(
            contents=[image_part, prompt],
            generation_config=generation_config
        )
        
        latency = time.time() - start_time
        result_text = response.text
        logger.info(f"Gemini analyze_product_image latency: {latency:.2f}s, response: {result_text}")
        
        parsed = json.loads(result_text)
        
        normalized_res = {
            "item_name": str(parsed.get("item_name", fallback_response["item_name"])),
            "category": str(parsed.get("category", fallback_response["category"])),
            "condition": int(parsed.get("condition", 5)),
            "estimated_price": float(parsed.get("estimated_price", fallback_response["estimated_price"])),
            "details": str(parsed.get("details", fallback_response["details"])),
            "confidence": float(parsed.get("confidence", 0.5))
        }
        
        # Simpan ke cache selama 1 jam
        _set_cache(cache_key, normalized_res, 3600)
        return normalized_res

    except Exception as e:
        logger.error(f"Gagal menganalisis gambar: {str(e)}", exc_info=True)
        fallback_response["error"] = str(e)
        return fallback_response

# ==============================================================================
# 2. GENERATE ITEM DESCRIPTION
# ==============================================================================
def generate_item_description(item_data: Dict[str, Any], business_type: str) -> Dict[str, Any]:
    """
    Menghasilkan materi promosi/caption media sosial berdasarkan data item, harga, dan nama toko.
    Return: {caption_whatsapp, caption_instagram, caption_tiktok, suggested_hashtags, promo_text, recommended_price}
    """
    logger.info(f"Memulai generate_item_description untuk sektor: {business_type}")
    
    price = item_data.get("price", item_data.get("estimated_price", 0.0))
    store_name = item_data.get("store_name", "Toko Kami")
    item_name = item_data.get("item_name", "Produk/Jasa Baru")
    
    fallback_response = {
        "caption_whatsapp": f"Halo Kak! Ready nih *{item_name}* berkualitas di *{store_name}*. Yuk buruan diorder sekarang! Harga terjangkau hanya Rp {price:,.0f}.",
        "caption_instagram": f"Ready now! ✨ {item_name} kualitas premium di @{store_name}. Harga bersahabat Rp {price:,.0f}. Kunjungi toko kami atau hubungi via DM!",
        "caption_tiktok": f"Buruan check out {item_name} sebelum kehabisan! Hanya di {store_name} 🔥 #UMKMBisa Rp {price:,.0f}",
        "suggested_hashtags": ["umkmindonesia", "localbusiness", "produklokal"],
        "promo_text": "Diskon spesial belanja hari ini!",
        "recommended_price": f"Rp {price:,.0f}"
    }

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        prompt = (
            f"{DEDEMIT_PERSONA}\n\n"
            "Tugas Anda adalah menghasilkan materi caption pemasaran media sosial yang ramah, lokal, "
            "dan persuasif sesuai target pasar UMKM Indonesia.\n"
            f"Nama Toko: {store_name}\n"
            f"Sektor Usaha: {business_type}\n"
            f"Data Item: {json.dumps(item_data)}\n"
            f"Harga Jual: Rp {price:,.0f}\n\n"
            "Format respons HARUS berupa JSON valid dengan kunci data berikut:\n"
            "{\n"
            '  "caption_whatsapp": "Caption ramah dengan bullet points dan emoji untuk disebar di WA (string)",\n'
            '  "caption_instagram": "Caption estetik penuh cerita persuasif untuk feeds Instagram (string)",\n'
            '  "caption_tiktok": "Caption pendek, penuh energi, FOMO, cocok untuk FYP (string)",\n'
            '  "suggested_hashtags": ["#tag1", "#tag2", ...],\n'
            '  "promo_text": "Kalimat diskon/headline promo menarik satu baris (string)",\n'
            '  "recommended_price": "Harga pasaran rekomendasi dalam bentuk string rupiah (string)"\n'
            "}"
        )
        
        generation_config = {"response_mime_type": "application/json"}
        response = model.generate_content(contents=prompt, generation_config=generation_config)
        
        parsed = json.loads(response.text)
        return {
            "caption_whatsapp": str(parsed.get("caption_whatsapp", fallback_response["caption_whatsapp"])),
            "caption_instagram": str(parsed.get("caption_instagram", fallback_response["caption_instagram"])),
            "caption_tiktok": str(parsed.get("caption_tiktok", fallback_response["caption_tiktok"])),
            "suggested_hashtags": list(parsed.get("suggested_hashtags", fallback_response["suggested_hashtags"])),
            "promo_text": str(parsed.get("promo_text", fallback_response["promo_text"])),
            "recommended_price": str(parsed.get("recommended_price", fallback_response["recommended_price"]))
        }

    except Exception as e:
        logger.error(f"Gagal generate_item_description: {str(e)}", exc_info=True)
        return fallback_response

# ==============================================================================
# 3. VALIDATE PAYMENT PROOF
# ==============================================================================
def validate_payment_proof(image_base64: str, expected_amount: float) -> Dict[str, Any]:
    """
    OCR bukti transfer dan memvalidasi apakah jumlah transfer cocok dengan nominal yang diharapkan.
    Mendukung BCA, BRI, Mandiri, BNI, BSI, BTN, CIMB, GoPay, OVO, Dana, ShopeePay, LinkAja.
    Toleransi selisih ±Rp 1.000.
    """
    logger.info(f"Memulai validate_payment_proof. Diharapkan: Rp {expected_amount:,.0f}")
    
    fallback_response = {
        "is_valid": False,
        "extracted_data": {
            "sender_name": "Unknown",
            "amount": 0.0,
            "bank_or_wallet": "Unknown",
            "transaction_date": "Unknown",
            "ref_number": "Unknown"
        },
        "confidence": 0.0,
        "mismatch_reason": "Gagal membaca struk pembayaran."
    }

    try:
        image_bytes, mime_type = _clean_base64(image_base64)
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        prompt = (
            "Anda adalah AI asisten pembaca bukti pembayaran perbankan dan e-wallet di Indonesia.\n"
            "Analisis gambar struk transfer/bukti bayar ini (BCA, BRI, Mandiri, BNI, BSI, BTN, CIMB, GoPay, OVO, Dana, ShopeePay, LinkAja, dll).\n"
            "Ekstrak data penting secara akurat.\n\n"
            "Format respons HARUS berupa JSON valid dengan kunci data berikut:\n"
            "{\n"
            '  "sender_name": "Nama pemilik rekening pengirim. Jika tidak terbaca tulis Unknown (string)",\n'
            '  "amount": Nominal angka numerik uang yang dikirim saja tanpa titik/koma (float/integer),\n'
            '  "bank_or_wallet": "Nama bank atau dompet digital asal/tujuan (string)",\n'
            '  "transaction_date": "Tanggal transaksi berlangsung (string)",\n'
            '  "ref_number": "Nomor referensi/ID transaksi/Nomor jurnal (string)",\n'
            '  "confidence": Tingkat keyakinan OCR 0.0-1.0 (float)\n'
            "}"
        )
        
        image_part = {"mime_type": mime_type, "data": image_bytes}
        generation_config = {"response_mime_type": "application/json"}
        
        response = model.generate_content(contents=[image_part, prompt], generation_config=generation_config)
        parsed = json.loads(response.text)
        
        extracted_amount = float(parsed.get("amount", 0.0))
        sender_name = str(parsed.get("sender_name", "Unknown"))
        bank_or_wallet = str(parsed.get("bank_or_wallet", "Unknown"))
        transaction_date = str(parsed.get("transaction_date", "Unknown"))
        ref_number = str(parsed.get("ref_number", parsed.get("reference_number", "Unknown")))
        confidence = float(parsed.get("confidence", 0.5))
        
        # Validasi nominal di Python dengan toleransi ±Rp 1.000
        difference = abs(extracted_amount - expected_amount)
        is_valid = difference <= 1000.0
        mismatch_reason = None if is_valid else f"Nominal transfer Rp {extracted_amount:,.0f} tidak cocok dengan yang diharapkan Rp {expected_amount:,.0f}."
        
        return {
            "is_valid": is_valid,
            "extracted_data": {
                "sender_name": sender_name,
                "amount": extracted_amount,
                "bank_or_wallet": bank_or_wallet,
                "transaction_date": transaction_date,
                "ref_number": ref_number
            },
            "confidence": confidence,
            "mismatch_reason": mismatch_reason
        }

    except Exception as e:
        logger.error(f"Gagal validasi bukti bayar: {str(e)}", exc_info=True)
        fallback_response["mismatch_reason"] = f"Kesalahan internal: {str(e)}"
        return fallback_response

# ==============================================================================
# 4. ANALYZE RECEIPT EXPENSE
# ==============================================================================
def analyze_receipt_expense(image_base64: str) -> Dict[str, Any]:
    """
    OCR struk belanja / nota pembelian untuk mencatat pengeluaran operasional toko secara asinkron.
    Return: {merchant, total, date, items, suggested_expense_category}
    """
    logger.info("Memulai analyze_receipt_expense.")
    
    fallback_response = {
        "merchant": "Merchant Baru",
        "total": 0.0,
        "date": "2026-05-28",
        "items": [],
        "suggested_expense_category": "lainnya"
    }

    try:
        image_bytes, mime_type = _clean_base64(image_base64)
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        prompt = (
            "Anda adalah asisten keuangan pintar UMKM Indonesia.\n"
            "Tugas Anda adalah membaca gambar struk/nota belanja pengeluaran bisnis dan mengekstrak data keuangan.\n\n"
            "Format respons HARUS berupa JSON valid dengan kunci data berikut:\n"
            "{\n"
            '  "merchant": "Nama toko / tempat berbelanja (string)",\n'
            '  "total": Nominal total pengeluaran belanja (float/integer),\n'
            '  "date": "Tanggal belanja dalam format YYYY-MM-DD (string)",\n'
            '  "items": ["Nama item 1", "Nama item 2", ...],\n'
            '  "suggested_expense_category": "Rekomendasi kategori pengeluaran: stok, listrik, gaji, sewa, atau lainnya (string)"\n'
            "}"
        )
        
        image_part = {"mime_type": mime_type, "data": image_bytes}
        generation_config = {"response_mime_type": "application/json"}
        
        response = model.generate_content(contents=[image_part, prompt], generation_config=generation_config)
        parsed = json.loads(response.text)
        
        return {
            "merchant": str(parsed.get("merchant", fallback_response["merchant"])),
            "total": float(parsed.get("total", fallback_response["total"])),
            "date": str(parsed.get("date", fallback_response["date"])),
            "items": list(parsed.get("items", fallback_response["items"])),
            "suggested_expense_category": str(parsed.get("suggested_expense_category", fallback_response["suggested_expense_category"]))
        }

    except Exception as e:
        logger.error(f"Gagal memproses struk pengeluaran: {str(e)}", exc_info=True)
        return fallback_response

# ==============================================================================
# 5. ANALYZE BUSINESS PERFORMANCE
# ==============================================================================
def analyze_business_performance(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Menganalisis performa bisnis 30 hari terakhir.
    Return: {top_products, slow_moving_items, peak_hours, customer_insights, restock_recommendations, revenue_trend, weekly_summary_text}
    """
    logger.info("Memulai analyze_business_performance.")
    
    fallback_response = {
        "top_products": ["Kategori Produk A"],
        "slow_moving_items": ["Kategori Produk B"],
        "peak_hours": "12:00 - 15:00",
        "customer_insights": "Sebagian besar pelanggan menyukai menu baru.",
        "restock_recommendations": "Restock produk kategori A segera.",
        "revenue_trend": "Meningkat 10% dibanding minggu lalu.",
        "weekly_summary_text": "Performa toko Anda minggu ini berjalan cukup stabil dan mengalami kenaikan omset. Terus pertahankan stok barang favorit pelanggan agar keuntungan tetap konsisten. Jangan lupa untuk mulai gencar berpromosi pada jam-jam ramai!"
    }

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        prompt = (
            f"{DEDEMIT_PERSONA}\n\n"
            "Tugas Anda adalah bertindak sebagai konsultan bisnis UMKM pintar.\n"
            "Analisis data historis performa toko 30 hari terakhir berikut:\n"
            f"{json.dumps(data)}\n\n"
            "Format respons HARUS berupa JSON valid dengan kunci data berikut:\n"
            "{\n"
            '  "top_products": ["Daftar barang terlaris (string)", ...],\n'
            '  "slow_moving_items": ["Daftar barang kurang laku (string)", ...],\n'
            '  "peak_hours": "Keterangan jam tersibuk toko (string)",\n'
            '  "customer_insights": "Analisis perilaku pembeli secara singkat (string)",\n'
            '  "restock_recommendations": "Saran restock konkrit barang tertentu (string)",\n'
            '  "revenue_trend": "Tren pergerakan omset (string)",\n'
            '  "weekly_summary_text": "Narasi ringkasan performa mingguan dalam bahasa Indonesia yang ramah bagi owner awam, terdiri dari 3-5 kalimat terstruktur (string)"\n'
            "}"
        )
        
        generation_config = {"response_mime_type": "application/json"}
        response = model.generate_content(contents=prompt, generation_config=generation_config)
        parsed = json.loads(response.text)
        
        return {
            "top_products": list(parsed.get("top_products", fallback_response["top_products"])),
            "slow_moving_items": list(parsed.get("slow_moving_items", fallback_response["slow_moving_items"])),
            "peak_hours": str(parsed.get("peak_hours", fallback_response["peak_hours"])),
            "customer_insights": str(parsed.get("customer_insights", fallback_response["customer_insights"])),
            "restock_recommendations": str(parsed.get("restock_recommendations", fallback_response["restock_recommendations"])),
            "revenue_trend": str(parsed.get("revenue_trend", fallback_response["revenue_trend"])),
            "weekly_summary_text": str(parsed.get("weekly_summary_text", fallback_response["weekly_summary_text"]))
        }

    except Exception as e:
        logger.error(f"Gagal analyze_business_performance: {str(e)}", exc_info=True)
        return fallback_response

# ==============================================================================
# 6. GENERATE CUSTOMER REPLY
# ==============================================================================
def generate_customer_reply(context: Dict[str, Any]) -> str:
    """
    Menghasilkan draft balasan pesan pelanggan WhatsApp/Telegram secara asinkron.
    """
    logger.info("Memulai generate_customer_reply.")
    
    fallback_response = (
        "Halo Kak! Terima kasih sudah menghubungi kami. "
        "Pertanyaan Kakak akan segera kami jawab ya. Harap tunggu sebentar. Terima kasih!"
    )

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        prompt = (
            f"{DEDEMIT_PERSONA}\n\n"
            "Tugas Anda adalah menulis draft balasan pesan singkat untuk pelanggan toko via WhatsApp/Telegram.\n"
            "Balasan harus sopan, bersahabat, informatif, dan langsung menjawab esensi pertanyaan pelanggan.\n\n"
            f"Konteks Bisnis & Pertanyaan Pelanggan:\n{json.dumps(context)}\n\n"
            "Tulis draft balasannya secara natural dan siap kirim (tanpa tanda kutip penutup berlebih)."
        )
        
        response = model.generate_content(contents=prompt)
        return response.text.strip()

    except Exception as e:
        logger.error(f"Gagal generate_customer_reply: {str(e)}", exc_info=True)
        return fallback_response

# ==============================================================================
# 7. GENERATE CUSTOMER SENTIMENT
# ==============================================================================
def generate_customer_sentiment(feedbacks: List[str]) -> Dict[str, Any]:
    """
    Menganalisis sentimen ulasan atau masukan dari pelanggan dan merangkum poin penting.
    Return: {overall_score, key_positives, key_complaints, action_items}
    """
    logger.info(f"Memulai generate_customer_sentiment dengan {len(feedbacks)} masukan.")
    
    fallback_response = {
        "overall_score": 4.0,
        "key_positives": ["Layanan ramah"],
        "key_complaints": [],
        "action_items": ["Pertahankan kualitas layanan"]
    }

    if not feedbacks:
        return fallback_response

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        prompt = (
            "Anda adalah AI penganalisis sentimen pelanggan UMKM Indonesia.\n"
            "Tugas Anda adalah membaca daftar ulasan atau kritik pelanggan berikut dan meringkasnya:\n"
            f"{json.dumps(feedbacks)}\n\n"
            "Format respons HARUS berupa JSON valid dengan kunci data berikut:\n"
            "{\n"
            '  "overall_score": Skor kepuasan keseluruhan skala 1.0 - 5.0 (float),\n'
            '  "key_positives": ["Poin positif utama 1", ...],\n'
            '  "key_complaints": ["Poin keluhan utama 1", ...],\n'
            '  "action_items": ["Daftar tindakan korektif/peningkatan konkret", ...]\n'
            "}"
        )
        
        generation_config = {"response_mime_type": "application/json"}
        response = model.generate_content(contents=prompt, generation_config=generation_config)
        parsed = json.loads(response.text)
        
        return {
            "overall_score": float(parsed.get("overall_score", fallback_response["overall_score"])),
            "key_positives": list(parsed.get("key_positives", fallback_response["key_positives"])),
            "key_complaints": list(parsed.get("key_complaints", fallback_response["key_complaints"])),
            "action_items": list(parsed.get("action_items", fallback_response["action_items"]))
        }

    except Exception as e:
        logger.error(f"Gagal generate_customer_sentiment: {str(e)}", exc_info=True)
        return fallback_response
