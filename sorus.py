from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq

load_dotenv()

embed = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")

baza = Chroma(persist_directory="baza", embedding_function=embed)

model = ChatGroq(model="openai/gpt-oss-120b", temperature=0)

sual = input("Sual: ")

tapilanlar = baza.similarity_search(sual, k=4)
kontekst = "\n\n".join(p.page_content for p in tapilanlar)

prompt = f"""Aşağıdakı mətnə əsaslanaraq suala cavab ver.
Cavab mətndə yoxdursa, "Sənəddə bu barədə məlumat yoxdur" yaz. Uydurma

MƏTN:
{kontekst}

SUAL: {sual}"""

cavab = model.invoke(prompt)
print("\nCAVAB:", cavab.content)

print("\n--- MƏNBƏ ---")
for p in tapilanlar:
    print(f"[səhifə {p.metadata['page'] + 1}] {p.page_content[:120]}...")