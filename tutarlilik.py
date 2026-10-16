import csv
import time
from difflib import SequenceMatcher
from itertools import combinations
from llm import sor
from prompts import PROMPTLAR
from test_metinleri import TEST_METINLERI

TEKRAR = 3
SECILEN = ["T1", "T3", "T4"]  # 3 metin yeterli
MOD = "Özetle"


def benzerlik(a, b):
    """İki metnin karakter bazında benzerliği (0 = hiç, 1 = birebir aynı)."""
    return SequenceMatcher(None, a, b).ratio()


with open("tutarlilik.csv", "w", newline="", encoding="utf-8-sig") as dosya:
    yazici = csv.writer(dosya)
    yazici.writerow(["test_id", "surum", "ortalama_benzerlik", "cikti_1", "cikti_2", "cikti_3"])

    for test in TEST_METINLERI:
        if test["id"] not in SECILEN:
            continue
        for surum in ("v1", "v2"):
            ciktilar = []
            for i in range(TEKRAR):
                print(f"{test['id']} | {surum} | tekrar {i+1}/{TEKRAR}")
                ciktilar.append(sor(PROMPTLAR[MOD][surum], test["metin"]))
                time.sleep(4)

            ikililer = list(combinations(ciktilar, 2))  # (1,2) (1,3) (2,3)
            ort = sum(benzerlik(a, b) for a, b in ikililer) / len(ikililer)
            yazici.writerow([test["id"], surum, round(ort, 2), *ciktilar])
            print(f"   -> ortalama benzerlik: {ort:.2f}")

print("\n✅ Bitti! Sonuçlar: tutarlilik.csv")