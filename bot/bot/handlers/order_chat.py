import re
import logging
from telegram import Update
from telegram.ext import ContextTypes

from bot.services.backend_api import (
    fetch_products,
    fetch_product_by_name,
    create_order_api
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bot.order_chat")

async def order_chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Menangani pesan teks dengan format pencocokan instan: "Order [nama produk] - [nama] - [alamat]".
    Mempercepat pembeli untuk checkout barang thrift secara kilat lewat ketikan chat!
    """
    text = update.message.text.strip()
    
    # Regex untuk mendeteksi format: Order (produk) - (nama) - (alamat)
    pattern = r"^[Oo]rder\s+(.+?)\s*-\s*(.+?)\s*-\s*(.+)$"
    match = re.match(pattern, text)
    
    if not match:
        # Jika bukan format order, lewati saja agar ditangani handler lain
        return

    product_name_input = match.group(1).strip()
    buyer_name = match.group(2).strip()
    buyer_address = match.group(3).strip()
    
    logger.info(f"Menerima order chat instan: Produk={product_name_input}, Pembeli={buyer_name}, Alamat={buyer_address}")
    
    await update.message.reply_text("🔎 <i>Uka-Uka AI sedang memverifikasi stok barang di inventaris...</i>", parse_mode="HTML")
    
    # 1. Cari produk berdasarkan input nama di database backend
    product = await fetch_product_by_name(product_name_input)
    
    # 2. Jika produk tidak ditemukan / stok habis (stock == 0)
    if not product or product.get("stock", 0) < 1:
        logger.info(f"Produk '{product_name_input}' tidak tersedia atau stok habis. Mencari alternatif...")
        
        # Cari alternatif produk serupa
        all_products = await fetch_products()
        alternatives = []
        for p in all_products:
            if p.get("stock", 0) > 0 and p.get("isActive", True):
                # Jika brand atau kategori sama
                if (p.get("brand", "").lower() in product_name_input.lower() or 
                    p.get("category", "").lower() in product_name_input.lower()):
                    alternatives.append(p)
                    if len(alternatives) >= 2:
                        break
                        
        # Fallback jika tidak ada kategori/brand yang mirip, rekomendasikan 2 produk aktif acak
        if not alternatives:
            alternatives = [p for p in all_products if p.get("stock", 0) > 0 and p.get("isActive", True)][:2]

        # Susun pesan penolakan yang bersahabat
        not_found_msg = (
            f"❌ <b>Waduh sob, maaf banget!</b> Barang <code>{product_name_input}</code> "
            f"yang kamu cari saat ini sedang kosong atau sudah terjual (out of stock). 😭\n\n"
        )
        
        if alternatives:
            not_found_msg += "🔥 <b>Tapi tenang, Uka-Uka AI punya rekomendasi barang skena yang gak kalah gokil buat kamu:</b>\n"
            for alt in alternatives:
                not_found_msg += (
                    f"• 📦 <b>{alt.get('brand')} - {alt.get('name')}</b>\n"
                    f"  💰 Harga: Rp{int(alt.get('price', 0)):,}\n"
                    f"  ⭐ Kondisi: {alt.get('condition')}/5\n"
                    f"  💡 <i>Ketik: Order {alt.get('name')} - {buyer_name} - {buyer_address}</i>\n\n"
                )
        else:
            not_found_msg += "💡 <i>Katalog kami sedang direstock oleh owner. Pantau terus ya sob!</i>"
            
        await update.message.reply_text(not_found_msg, parse_mode="HTML")
        return

    # 3. Jika produk ada dan stok tersedia (stock > 0), proses pembuatan order di backend
    product_id = product.get("id")
    price = float(product.get("price", 0.0))
    buyer_phone = str(update.effective_user.id)  # Menggunakan Telegram User ID sebagai nomor kontak default
    
    order = await create_order_api(
        product_id=product_id,
        buyer_name=buyer_name,
        buyer_phone=buyer_phone,
        buyer_address=buyer_address,
        amount=price
    )
    
    if not order:
        await update.message.reply_text(
            "⚠️ <b>Waduh sob, terjadi gangguan teknis saat membuat pesanan.</b> "
            "Silakan coba sesaat lagi atau hubungi admin ya!",
            parse_mode="HTML"
        )
        return

    # 4. Generate URL Link Pembayaran Midtrans Snap
    # Backend orders mengembalikan paymentToken yang disimulasikan / Snap asli
    payment_token = order.get("paymentToken", "")
    # Susun snap link URL sandbox/production
    payment_url = f"https://app.sandbox.midtrans.com/snap/v2/vtweb/{payment_token}"
    
    # 5. Kirim tagihan invoice & CTA pembayaran
    success_msg = (
        f"🎉 <b>ORDER BERHASIL DIBUAT! SIKAT SOB!</b> 🎉\n"
        f"━━━━━━━━━━━━━━━━━━━\n\n"
        f"🛍️ <b>Barang:</b> {product.get('brand')} - {product.get('name')}\n"
        f"💰 <b>Total Tagihan:</b> Rp{int(price):,}\n"
        f"👤 <b>Nama Penerima:</b> {buyer_name}\n"
        f"📍 <b>Alamat Kirim:</b> {buyer_address}\n"
        f"📌 <b>Order ID:</b> <code>{order.get('id')}</code>\n\n"
        f"👇 <b>Klik tautan di bawah untuk pembayaran instan (E-Wallet/Bank/QRIS):</b>\n"
        f"🔗 <a href='{payment_url}'>BAYAR TAGIHAN SEKARANG</a>\n\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"⚠️ <i>Setelah transfer, harap unggah/kirim foto bukti transfer ke chat bot ini ya untuk konfirmasi otomatis. Mantap!</i> 🤙"
    )
    
    await update.message.reply_text(success_msg, parse_mode="HTML", disable_web_page_preview=True)
