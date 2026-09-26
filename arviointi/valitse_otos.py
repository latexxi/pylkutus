"""Valitsee kultaisen otoksen kappaleet leipätekstistä (siemenluku kiinnitetty).

Käyttö: python arviointi/valitse_otos.py LAHDE.md > arviointi/kulta/otos.txt
Kappaleen edellä kommenttirivi: % rivi N (lähdetiedoston rivinumero).
"""
import random
import sys

from pylkutus.esikasittelija import lue_md

SIEMEN = 2026
KOKO = 50
MINIMIPITUUS = 200

with open(sys.argv[1], encoding="utf-8") as f:
    leipa, _ = lue_md(f.read())
ehdokkaat = [(a, b) for a, b in leipa.kappaleet if b - a >= MINIMIPITUUS]
otos = random.Random(SIEMEN).sample(ehdokkaat, KOKO)
print(f"% Kultainen otos: {KOKO} kappaletta, siemen {SIEMEN}, vähintään {MINIMIPITUUS} merkkiä.")
print("% Merkinnät: [+,] pakollinen puuttuu, [-,] ylimääräinen, [?,] valinnainen puuttuu,")
print("% [?-,] olemassa oleva valinnainen. Perään sääntö, esim. [+,S1].")
for n, (a, b) in enumerate(otos, 1):
    print()
    print(f"% {n:02d} rivi {leipa.rivi_sarake(a)[0]}")
    print(leipa.teksti[a:b])
