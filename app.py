import streamlit as st
from llm import sor
from prompts import PROMPTLAR

st.set_page_config(page_title="Metin Özetleyici", page_icon="📝", layout="wide")

# ---------- YAN MENÜ (ayarlar) ----------
st.sidebar.header("⚙️ Ayarlar")
surum = st.sidebar.radio(
    "Prompt sürümü",
    ["v3", "v2", "v1"],
    help="v1: basit ilk prompt, v2: geliştirilmiş prompt, v3: v2 + dil ve uzunluk kuralları",
)
sicaklik = st.sidebar.slider(
    "Sıcaklık (temperature)", 0.0, 1.0, 0.3, 0.1,
    help="Düşük: daha tutarlı, yüksek: daha yaratıcı",
)
karsilastir = st.sidebar.checkbox("🔍 Sürümleri yan yana karşılaştır")
secilenler = ["v1", "v2"]
if karsilastir:
    secilenler = st.sidebar.multiselect(
        "Karşılaştırılacak sürümler", ["v1", "v2", "v3"], default=["v1", "v2"],
        help="2 veya 3 sürüm seçin",
    )

st.sidebar.divider()
st.sidebar.warning(
    "**Dikkat:** Kişisel veya gizli bilgi girmeyin. "
    "Metin işlenmek üzere Google Gemini API'ye gönderilir. "
    "Yapay zekâ hata yapabilir; sonucu orijinal metinle kontrol edin."
)

# ---------- ANA SAYFA ----------
st.title("📝 LLM Tabanlı Metin Özetleme ve Yeniden Yazma")
st.caption("Metninizi yapıştırın, ne yapmak istediğinizi seçin.")

mod = st.selectbox("Ne yapılsın?", list(PROMPTLAR.keys()))
metin = st.text_area("Metniniz", height=250, placeholder="Metni buraya yapıştırın...")
st.caption(f"{len(metin)} karakter · {len(metin.split())} kelime")


def goster(baslik, sonuc):
    """Sonucu ekrana basar; hata mesajıysa kırmızı gösterir."""
    st.subheader(baslik)
    if sonuc.startswith(("⚠️", "❌")):
        st.error(sonuc)
    else:
        st.markdown(sonuc)
        st.caption(f"{len(sonuc.split())} kelime")


if st.button("✨ Çalıştır", type="primary"):
    if karsilastir:
        ACIKLAMA = {"v1": "basit prompt", "v2": "geliştirilmiş prompt", "v3": "dil + uzunluk kuralları"}
        secilenler = sorted(secilenler)
        if len(secilenler) < 2:
            st.warning("Karşılaştırma için en az 2 sürüm seçin.")
            st.stop()
        with st.spinner(", ".join(secilenler) + " çalıştırılıyor..."):
            sonuclar = {s: sor(PROMPTLAR[mod][s], metin, sicaklik) for s in secilenler}
        for sutun, s in zip(st.columns(len(secilenler)), secilenler):
            with sutun:
                goster(f"{s} ({ACIKLAMA[s]})", sonuclar[s])
    else:
        with st.spinner("Model çalışıyor..."):
            sonuc = sor(PROMPTLAR[mod][surum], metin, sicaklik)
        sol, sag = st.columns(2)
        with sol:
            st.subheader("Orijinal metin")
            st.write(metin)
            st.caption(f"{len(metin.split())} kelime")
        with sag:
            goster(f"Sonuç ({mod}, {surum})", sonuc)
        if not sonuc.startswith(("⚠️", "❌")):
            st.download_button("⬇️ Sonucu indir (.txt)", sonuc, file_name="sonuc.txt")