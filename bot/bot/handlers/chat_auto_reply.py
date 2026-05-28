import logging
import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ContextTypes

from bot.services.backend_api import fetch_products

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bot.chat_auto_reply")

# Konfigurasi Gemini API untuk Bot
bot_gemini_api_key = os.getenv("GEMINI_API_KEY")
if bot_gemini_api_key:
    genai.configure(api_key=bot_gemini_api_key)
    logger.info("Gemini API berhasil dikonfigurasi pada Telegram Bot.")

async def chat_auto_reply_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Menangani pesan teks bebas dari pelanggan.
    Mencari informasi produk/toko dan menjawab secara otomatis menggunakan Gemini AI.
    """
    message_text = update.message.text.strip()
    logger.info(f"Menerima pesan dari pelanggan: {message_text}")

    # 1. Tarik info katalog terupdate sebagai context untuk Gemini
    products = await fetch_products()
    products_context = []
    for p in products:
        stock_str = f"stok {p.get('stock')}" if p.get("stock") is not None else "tipe Jasa/Service"
        products_context.append(f"- {p.get('name')}: Harga Rp {p.get('price'):,.0f} ({stock_str}), Kategori: {p.get('category')}")
        
    products_info = "\n".join(products_context) if products_context else "Saat ini katalog sedang kosong."

    # 2. Bangun context toko lengkap
    store_context = (
        f"Konteks Bisnis:\n"
        f"• Nama Toko: Dedemit UMKM\n"
        f"• Deskripsi: AI Business OS untuk seluruh UMKM Indonesia\n"
        f"• Jam Operasional: Setiap hari pukul 08:00 - 20:00 WIB\n"
        f"• Lokasi Toko: Jl. Merdeka No. 10, Bandung, Jawa Barat\n"
        f"• Kontak Dukungan Admin: @dedemit_support_bot\n"
        f"• Katalog Tersedia:\n{products_info}"
    )

    fallback_response = (
        "🤖 <b>Dedemit AI di sini!</b> 👻\n\n"
        "Halo Kak! Untuk pertanyaan tentang produk, pemesanan, atau lokasi, "
        "bisa ditanyakan langsung di sini ya. Jika butuh bantuan manusia, "
        "silakan ketuk tombol <b>Hubungi Kami</b> di `/start` untuk berkontak dengan admin kami di @dedemit_support_bot! 👍"
    )

    if not bot_gemini_api_key:
        await update.message.reply_text(fallback_response, parse_mode="HTML")
        return

    # 3. Panggil Gemini AI
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        prompt = (
            "Kamu adalah Dedemit AI — asisten bisnis UMKM Indonesia yang cerdas, ramah, dan praktis.\n"
            "Tugasmu adalah menjawab chat pertanyaan pembeli secara ramah, profesional, dan to-the-point.\n\n"
            f"{store_context}\n\n"
            f"Pertanyaan Pembeli: \"{message_text}\"\n\n"
            "Aturan Jawaban:\n"
            "1. Jawab HANYA menggunakan informasi tertera pada konteks di atas. Jika tidak ada di konteks, jawab dengan sopan bahwa Anda tidak tahu dan arahkan mereka untuk menghubungi admin cs di @dedemit_support_bot.\n"
            "2. Gunakan bahasa Indonesia yang santai khas wirausaha lokal dengan emoji yang cocok.\n"
            "3. Jangan bertele-tele."
        )
        
        response = model.generate_content(contents=prompt)
        await update.message.reply_text(response.text.strip(), parse_mode="HTML")
    except Exception as e:
        logger.error(f"Gagal memanggil Gemini di Auto-Reply: {str(e)}")
        await update.message.reply_text(fallback_response, parse_mode="HTML")
