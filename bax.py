"""
bax.py — diaqnoz aləti.
Sualı bazadakı parçalarla tutuşdurub oxşarlıq balına görə sıralayır.
Beləliklə "düz parça neçənci sıradadır və modelə çatırmı?" sualına baxmaq olur.
Bal = məsafə → KİÇİK olan daha yaxındır.
"""

from ayarlar import TAPILAN_SAY
from bot import baza

sual = input("Sual: ")

neticeler = baza.similarity_search_with_score(sual, k=20)

for i, (parca, bal) in enumerate(neticeler, 1):
    isare = "  ← MODELƏ GEDİR" if i <= TAPILAN_SAY else ""
    print(f"\n--- {i}  bal={bal:.3f}{isare} ---")
    print(parca.page_content[:200].replace("\n", " "))