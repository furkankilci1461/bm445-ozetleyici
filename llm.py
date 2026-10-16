import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types, errors

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODELLER = ["gemini-flash-latest", "gemini-flash-lite-latest"]
MAKS_KARAKTER = 15000  # çok uzun metinleri engellemek için


def sor(sistem_promptu, metin, sicaklik=0.3):
    """Modele sistem promptu + kullanıcı metnini gönderir, cevabı döndürür."""
    metin = metin.strip()
    if not metin:
        return "⚠️ Lütfen bir metin girin."
    if len(metin) > MAKS_KARAKTER:
        return f"⚠️ Metin çok uzun ({len(metin)} karakter). En fazla {MAKS_KARAKTER} karakter girin."

    # Kullanıcı metnini etiketler arasına koyuyoruz (girdi tasarımı)
    icerik = f"<metin>\n{metin}\n</metin>"

    ayarlar = types.GenerateContentConfig(
        system_instruction=sistem_promptu,
        temperature=sicaklik,  # düşük = daha tutarlı, yüksek = daha yaratıcı
    )

    for model_adi in MODELLER:
        for deneme in range(3):
            try:
                cevap = client.models.generate_content(
                    model=model_adi, contents=icerik, config=ayarlar
                )
                return cevap.text
            except errors.APIError as e:
                if e.code in (429, 500, 503):
                    time.sleep(2 ** deneme)
                else:
                    return f"❌ API hatası ({e.code}): {e.message}"
    return 