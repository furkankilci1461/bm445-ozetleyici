from llm import sor
from prompts import PROMPTLAR

ORNEK_METIN = """
Yapay zekâ, bilgisayar sistemlerinin insan zekâsı gerektiren görevleri yerine
getirebilmesini amaçlayan bir bilim dalıdır. 1956 yılında Dartmouth Konferansı'nda
ilk kez bir araştırma alanı olarak tanımlanmıştır. Günümüzde makine öğrenmesi ve
derin öğrenme yöntemleri sayesinde görüntü tanıma, doğal dil işleme ve otonom
araçlar gibi alanlarda büyük ilerlemeler kaydedilmiştir. Ancak bu teknolojilerin
yaygınlaşması; veri gizliliği, önyargı ve istihdam üzerindeki etkiler gibi
etik tartışmaları da beraberinde getirmiştir.
"""

for mod, surumler in PROMPTLAR.items():
    print("=" * 60)
    print(f"MOD: {mod}")
    for surum in ["v1", "v2"]:
        print(f"\n--- {surum} ---")
        print(sor(surumler[surum], ORNEK_METIN))