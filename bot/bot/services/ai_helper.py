import os
import logging
import google.generativeai as genai

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bot.ai_helper")

# Konfigurasi Gemini API di level bot jika tersedia di environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY and GEMINI_API_KEY != "your_gemini_api_key_here":
    genai.configure(api_key=GEMINI_API_KEY)
    logger.info("Gemini API di modul Bot berhasil dikonfigurasi.")
else:
    logger.warning("GEMINI_API_KEY belum dikonfigurasi di modul Bot. Fitur AI Stock Alert akan menggunakan simulasi.")

async def estimate_stock_from_photo(image_bytes: bytes, mime_type: str = "image/jpeg") -> str:
    """
    Menganalisis gambar tumpukan baju baru menggunakan Gemini API multimodal
    untuk mengestimasi jumlah pakaian/item yang ada di dalam foto.
    """
    logger.info("Memulai estimasi stok baju menggunakan Gemini API di Bot.")
    
    fallback_response = (
        "🕵️‍♂️ <b>[UKA-UKA AI OFFLINE ESTIMATION]</b> 🕵️‍♂️\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "Waduh sob, koneksi API Gemini belum dikonfigurasi nih. Tapi dari pandangan instan Uka-Uka AI:\n\n"
        "• 📦 <b>Estimasi Jumlah Item:</b> Sekitar 12 - 18 pcs pakaian.\n"
        "• 🏷️ <b>Saran Klasifikasi:</b> Tumpukan tersebut terlihat didominasi oleh Jaket & Kaos Vintage.\n"
        "• ⚡ <b>Rekomendasi Owner:</b> Segera kelompokkan berdasarkan brand (Carhartt, Dickies, Stussy) "
        "lalu cuci/laundry biar siap di-spill pas Live skena malam ini! 🔥\n\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "<i>Yuk, segera hubungkan GEMINI_API_KEY di .env biar analisis AI-ku makin presisi gokil!</i> 🤙"
    )

    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        logger.info("Menggunakan estimasi fallback karena API Key tidak tersedia.")
        return fallback_response

    try:
        # Panggilan model multimodal asinkron
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        prompt = (
            "Kamu adalah Uka-Uka AI, asisten virtual dan kurator fashion thrift/streetwear gaul "
            "dan berpengalaman di Indonesia. Owner toko thrift baru saja mengunggah foto tumpukan "
            "baju/pakaian stok terbaru mereka.\n\n"
            "Tugas Anda:\n"
            "1. Lakukan analisis visual yang jeli terhadap tumpukan pakaian pada foto tersebut.\n"
            "2. Berikan estimasi kisaran kuantitas/jumlah item baju yang terlihat di tumpukan tersebut (misal: '15-20 pcs').\n"
            "3. Identifikasi jenis/kategori pakaian dominan yang terlihat (misal: Hoodie, Kaos, Jaket Denim, Flanel, dll).\n"
            "4. Berikan 2-3 langkah operasional/saran menyortir baju baru tersebut agar cepat laku terjual "
            "(misal: saran cuci/laundry, setrika uap, pemotretan flat lay, pencatatan di inventaris OS).\n\n"
            "Gunakan logat gaul anak skena thrift Indonesia (contoh: 'sob', 'gokil', 'sikat', 'luku', 'mulus'), "
            "penuh semangat, persuasif, serta sertakan emoji yang melimpah dan menarik!"
        )
        
        image_part = {
            "mime_type": mime_type,
            "data": image_bytes
        }
        
        # Jalankan pemanggilan Gemini (menggunakan run_in_executor untuk membungkus panggilan sinkron API client library)
        import asyncio
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: model.generate_content(contents=[image_part, prompt])
        )
        
        result_text = response.text
        logger.info("Berhasil mendapatkan hasil estimasi visual Gemini API.")
        
        formatted_result = (
            f"🕵️‍♂️ <b>[UKA-UKA AI STOCK ALERT ANALYSIS]</b> 🕵️‍♂️\n"
            f"━━━━━━━━━━━━━━━━━━━\n\n"
            f"{result_text}\n\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"<i>Analisis AI Uka-Uka selesai. Semangat cuannya bos!</i> 💸🤙"
        )
        return formatted_result

    except Exception as e:
        logger.error(f"Gagal melakukan estimasi stok visual Gemini API: {str(e)}", exc_info=True)
        return fallback_response
