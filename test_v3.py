import csv
import time
from llm import sor
from prompts import PROMPTLAR
from test_metinleri import TEST_METINLERI

# Özetle modunda tüm metinler + İngilizce metin (T6) için diğer 3 mod
isler = [(t, "Özetle") for t in TEST_METINLERI]
isler += [(t, m) for t in TEST_METINLERI if t["id"] == "T6" for m in PROMPTLAR if m != "Özetle"]

with open("v3_sonuclar.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["test_id", "mod", "girdi_kelime", "cikti_kelime", "oran", "cikti"])
    for t, mod in isler:
        girdi = t["metin"].strip()
        cikti = sor(PROMPTLAR[mod]["v3"], girdi)
        g, c = len(girdi.split()), len(cikti.split())
        w.writerow([t["id"], mod, g, c, round(c / g, 2), cikti])
        print(f"{t['id']} | {mod} | oran: {c/g:.2f}")
        time.sleep(4)