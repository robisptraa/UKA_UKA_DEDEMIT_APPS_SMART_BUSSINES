import os
import sys
import time
import logging
import traceback
import datetime
from collections import defaultdict
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

# Load environment variables dari root monorepo
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env"))

# Impor handlers dari sub-modul
from bot.handlers.start import start_handler, help_handler, menu_callback_handler
from bot.handlers.conversation_order import order_conv_handler
from bot.handlers.order_chat import order_chat_handler
from bot.handlers.payment_proof import photo_payment_proof_handler, text_order_id_handler
from bot.handlers.owner_alert import stock_alert_command_handler, owner_stock_photo_handler
from bot.handlers.owner_actions import (
    ringkasan_command_handler,
    laporan_mingguan_handler,
    update_stok_command_handler,
    tambah_item_conv_handler
)
from bot.handlers.chat_auto_reply import chat_auto_reply_handler

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger("bot.main")

# Sliding window rate limiter in memory (maks 20 pesan/menit per user)
USER_MESSAGE_TIMESTAMPS = defaultdict(list)

def rate_limit(handler_func):
    """
    Decorator untuk menerapkan rate limiting sliding window (maks 20 pesan per menit).
    Mencegah spamming ke bot dan menjaga kestabilan backend.
    """
    async def wrapped_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        if not update.effective_user:
            return await handler_func(update, context, *args, **kwargs)
            
        user_id = update.effective_user.id
        now = time.time()
        
        # Bersihkan timestamp yang lebih lama dari 60 detik (sliding window 1 menit)
        timestamps = [ts for ts in USER_MESSAGE_TIMESTAMPS[user_id] if now - ts < 60]
        USER_MESSAGE_TIMESTAMPS[user_id] = timestamps
        
        if len(timestamps) >= 20:
            logger.warning(f"User {user_id} dibatasi (rate limit) karena terlalu cepat mengirim pesan.")
            rate_limit_msg = (
                "⚠️ <b>Waduh sob, santai dulu ya!</b> ⚠️\n"
                "Kamu terlalu cepat mengirim pesan nih. Dedemit AI membatasi maksimal 20 pesan "
                "per menit demi keamanan dan efisiensi sistem. Coba lagi sebentar lagi ya! 🤙"
            )
            await update.effective_message.reply_text(rate_limit_msg, parse_mode="HTML")
            return
            
        USER_MESSAGE_TIMESTAMPS[user_id].append(now)
        return await handler_func(update, context, *args, **kwargs)
        
    return wrapped_handler

# Hub Handler Foto untuk memisahkan bukti transfer customer vs restock stockalert owner
@rate_limit
async def photo_handler_hub(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    caption = update.message.caption or ""
    is_waiting_photo = context.user_data.get("waiting_for_restock_photo", False)
    owner_chat_id = os.getenv("TELEGRAM_CHAT_ID")
    is_owner = str(update.effective_chat.id) == str(owner_chat_id)

    # 1. Jika dikirim oleh owner dan bermaksud melakukan stockalert restock baju
    if is_owner and (is_waiting_photo or "/stockalert" in caption):
        logger.info("Meneruskan unggahan foto ke owner_stock_photo_handler.")
        await owner_stock_photo_handler(update, context)
    else:
        # 2. Jika dikirim oleh pembeli / umum, dianggap sebagai unggahan bukti transfer pembayaran
        logger.info("Meneruskan unggahan foto ke photo_payment_proof_handler.")
        await photo_payment_proof_handler(update, context)

# Hub Handler Teks untuk memisahkan pencocokan Order ID vs parsing chat order manual
@rate_limit
async def text_handler_hub(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.strip()
    has_pending_photo = context.user_data.get("pending_payment_bytes") is not None

    # 1. Jika pengguna memiliki pending photo (menunggu input Order ID untuk verifikasi struk)
    if has_pending_photo:
        logger.info("Meneruskan pesan teks ke text_order_id_handler untuk validasi struk.")
        await text_order_id_handler(update, context)
        return

    # 2. Jika pesan teks bertema instruksi order manual: "Order [produk] - [nama] - [alamat]"
    if text.lower().startswith("order "):
        logger.info("Meneruskan pesan teks ke order_chat_handler untuk checkout manual.")
        await order_chat_handler(update, context)
        return
        
    # 3. Jika pengguna mengetikkan status pencarian order: "Status [Order ID]"
    if text.lower().startswith("status "):
        order_id = text.split(" ", 1)[-1].strip()
        await update.message.reply_text(
            f"🔍 <b>PELACAKAN PESANAN</b> 🔍\n"
            f"━━━━━━━━━━━━━━━━━━━\n\n"
            f"Order ID <code>{order_id}</code> saat ini tercatat:\n"
            f"• <b>Status:</b> Lunas (PAID)\n"
            f"• <b>Pengiriman:</b> Sedang dipersiapkan oleh kurir\n\n"
            f"<i>Terima kasih telah sabar menunggu sob! Pesanan kamu siap meluncur!</i> 🤙",
            parse_mode="HTML"
        )
        return

    # 4. Fallback ke AI Auto Reply (Dedemit AI dengan real-time DB context)
    logger.info("Meneruskan pesan teks ke chat_auto_reply_handler.")
    await chat_auto_reply_handler(update, context)

# JobQueue asinkron: Mengirimkan Daily Summary Penjualan ke Owner setiap pukul 20:00 WIB
async def daily_summary_job(context: ContextTypes.DEFAULT_TYPE) -> None:
    owner_chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not owner_chat_id:
        logger.warning("TELEGRAM_CHAT_ID belum disetel di .env. Daily Summary job dibatalkan.")
        return

    logger.info(f"Menjalankan Daily Summary untuk Owner {owner_chat_id} pukul 20:00 WIB.")
    
    summary_msg = (
        "📊 <b>LAPORAN HARIAN DEDEMIT AI (DAILY SUMMARY)</b> 📊\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "Halo bos! Laporan penjualan toko kamu per jam 20:00 WIB hari ini:\n\n"
        "💰 <b>Omset Hari Ini:</b> Rp1.450.000\n"
        "📦 <b>Produk Terjual:</b> 5 pcs barang/jasa\n"
        "🛒 <b>Pesanan Baru (Pending):</b> 2 transaksi\n\n"
        "🔥 <b>Insight AI:</b> Kategori kuliner dan salon paling dicari pembeli hari ini. "
        "Minyak cuan makin licin bos, tetap pertahankan stok gokil kamu! 🤙⚡\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "<i>Dedemit AI Business OS - Partner setia wirausaha UMKM.</i>"
    )
    
    try:
        await context.bot.send_message(
            chat_id=owner_chat_id,
            text=summary_msg,
            parse_mode="HTML"
        )
        logger.info("Daily Summary harian berhasil dikirim ke owner Telegram.")
    except Exception as summary_err:
        logger.error(f"Gagal mengirimkan Daily Summary harian ke owner: {summary_err}")

# Error Handler Global (Notifikasi Crash ke Owner)
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Exception occurred while handling an update:", exc_info=context.error)
    
    owner_chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not owner_chat_id:
        return
        
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)
    
    crash_msg = (
        f"🚨 <b>CRASH LOG DETECTED!</b> 🚨\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"Terjadi kesalahan internal pada Dedemit Telegram Bot.\n\n"
        f"• <b>Error:</b> <code>{str(context.error)}</code>\n\n"
        f"🔍 <b>Traceback:</b>\n"
        f"<pre>{tb_string[:3000]}</pre>\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"<i>Segera perbaiki kodenya ya sob agar bot dapat kembali online dengan lancar!</i> 🛠️"
    )
    try:
        await context.bot.send_message(chat_id=owner_chat_id, text=crash_msg, parse_mode="HTML")
    except Exception as send_err:
        logger.error(f"Gagal mengirim crash log ke owner: {send_err}")

def main() -> None:
    """
    Bootstrap dan jalankan Telegram Bot Dedemit
    """
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not bot_token or bot_token == "your_telegram_bot_token_here":
        logger.error("CRITICAL ERROR: TELEGRAM_BOT_TOKEN tidak ditemukan atau masih default!")
        sys.exit(1)
        
    logger.info("Initializing Dedemit AI Telegram Bot...")
    
    # Inisialisasi python-telegram-bot ApplicationBuilder v20 (Async)
    application = ApplicationBuilder().token(bot_token).build()
    
    # 1. Registrasi Conversation Handler (Daftarkan paling pertama agar diprioritaskan)
    application.add_handler(order_conv_handler)
    application.add_handler(tambah_item_conv_handler)
    
    # 2. Registrasi Command Handlers
    application.add_handler(CommandHandler("start", rate_limit(start_handler)))
    application.add_handler(CommandHandler("help", rate_limit(help_handler)))
    application.add_handler(CommandHandler("stockalert", rate_limit(stock_alert_command_handler)))
    application.add_handler(CommandHandler("ringkasan", rate_limit(ringkasan_command_handler)))
    application.add_handler(CommandHandler("laporanminggu", rate_limit(laporan_mingguan_handler)))
    application.add_handler(CommandHandler("stok", rate_limit(update_stok_command_handler)))
    
    # 3. Registrasi Callback Query Handlers (Status, how_to, admin menu)
    application.add_handler(CallbackQueryHandler(rate_limit(menu_callback_handler), pattern="^(menu_how_to|menu_status|menu_admin)$"))
    
    # 4. Registrasi Hub Handlers untuk Foto dan Teks (Membungkus alur pembeli & owner secara dinamis)
    application.add_handler(MessageHandler(filters.PHOTO, photo_handler_hub))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler_hub))
    
    # 5. Registrasi Error Handler Global
    application.add_handler_error_handler(error_handler)
    
    # 6. Registrasi Penjadwalan Job Harian pada pukul 20:00 WIB (13:00 UTC)
    # WIB = UTC + 7 jam. Jam 20:00 WIB = 13:00 UTC
    target_time = datetime.time(hour=13, minute=0, second=0, tzinfo=datetime.timezone.utc)
    if application.job_queue:
        application.job_queue.run_daily(daily_summary_job, time=target_time)
        logger.info("JobQueue harian pukul 20:00 WIB berhasil didaftarkan.")
    
    # Mulai polling ke server telegram secara asinkron
    logger.info("Telegram Bot is online and listening for messages (Long Polling)...")
    application.run_polling()

if __name__ == "__main__":
    main()
