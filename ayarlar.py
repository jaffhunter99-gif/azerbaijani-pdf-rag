"""
ayarlar.py — sistemin bütün sabitləri.
Səbəb: eyni ayar iki yerdə yazılsa, biri dəyişəndə sistem SƏSSİZ sınır.
Bu layihədə həmin səhv bir dəfə embedding modeli üstündə baş verib.
"""

PDF_FAYLI = "araz_logistika_telimat.pdf"
BAZA_QOVLUGU = "baza"

EMBED_MODELI = "BAAI/bge-m3"
CAVAB_MODELI = "openai/gpt-oss-120b"

PARCA_OLCUSU = 800
PARCA_ORTUSU = 150
TAPILAN_SAY = 4