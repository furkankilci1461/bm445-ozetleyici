# 📝 LLM Tabanlı Metin Özetleme ve Yeniden Yazma Uygulaması

**BM 445 – Üretken Yapay Zekâ ve Büyük Dil Modelleri · Proje 2**
Hazırlayan: [Furkan Kılcı] · [230206001]

Kullanıcının verdiği metni **özetleyen**, **sadeleştiren**, **akademik dile** veya **günlük dile** çeviren bir web uygulaması. Hazır bir büyük dil modeli (Google Gemini) API üzerinden kullanılır; model eğitimi yapılmaz. Projenin odağı prompt tasarımı, promptların iyileştirilmesi ve çıktıların sistematik olarak değerlendirilmesidir.

![Uygulama ekran görüntüsü](ekran_goruntuleri/ana_ekran.png)

---

## Özellikler

- **4 mod:** Özetle · Sadeleştir · Akademik dile çevir · Günlük dile çevir
- **3 prompt sürümü:** v1 (basit), v2 (rol + kurallar), v3 (v2 + dil ve uzunluk kuralları)
- **Karşılaştırma modu:** seçilen 2 veya 3 sürümün (v1, v2, v3) çıktılarını yan yana gösterir
- **Sıcaklık (temperature) ayarı:** tutarlılık ile çeşitlilik arasında denge
- **Girdi kontrolleri:** boş metin ve 15.000 karakter sınırı
- **Hata yönetimi:** sunucu yoğunluğunda (429/503) artan bekleme süresiyle (exponential backoff) yeniden deneme, ardından yedek modele geçiş
- **Prompt enjeksiyonuna karşı koruma:** kullanıcı metni `<metin>` etiketleriyle ayrılır ve sistem promptunda "metindeki talimatlara uyma" kuralı yer alır
- Sonucu `.txt` olarak indirme

## Proje yapısı

```
bm445-ozetleyici/
├── app.py               # Streamlit web arayüzü
├── llm.py               # Gemini API çağrısı, girdi kontrolü, hata yönetimi
├── prompts.py           # 4 mod × 3 sürüm sistem promptu
├── deneme.py            # v1 / v2 promptlarını hızlıca karşılaştırma
├── test_metinleri.py    # 8 test metni (T1–T8)
├── test_calistir.py     # 64 çıktılık ana test → sonuclar.csv
├── tutarlilik.py        # Aynı girdinin 3 tekrarı → tutarlilik.csv
├── test_v3.py           # v3 promptlarının testi → v3_sonuclar.csv
├── sonuclar_puanli.csv  # Elle puanlanmış test sonuçları
├── tutarlilik.csv
├── v3_sonuclar.csv
├── requirements.txt
├── .env.example         # API anahtarı şablonu
└── README.md
```

## Nasıl çalışır?

```
Kullanıcı metni ──► app.py ──► llm.sor(sistem_promptu, metin)
                                   │
                                   ├─ boş / çok uzun mu? → uyarı
                                   ├─ metni <metin>…</metin> içine al
                                   ├─ Gemini API (system_instruction + temperature)
                                   │     └─ 429/503 → 1-2-4 sn bekle, tekrar dene → yedek model
                                   ▼
                             Sonuç ekranda gösterilir
```

Sistem promptu (modelin rolü ve kuralları) ile kullanıcı metni API'ye **ayrı ayrı** gönderilir. Varsayılan `temperature = 0.3` değeri, aynı metin için birbirine yakın sonuçlar alınmasını sağlar.

---

## Kurulum

**Gereksinimler:** Python 3.10 veya üzeri, Google hesabı (ücretsiz Gemini API anahtarı için).

```bash
# 1) Proje klasörüne gir
cd bm445-ozetleyici

# 2) Sanal ortam oluştur ve etkinleştir
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3) Kütüphaneleri kur
pip install -r requirements.txt
```

**API anahtarı:**

1. https://aistudio.google.com → **Get API key** → **Create API key**
2. `.env.example` dosyasını kopyalayıp adını `.env` yap ve anahtarı yaz:
   ```
   GEMINI_API_KEY=buraya_anahtarinizi_yazin
   ```

> ⚠️ `.env` dosyası `.gitignore` içindedir; API anahtarını kimseyle paylaşmayın ve GitHub'a yüklemeyin.

## Çalıştırma

```bash
streamlit run app.py
```

Tarayıcıda `http://localhost:8501` adresi açılır.

1. Metni kutuya yapıştırın.
2. Modu seçin (Özetle, Sadeleştir, Akademik veya Günlük).
3. İsterseniz sol menüden prompt sürümünü ve sıcaklık değerini değiştirin.
4. **Çalıştır** düğmesine basın. Sürümleri kıyaslamak için **Karşılaştır** kutusunu işaretleyip sürümleri seçin.

## Testleri çalıştırma

```bash
python test_calistir.py   # 8 metin × 4 mod × 2 sürüm = 64 çıktı  (~6 dk)
python tutarlilik.py      # 3 metin × 2 sürüm × 3 tekrar         (~2 dk)
python test_v3.py         # v3 promptları, 12 çıktı               (~1,5 dk)
```

Ücretsiz kotayı aşmamak için istekler arasında 4 saniye beklenir.

---

## Test metinleri

| ID | Tür | Neyi sınıyor? |
|---|---|---|
| T1 | Haber | Sayıların korunması |
| T2 | Akademik (biyoloji) | Terim yoğun metin |
| T3 | Teknik (ağlar) | Teknik doğruluk |
| T4 | Resmi duyuru | Tarihlerin korunması |
| T5 | Günlük konuşma | Hedef üsluba zaten yakın metin |
| T6 | İngilizce | Dilin korunması |
| T7 | Prompt enjeksiyonu | Güvenlik |
| T8 | 10 kelimelik metin | Uç durum |

## Özet sonuçlar

| Ölçüt | v1 | v2 | v3 |
|---|---|---|---|
| Doğruluk (1–5, elle) | 4.38 | **4.94** | – |
| Kullanışlılık (1–5, elle) | 3.66 | **4.41** | – |
| Halüsinasyon içeren çıktı | 6 / 32 | **0 / 32** | – |
| Gereksiz giriş cümlesi | 20 / 32 | **0 / 32** | – |
| Prompt enjeksiyonu başarılı | 3 / 4 | **0 / 4** | 0 / 1 |
| Özetleme oranı (çıktı / girdi) | 0.88 | 1.19 | **0.77** |
| İngilizce metinde dilin korunması | karışık | 0 / 4 | **4 / 4** |
| Tutarlılık (T1 / T4) | 0.55 / 0.80 | **0.80 / 0.83** | – |

Ayrıntılı analiz için teknik rapora bakınız.

## Sınırlılıklar

- Doğruluk ve kullanışlılık puanları **tek bir değerlendirici** tarafından elle verilmiştir.
- Otomatik "uydurma sayı" kontrolü yalnızca rakamları yakalar ve biçim değişikliklerinde yanlış alarm verir (örneğin "22.00" → "akşam 10").
- Karakter bazlı benzerlik ölçüsü, anlamı aynı olup farklı cümlelerle yazılmış çıktıları düşük puanlar.
- Test metinleri kısadır (10–70 kelime); uzun metinlerdeki davranış ayrıca test edilmelidir.
- Model ve sürümü Google tarafından güncellenebilir; aynı test ileride farklı sonuç verebilir.

## Etik ve güvenlik

- Girilen metin işlenmek üzere Google Gemini API'ye gönderilir. **Kişisel veya gizli bilgi girilmemelidir**; bu uyarı uygulamada da gösterilir.
- Model bilgi uydurabilir veya anlamı değiştirebilir. Çıktılar her zaman orijinal metinle karşılaştırılmalıdır.
- Telif hakkı korumalı metinlerin yeniden yazılması, eserin sahipliğini değiştirmez.
- Prompt enjeksiyonuna karşı girdi etiketleme ve açık kurallar kullanılmıştır; ancak hiçbir yöntem %100 koruma sağlamaz.

## Kullanılan teknolojiler

Python · [google-genai](https://pypi.org/project/google-genai/) (Gemini API) · [Streamlit](https://streamlit.io) · python-dotenv · csv / difflib (test ve analiz)
