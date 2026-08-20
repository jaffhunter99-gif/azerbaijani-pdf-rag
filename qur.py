"""qur.py — PDF → təmizlə → parçala → embed → Chroma. BİR DƏFƏ işlədilir."""

import re

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from ayarlar import (PDF_FAYLI, BAZA_QOVLUGU, EMBED_MODELI,
                     PARCA_OLCUSU, PARCA_ORTUSU)

sened = PyPDFLoader(PDF_FAYLI).load()
print("Səhifə sayı:", len(sened))

# pypdf sözlərin arasına tab qoyur — təmizlənməsə axtarış pozulur
for s in sened:
    s.page_content = re.sub(r"[ \t]+", " ", s.page_content)

bolucu = RecursiveCharacterTextSplitter(chunk_size=PARCA_OLCUSU,
                                        chunk_overlap=PARCA_ORTUSU)
parcalar = bolucu.split_documents(sened)
print("Parça sayı:", len(parcalar))

embed = HuggingFaceEmbeddings(model_name=EMBED_MODELI)
Chroma.from_documents(parcalar, embed, persist_directory=BAZA_QOVLUGU)
print("Baza hazırdır.")