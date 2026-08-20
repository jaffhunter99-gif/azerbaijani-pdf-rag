"""
bot.py — sistemin özəyi.
Baza, model və cavab məntiqi burada yaşayır ki,
sohbet.py və test.py eyni koddan istifadə etsin.
"""

import time

from dotenv import load_dotenv
from groq import RateLimitError
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from ayarlar import BAZA_QOVLUGU, EMBED_MODELI, CAVAB_MODELI, TAPILAN_SAY

load_dotenv()

embed = HuggingFaceEmbeddings(model_name=EMBED_MODELI)
baza = Chroma(persist_directory=BAZA_QOVLUGU, embedding_function=embed)
model = ChatGroq(model=CAVAB_MODELI, temperature=0)

def invoke_et(prompt, cehd=4):
    """Groq-un dəqiqəlik token limitinə (TPM) dəyəndə gözləyib yenidən cəhd edir."""
    for i in range(cehd):
        try:
            return model.invoke(prompt).content
        except RateLimitError:
            gozle = 10 * (i + 1)
            print(f"    ⏳ limit doldu — {gozle} saniyə gözlənilir...")
            time.sleep(gozle)
    raise RuntimeError("Rate limit 4 cəhddən sonra da keçmədi")


def cavab_al(sual, tarixce=None, goster=False):
    """Bir sual → (lazım olsa) sualı tam hala sal → axtar → cavab yaz."""
    tarixce = tarixce or []
    kecmis = "\n".join(f"{rol}: {metn}" for rol, metn in tarixce[-6:])

    if tarixce:
        yaz_prompt = f"""Aşağıda söhbət tarixçəsi və yeni sual var.
Yeni sualı, tarixçəyə baxmadan da anlaşılan, tam sual halına gətir.
Yalnız yenidən yazılmış sualı qaytar, başqa heç nə yazma.

TARİXÇƏ:
{kecmis}

YENİ SUAL: {sual}"""
        axtaris_sualı = invoke_et(yaz_prompt).strip()
        if goster:
            print(f"[axtarış: {axtaris_sualı}]")
    else:
        axtaris_sualı = sual

    tapilanlar = baza.similarity_search(axtaris_sualı, k=TAPILAN_SAY)
    kontekst = "\n\n".join(p.page_content for p in tapilanlar)

    prompt = f"""Aşağıdakı mətnə əsaslanaraq suala cavab ver.
Cavab mətndə yoxdursa, "Sənəddə bu barədə məlumat yoxdur" yaz. Uydurma.

ƏVVƏLKİ SÖHBƏT:
{kecmis}

MƏTN:
{kontekst}

SUAL: {sual}"""

    return invoke_et(prompt)