import logging
import httpx
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bot.start")

BACKEND_API_URL = "http://localhost:8000/api/v1"

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Menangani perintah /start dari pengguna.
    Menyambut pengguna dan menyajikan menu utama interaktif bertema Dedemit UMKM.
    """
    user_first_name = update.effective_user.first_name
    
    welcome_message = (
        f"👻 <b>Halo {user_first_name}! Selamat datang di Dedemit UMKM</b> 👻\n"
        f"━━━━━━━━━━━━━━━━━━━\n\n"
        f"Saya adalah <b>Dedemit AI</b> — asisten bisnis UMKM Indonesia yang cerdas, ramah, dan praktis! ⚡\n\n"
        f"Di sini, Kakak bisa langsung melihat menu/katalog usaha, melakukan pemesanan instan, "
        f"mengecek status pesanan secara real-time, hingga mengonfirmasi pembayaran bukti transfer otomatis!\n\n"
        f"👇 <i>Silakan ketuk salah satu menu di bawah ini untuk memulai:</i>"
    )

    # Inisialisasi menu tombol Inline Keyboard utama
    keyboard = [
        [
            InlineKeyboardButton("🛍️ Lihat Produk/Menu", callback_data="menu_products"),
        ],
        [
            InlineKeyboardButton("📋 Cara Order", callback_data="menu_how_to"),
            InlineKeyboardButton("📦 Cek Pesanan", callback_data="menu_status")
        ],
        [
            InlineKeyboardButton("📞 Hubungi Kami", callback_data="menu_admin")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        text=welcome_message,
        parse_mode="HTML",
        reply_markup=reply_markup
    )

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Menangani perintah /help dengan menyajikan panduan interaksi bot Dedemit UMKM.
    """
    help_text = (
        "💡 <b>PANDUAN DEDEMIT UMKM BOT</b> 💡\n"
        "━━━━━━━━━━━━━━━━━━━\n\n"
        "• <b>Pemesanan Menu/Produk (Checkout):</b>\n"
        "  Ketuk menu <b>🛍️ Lihat Produk/Menu</b> di `/start` atau ketik `/order` untuk mulai memesan secara interaktif.\n\n"
        "• <b>Pemesanan Kilat via Chat:</b>\n"
        "  Kakak juga bisa memesan langsung via chat dengan format:\n"
        "  <code>Order [Nama Produk] - [Nama Kakak] - [Nomor HP] - [Alamat]</code>\n"
        "  <i>Contoh: Order Nasi Rendang - Andi - 0812345678 - Jl. Merdeka 10 Bandung</i>\n\n"
        "• <b>Konfirmasi Struk Transfer (Pembayaran Manual):</b>\n"
        "  Cukup kirimkan foto struk transfer pembayaran ke chat bot ini, asisten AI kami akan memverifikasi OCR nominal secara instan!\n\n"
        "• <b>Pelacakan Status Pesanan:</b>\n"
        "  Ketik <code>/cekpesanan [Order ID]</code> untuk melihat status pemesanan Kakak secara langsung.\n\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "👻 <i>Ada pertanyaan lain? Ketik langsung ke chat, Dedemit AI siap menjawab otomatis!</i>"
    )
    await update.message.reply_text(text=help_text, parse_mode="HTML")

async def menu_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Menangani interaksi klik tombol menu utama inline callback query.
    """
    query = update.callback_query
    await query.answer()
    
    data = query.data
    logger.info(f"Menerima callback menu klik: {data}")

    if data == "menu_how_to":
        how_to_text = (
            "📋 <b>CARA MUDAH MEMESAN DI DEDEMIT UMKM</b> 📋\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"
            "Kakak bisa berbelanja dengan 2 cara super cepat:\n\n"
            "🔥 <b>Cara 1: Belanja Interaktif (Rekomendasi)</b>\n"
            "1. Ketik perintah `/order` di chat bot ini.\n"
            "2. Pilih produk atau jasa yang diinginkan pada tombol menu yang muncul.\n"
            "3. Isi Nama, Nomor HP, dan Alamat Pengiriman Kakak.\n"
            "4. Kakak akan menerima link pembayaran Midtrans (QRIS/VA) untuk menyelesaikan pembayaran secara instan!\n\n"
            "⚡ <b>Cara 2: Ketik Chat Pemesanan Kilat</b>\n"
            "Kirim pesan langsung ke bot dengan format:\n"
            "<code>Order [Nama Barang] - [Nama Kakak] - [No HP] - [Alamat]</code>\n"
            "<i>(Contoh: Order Batik Solo - Dian - 08129999888 - Jl. Sudirman 5 Solo)</i>\n\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "👉 <i>Mudah banget kan? Yuk ketik `/order` sekarang untuk mencoba!</i>"
        )
        await query.message.reply_text(how_to_text, parse_mode="HTML")
        
    elif data == "menu_status":
        status_info_text = (
            "📦 <b>CEK STATUS PESANAN</b> 📦\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"
            "Kakak ingin melacak pesanan belanja secara real-time?\n\n"
            "👉 <b>Caranya gampang:</b>\n"
            "Cukup ketikkan perintah <code>/cekpesanan [Order ID]</code> Kakak ke bot ini!\n"
            "<i>(Contoh: /cekpesanan ORD-SUCCESS)</i>\n\n"
            "Dedemit AI akan mencarikan status invoice terbarunya langsung dari server database utama! ⚡"
        )
        await query.message.reply_text(status_info_text, parse_mode="HTML")
        
    elif data == "menu_admin":
        admin_text = (
            "📞 <b>HUBUNGI KAMI</b> 📞\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"
            "Ada kendala transaksi, ingin koreksi alamat kirim, atau butuh bantuan admin? Kami siap melayani!\n\n"
            "Hubungi customer service kami di:\n"
            "• 📱 <b>WhatsApp:</b> +62 812-3456-7890\n"
            "• 💬 <b>Telegram Support:</b> @dedemit_support_bot\n"
            "• 📧 <b>Email:</b> support@dedemit.id\n\n"
            "<i>Jam Operasional Layanan Pelanggan: 08:00 - 20:00 WIB.</i>"
        )
        await query.message.reply_text(admin_text, parse_mode="HTML")
        
    elif data == "menu_products":
        # Mengambil katalog produk dari backend asinkron
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{BACKEND_API_URL}/items?is_active=true", timeout=10.0)
                if response.status_code == 200:
                    items = response.json()
                    if not items:
                        await query.message.reply_text("📭 <i>Saat ini belum ada produk/jasa terdaftar di katalog kami.</i>", parse_mode="HTML")
                        return
                        
                    await query.message.reply_text("🛍️ <b>KATALOG PRODUK & JASA</b> 🛍️\n━━━━━━━━━━━━━━━━━━━")
                    for item in items:
                        price_fmt = f"Rp {item.get('price', 0):,.0f}"
                        stock_fmt = f"{item.get('stock')} {item.get('unit')}" if item.get("stock") is not None else "Jasa/Service"
                        
                        detail_msg = (
                            f"📌 <b>{item.get('name')}</b>\n"
                            f"• Kategori: {item.get('category')}\n"
                            f"• Tipe: {item.get('type').upper()}\n"
                            f"• Stok: {stock_fmt}\n"
                            f"• Harga: <b>{price_fmt}</b>\n"
                            f"• Deskripsi: {item.get('description', '-')}\n\n"
                            f"👉 Ketik `/order` untuk memesan item ini!"
                        )
                        
                        # Tampilkan foto jika ada URL
                        if item.get("imageUrl"):
                            try:
                                await query.message.reply_photo(photo=item.get("imageUrl"), caption=detail_msg, parse_mode="HTML")
                            except Exception:
                                await query.message.reply_text(detail_msg, parse_mode="HTML")
                        else:
                            await query.message.reply_text(detail_msg, parse_mode="HTML")
                else:
                    await query.message.reply_text("⚠️ <i>Gagal memuat katalog. Server database backend sedang offline.</i>", parse_mode="HTML")
        except Exception as e:
            logger.error(f"Error fetching catalog: {str(e)}")
            await query.message.reply_text("⚠️ <i>Gagal memuat katalog karena kendala jaringan.</i>", parse_mode="HTML")
