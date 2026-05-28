import logging
from telegram import Update
from telegram.ext import ContextTypes

from bot.services.backend_api import validate_payment_proof_api

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bot.payment_proof")

async def photo_payment_proof_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Menangani unggahan foto bukti pembayaran (struk transfer) dari pembeli.
    Menyimpan file foto sementara dan meminta pembeli memasukkan Order ID.
    """
    logger.info(f"Menerima unggahan foto bukti pembayaran dari User ID: {update.effective_user.id}")
    
    # 1. Dapatkan file foto dengan resolusi tertinggi
    photo_file = await update.message.photo[-1].get_file()
    
    try:
        # Download foto menjadi bytes di memori (tidak menulis ke disk)
        file_bytes = await photo_file.download_as_bytearray()
        
        # 2. Simpan bytes foto sementara di context.user_data pembeli
        context.user_data["pending_payment_bytes"] = bytes(file_bytes)
        context.user_data["pending_payment_filename"] = f"proof_{update.effective_user.id}.jpg"
        
        logger.info("Foto bukti transfer berhasil diunduh dan disimpan sementara di user_data.")
        
        # 3. Minta pembeli untuk memasukkan Order ID transaksi
        request_msg = (
            "🕵️‍♂️ <b>Dedemit AI mendeteksi struk bukti transfer!</b> 🕵️‍♂️\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"
            "Wah hebat Kak! Untuk memproses verifikasi otomatis secara instan, "
            "harap <b>balas/ketikkan Order ID</b> pesanan Kakak sekarang ya:\n\n"
            "👉 <i>(Ketik langsung ke chat bot ini, contoh: ORD-xxxx atau salin ID dari invoice)</i>"
        )
        await update.message.reply_text(request_msg, parse_mode="HTML")
        
    except Exception as e:
        logger.error(f"Gagal mengunduh foto bukti transfer: {str(e)}", exc_info=True)
        await update.message.reply_text(
            "⚠️ <b>Waduh Kak, gagal memproses foto bukti transfer.</b> "
            "Harap pastikan koneksi internet Kakak stabil dan coba kirim ulang ya!",
            parse_mode="HTML"
        )

async def text_order_id_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Menangani pesan teks yang berisi Order ID ketika ada foto bukti transfer tertunda di user_data.
    Melakukan panggilan ke API Backend untuk validasi OCR otomatis.
    """
    text = update.message.text.strip()
    
    # Cek apakah ada file foto bukti transfer yang sedang tertunda di user_data
    file_bytes = context.user_data.get("pending_payment_bytes")
    filename = context.user_data.get("pending_payment_filename", "proof.jpg")
    
    # Jika tidak ada foto tertunda, abaikan
    if not file_bytes:
        return

    # Kita asumsikan input teks ini adalah Order ID
    order_id = text
    logger.info(f"Memproses Order ID '{order_id}' untuk validasi foto yang tertunda.")
    
    await update.message.reply_text(
        "🔎 <i>Dedemit AI sedang membaca OCR struk transfer dan mencocokkan nominal belanja Kakak... Mohon tunggu.</i>",
        parse_mode="HTML"
    )
    
    # Panggil API validasi bukti transfer asinkron di backend
    result = await validate_payment_proof_api(
        order_id=order_id,
        file_bytes=file_bytes,
        filename=filename
    )
    
    # Bersihkan memori file tertunda di user_data agar tidak berulang
    context.user_data.pop("pending_payment_bytes", None)
    context.user_data.pop("pending_payment_filename", None)
    
    if not result:
        await update.message.reply_text(
            "⚠️ <b>Maaf Kak, validasi gagal karena tidak dapat menghubungi server backend.</b> "
            "Harap pastikan Order ID sudah benar, atau silakan kirim ulang struk fotonya.",
            parse_mode="HTML"
        )
        return
        
    # Ambil hasil validasi dari response backend (format camelCase dari schema)
    is_valid = result.get("isValid", False)
    extracted_amount = result.get("extractedAmount", 0.0)
    extracted_sender = result.get("extractedSender", "Unknown")
    extracted_bank = result.get("extractedBank", "Unknown")
    
    # Jika bukti transfer valid
    if is_valid:
        success_msg = (
            f"✅ <b>PEMBAYARAN TERKONFIRMASI LUNAS!</b> ✅\n"
            f"━━━━━━━━━━━━━━━━━━━\n\n"
            f"Status pesanan Kakak untuk Order ID <code>{order_id}</code> telah berhasil "
            f"diperbarui menjadi <b>Lunas (PAID)</b>! 💰\n\n"
            f"👤 <b>Pengirim:</b> {extracted_sender}\n"
            f"🏦 <b>Bank/Wallet:</b> {extracted_bank}\n"
            f"💰 <b>Nominal Terbaca:</b> Rp {extracted_amount:,.0f}\n"
            f"📦 <i>Owner toko telah kami beritahu secara otomatis dan barang sedang dipersiapkan untuk dikirim/diberikan!</i>\n\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"👻 <i>Terima kasih banyak telah berbelanja di Dedemit UMKM! Sukses selalu usahanya!</i> 👍"
        )
        await update.message.reply_text(success_msg, parse_mode="HTML")
    else:
        # Jika tidak valid
        fail_msg = (
            f"❌ <b>BUKTI BAYAR TIDAK COCOK / KURANG JELAS!</b> ❌\n"
            f"━━━━━━━━━━━━━━━━━━━\n\n"
            f"Mohon maaf Kak, pembayaran untuk Order ID <code>{order_id}</code> gagal kami konfirmasi otomatis.\n\n"
            f"⚠️ <b>Kemungkinan Penyebab:</b> Nominal transfer tidak sesuai dengan jumlah tagihan belanja, atau gambar struk buram/terpotong.\n\n"
            f"💡 <b>Solusi:</b>\n"
            f"1. Pastikan foto struk memiliki pencahayaan cukup dan nominal angka terlihat sangat jelas.\n"
            f"2. Kirim/unggah kembali foto struk transfer baru ke bot ini untuk mencoba kembali."
        )
        await update.message.reply_text(fail_msg, parse_mode="HTML")
