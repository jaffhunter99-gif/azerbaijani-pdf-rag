"""
test.py — Praktika 2 üçün sadə evaluation.
Botu bot.py-dan götürür — yəni söhbət rejimi ilə EYNİ kodu yoxlayır.
İşlətmək: py test.py   (əvvəlcə qur.py işlədilmiş olmalıdır)
"""

import time

from bot import cavab_al

# Hər testdə "gozlenilen" siyahısının HƏR elementi cavabda olmalıdır.
# Bir elementin içindəki "|" = alternativlər, biri kifayətdir.
TESTLER = [
    {"ad": "Sadə fakt",
     "sual": "Xırdalan anbarı axşam saat neçədə bağlanır?",
     "gozlenilen": ["20:00"]},

    {"ad": "Oxşar bölmə — qaytarma ilə qarışdırmır",
     "sual": "Dəyişdirmə sorğusu neçə gün ərzində verilməlidir?",
     "gozlenilen": ["14"]},

    {"ad": "Hesablama",
     "sual": "Gəncəyə 4 kq bağlama neçəyə başa gəlir?",
     "gozlenilen": ["12.6|12,6"]},

    {"ad": "Hərf səhvi ilə sual",
     "sual": "xirdlan anbari axsam necde baglanir",
     "gozlenilen": ["20:00"]},

    {"ad": "Fərqli sözlərlə — sinonim",
     "sual": "paketi itirseler mene nə qədər pul verirler",
     "gozlenilen": ["80", "500"]},

    {"ad": "Uydurma yoxlaması — sənəddə olmayan fakt",
     "sual": "Gəncədə filial varmı?",
     "gozlenilen": ["yox|deyil|olunmayıb"]},

    {"ad": "Ardıcıl söhbət — kontekstsiz sual",
     "hazirliq": "Xırdalan anbarı neçədə açılır?",
     "sual": "Bəs bağlanır?",
     "gozlenilen": ["20:00"]},

    {"ad": "MƏLUM PROBLEM — sığorta nüansı",
     "sual": "Sığorta xidməti neçəyə başa gəlir?",
     "gozlenilen": ["2"],
     "qadagan": ["kompensasiya"]},
]


def yoxla(cavab, gozlenilen, qadagan):
    metn = cavab.lower()
    for qrup in gozlenilen:
        if not any(alt.lower() in metn for alt in qrup.split("|")):
            return False, f"tapılmadı → {qrup}"
    for soz in qadagan:
        if soz.lower() in metn:
            return False, f"olmamalıydı → {soz}"
    return True, ""


kecen = 0

for i, t in enumerate(TESTLER, 1):
    tarixce = []
    if "hazirliq" in t:
        ilk = cavab_al(t["hazirliq"])
        tarixce = [("İstifadəçi", t["hazirliq"]), ("Bot", ilk)]

    cavab = cavab_al(t["sual"], tarixce)
    ugur, sebeb = yoxla(cavab, t["gozlenilen"], t.get("qadagan", []))

    print(f"\n[{i}] {t['ad']}")
    print(f"    Sual  : {t['sual']}")
    print(f"    Cavab : {cavab.strip()[:150]}")
    print(f"    {'✅ KEÇDİ' if ugur else '❌ KEÇMƏDİ — ' + sebeb}")

    if ugur:
        kecen += 1

    time.sleep(3)

print(f"\n{'=' * 50}")
print(f"NƏTİCƏ: {kecen}/{len(TESTLER)} keçdi")