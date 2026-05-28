import base64
import logging
from fastapi import APIRouter, File, UploadFile, HTTPException, status

from app.ai_service import analyze_product_image

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app.api.v1.ai")

router = APIRouter(prefix="/ai", tags=["AI Services"])

@router.post("/analyze-product", status_code=status.HTTP_200_OK)
async def analyze_product_via_image(
    file: UploadFile = File(..., description="Foto produk streetwear/thrift yang ingin dianalisis AI Uka-Uka")
):
    """
    FastAPI Endpoint: Menerima unggahan foto produk dari kamera/galeri ponsel owner,
    mengekstraksi data visual secara asinkron menggunakan Gemini AI multimodal,
    dan mengembalikan estimasi brand, kategori, warna, grade kondisi, serta tahun rilis.
    """
    logger.info(f"Menerima request analisis produk AI via gambar. Filename: {file.filename}")

    # 1. Validasi ekstensi berkas
    allowed_extensions = ["png", "jpg", "jpeg", "webp"]
    file_ext = file.filename.split(".")[-1].lower() if "." in file.filename else ""
    if file_ext not in allowed_extensions:
        logger.warning(f"File ditolak karena ekstensi tidak valid: {file_ext}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Format file tidak didukung. Silakan unggah foto berformat PNG, JPG, atau WEBP."
        )

    try:
        # 2. Baca data bytes gambar secara asinkron
        image_bytes = await file.read()
        
        # 3. Konversi menjadi string base64 untuk dikirim ke modul Gemini API
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        
        # 4. Panggil modul AI Service Uka-Uka
        # Ini akan memanggil Gemini API dan mengembalikan JSON terstruktur
        analysis_result = analyze_product_image(image_base64)
        
        logger.info(f"Hasil analisis AI untuk {file.filename}: {analysis_result}")
        return analysis_result

    except Exception as e:
        logger.error(f"Gagal melakukan pemrosesan gambar di endpoint AI: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Terjadi kegagalan pemrosesan AI internal: {str(e)}"
        )
