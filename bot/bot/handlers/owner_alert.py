import os
import logging
from telegram import Update
from telegram.ext import ContextTypes

from bot.services.ai_helper import estimate_stock_from_photo

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bot.owner_alert")

def _is_message_from_owner(update: Update) -> bool:
    """
    Memeriksa apakah pengirim pesan adalah owner bisnis berdasarkan TELEGRAM_CHAT_ID.
    """
    owner_chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not owner_chat_id:
        logger.warning("TELEGRAM_CHAT_ID tidak dikonfigurasi di environment. Akses ditolak secara default.")
        return False
        
    return str(update.effective_chat.id) == str(owner_chat_id)

async def stock_alert_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Menangani perintah /stockalert dari owner bisnis.
    Meminta owner untuk mengunggah foto tumpukan stok baju baru.
    """
    # 1. Autentikasi owner
    if not _is_message_from_owner(update):
        await update.message.reply_text(
            "❌ <b>Akses Ditolak!</b>\n"
            "Perintah /stockalert ini khusus hanya untuk owner bisnis Uka-Uka ya sob! 🤙",
            parse_mode="HTML"
        )
        return

    # 2. Instruksi unggah foto
    instruction = (
        "📦 <b>UKA-UKA AI VISUAL STOCK ESTIMATOR</b> 📦\n"
        "━━━━━━━━━━━━━━━━━━━\n\n"
        "Halo bos! Siap restock barang skena terbaru nih?\n"
        "Yuk kirimkan <b>foto tumpukan pakaian baru</b> kamu kesini untuk diestimasi kuantitasnya oleh AI!\n\n"
        "💡 <i>(Unggah fotomu dengan menulis caption perintah <code>/stockalert</code> atau cukup kirim "
        "fotonya setelah mengetik perintah ini)</i>"
    )
    await update.message.reply_text(instruction, parse_mode="HTML")
    # Set state sederhana di user_data untuk menandai kita menunggu foto restock
    context.user_data["waiting_for_restock_photo"] = True

async def owner_stock_photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Menangani unggahan foto tumpukan baju ketika state waiting_for_restock_photo aktif atau di caption termuat /stockalert.
    Memanggil model Gemini multimodal asinkron untuk analisis visual.
    """
    # 1. Verifikasi pengirim adalah owner
    if not _is_message_from_owner(update):
        return
        
    # Cek state atau caption
    caption = update.message.caption or ""
    is_waiting = context.user_data.get("waiting_for_restock_photo", False)
    
    if not (is_waiting or "/stockalert" in caption):
        # Jika bukan stock alert, lewati agar diproses handler pembeli (seperti bukti transfer)
        return

    # Reset state
    context.user_data.pop("waiting_for_restock_photo", None)
    
    logger.info(f"Owner {update.effective_user.id} mengunggah foto untuk estimasi stok visual restock.")
    
    await update.message.reply_text(
        "🕵️‍♂️ <i>Uka-Uka AI sedang mengamati foto dan menghitung lipatan pakaian di tumpukan baju Anda...</i>",
        parse_mode="HTML"
    )
    
    # 2. Unduh file foto resolusi tinggi
    photo_file = await update.message.photo[-1].get_file()
    
    try:
        file_bytes = await photo_file.download_as_bytearray()
        
        # 3. Panggil fungsi estimasi stok visual Gemini API
        analysis_result = await estimate_stock_from_photo(bytes(file_bytes))
        
        # 4. Kirim hasil estimasi kembali ke owner
        await update.message.reply_text(analysis_result, parse_mode="HTML")
        
    except Exception as e:
        logger.error(f"Gagal memproses foto tumpukan stok owner: {str(e)}", exc_info=True)
        await update.message.reply_text(
            "⚠️ <b>Waduh bos, terjadi galat teknis saat menganalisis foto.</b> "
            "Harap pastikan GEMINI_API_KEY telah diatur dan coba lagi ya!",
            parse_mode="HTML"
        )
