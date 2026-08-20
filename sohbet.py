"""sohbet.py — söhbət rejimi. Bütün məntiq bot.py-dadır."""

from bot import cavab_al

tarixce = []

while True:
    sual = input("\nSual (çıxmaq üçün q): ")
    if sual.strip().lower() == "q":
        break

    cavab = cavab_al(sual, tarixce, goster=True)
    print("\nCAVAB:", cavab)

    tarixce.append(("İstifadəçi", sual))
    tarixce.append(("Bot", cavab))