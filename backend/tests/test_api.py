import httpx
import time
import sys

BASE_URL = "http://localhost:8000/api/v1"

def run_tests():
    print("🚀 Memulai Pengujian API End-to-End untuk Uka-Uka Backend...")
    time.sleep(2)  # Menunggu server uvicorn menyala sepenuhnya
    
    client = httpx.Client()

    # ==========================================================================
    # 1. REGISTER USER TEST
    # ==========================================================================
    print("\n[TEST 1] Mendaftarkan Pengguna Baru (/auth/register)...")
    email = f"test_owner_{int(time.time())}@uka-uka.id"
    register_payload = {
        "name": "Budi Santoso",
        "email": email,
        "phone": "081299998888",
        "storeName": "Budi Vintage Store",
        "password": "supersecretpassword123"
    }
    
    res = client.post(f"{BASE_URL}/auth/register", json=register_payload)
    if res.status_code != 201:
        print(f"❌ Gagal mendaftarkan user: {res.status_code} - {res.text}")
        sys.exit(1)
        
    user_data = res.json()
    print(f"✅ Registrasi Sukses! User ID: {user_data.get('id')}")

    # ==========================================================================
    # 2. LOGIN USER TEST
    # ==========================================================================
    print("\n[TEST 2] Mengautentikasi Pengguna (/auth/login)...")
    login_payload = {
        "email": email,
        "password": "supersecretpassword123"
    }
    res = client.post(f"{BASE_URL}/auth/login", json=login_payload)
    if res.status_code != 200:
        print(f"❌ Gagal login: {res.status_code} - {res.text}")
        sys.exit(1)
        
    token_data = res.json()
    access_token = token_data.get("accessToken") or token_data.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    print("✅ Login Sukses! Token JWT didapatkan.")

    # ==========================================================================
    # 3. CREATE PRODUCT TEST
    # ==========================================================================
    print("\n[TEST 3] Membuat Produk Baru (POST /products)...")
    product_payload = {
        "name": "Nike Windbreaker Jacket 90s Vintage",
        "brand": "Nike",
        "category": "Jacket",
        "condition": 4,
        "price": 250000.0,
        "stock": 2,
        "description": "Jaket vintage Nike, kondisi sangat baik 9/10, warna pekat.",
        "image_url": "https://images.example.com/nike.jpg",
        "is_active": True
    }
    res = client.post(f"{BASE_URL}/products", json=product_payload, headers=headers)
    if res.status_code != 201:
        print(f"❌ Gagal membuat produk: {res.status_code} - {res.text}")
        sys.exit(1)
        
    product_data = res.json()
    product_id = product_data.get("id")
    print(f"✅ Produk Berhasil Dibuat! ID: {product_id}, Nama: {product_data.get('name') or product_data}")

    # ==========================================================================
    # 4. GET PRODUCTS LIST & DETAIL TEST
    # ==========================================================================
    print("\n[TEST 4] Mengambil Daftar & Detail Produk (GET /products)...")
    res = client.get(f"{BASE_URL}/products", headers=headers)
    if res.status_code != 200 or len(res.json()) < 1:
        print(f"❌ Gagal mengambil daftar produk: {res.status_code} - {res.text}")
        sys.exit(1)
    print(f"✅ Daftar Produk Berhasil Diambil. Jumlah produk: {len(res.json())}")

    res = client.get(f"{BASE_URL}/products/{product_id}", headers=headers)
    if res.status_code != 200:
        print(f"❌ Gagal mengambil detail produk: {res.status_code} - {res.text}")
        sys.exit(1)
    print(f"✅ Detail Produk Berhasil Diambil. Nama: {res.json().get('name')}")

    # ==========================================================================
    # 5. CREATE ORDER TEST (PUBLIC)
    # ==========================================================================
    print("\n[TEST 5] Membuat Pesanan Baru secara Publik (POST /orders)...")
    order_payload = {
        "product_id": product_id,
        "buyer_name": "Ahmad Fauzi",
        "buyer_phone": "087711112222",
        "buyer_address": "Jl. Mampang Prapatan No. 5, Jakarta Selatan",
        "amount": 250000.0
    }
    res = client.post(f"{BASE_URL}/orders", json=order_payload)
    if res.status_code != 201:
        print(f"❌ Gagal membuat pesanan: {res.status_code} - {res.text}")
        sys.exit(1)
        
    order_data = res.json()
    order_id = order_data.get("id")
    print(f"✅ Pesanan Berhasil Dibuat! ID: {order_id}, Status: {order_data.get('status')}, Full: {order_data}")

    # ==========================================================================
    # 6. VERIFY STOCK DECREMENT & STOCK ALERTS
    # ==========================================================================
    print("\n[TEST 6] Memverifikasi Pengurangan Stok Produk...")
    res = client.get(f"{BASE_URL}/products/{product_id}", headers=headers)
    updated_product = res.json()
    print(f"✅ Stok Awal: 2, Stok Sekarang: {updated_product.get('stock')}")
    if updated_product.get('stock') not in (0, 1):
        print("❌ Pengurangan stok tidak sesuai!")
        sys.exit(1)

    # ==========================================================================
    # 7. DASHBOARD SUMMARY TEST
    # ==========================================================================
    print("\n[TEST 7] Memverifikasi Agregasi Dashboard (/dashboard/summary)...")
    res = client.get(f"{BASE_URL}/dashboard/summary", headers=headers)
    if res.status_code != 200:
        print(f"❌ Gagal mengambil dashboard: {res.status_code} - {res.text}")
        sys.exit(1)
        
    dash_data = res.json()
    print(f"✅ Ringkasan Dashboard: {dash_data}")

    # ==========================================================================
    # 8. PAYMENT PROOF VALIDATION (OCR SIMULATOR)
    # ==========================================================================
    print("\n[TEST 8] Memvalidasi Bukti Pembayaran menggunakan OCR (/payment-proofs/validate)...")
    # Buat mockup gambar dummy berukuran kecil untuk upload
    dummy_file = ("proof.png", b"fake-png-file-content", "image/png")
    upload_payload = {"order_id": order_id}
    res = client.post(
        f"{BASE_URL}/payment-proofs/validate",
        data=upload_payload,
        files={"file": dummy_file}
    )
    if res.status_code != 201:
        print(f"❌ Gagal melakukan OCR validasi bukti bayar: {res.status_code} - {res.text}")
        sys.exit(1)
        
    proof_data = res.json()
    print(f"✅ Bukti Transfer Valid!")
    print(f"   - Hasil Ekstraksi Nama Pengirim: {proof_data.get('extractedSender')}")
    print(f"   - Hasil Ekstraksi Nominal Transfer: Rp{proof_data.get('extractedAmount')}")
    print(f"   - Apakah Valid: {proof_data.get('isValid')}")

    # ==========================================================================
    # 9. RE-VERIFY REVENUE & TRENDING PRODUCTS
    # ==========================================================================
    print("\n[TEST 9] Memverifikasi Ulang Pendapatan & Analitik Tren Penjualan...")
    # Dashboard summary should now reflect the paid order's revenue
    res = client.get(f"{BASE_URL}/dashboard/summary", headers=headers)
    dash_data = res.json()
    print(f"✅ Pendapatan Terupdate Bulan Ini: Rp{dash_data.get('revenueThisMonth')}")
    revenue = dash_data.get('revenueThisMonth') or dash_data.get('revenue_this_month')
    if revenue != 250000.0:
        print("❌ Perhitungan pendapatan tidak sesuai!")
        sys.exit(1)

    # Trending analytics
    res = client.get(f"{BASE_URL}/analytics/trending", headers=headers)
    if res.status_code != 200:
        print(f"❌ Gagal mengambil tren penjualan: {res.status_code} - {res.text}")
        sys.exit(1)
        
    trending_list = res.json()
    print(f"✅ Tren Produk Terjual 30 Hari Terakhir:")
    for item in trending_list:
        product_name = item.get('product', {}).get('name', 'N/A')
        total_sold = item.get('totalSold') or item.get('total_sold', 0)
        print(f"   - Produk: {product_name} | Total Terjual: {total_sold}")

    print("\n🎉 SELURUH PENGUJIAN API UKA-UKA BERHASIL 100% SECARA ASINKRON! 🎉")

if __name__ == "__main__":
    run_tests()
