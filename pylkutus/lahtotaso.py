"""Lähtötasot (PLAN_PILKKU.md luku 5, 7.3/V2).

(a) vanha pilkut.py: sen check_line ajetaan kappaleelle, ja varoituksen token muunnetaan
    offsetiksi. Sääntö "loppupilkku" jätetään pois, koska se ei osoita paikkaa.
(b) sanalista: sidesana, relatiivisana tai kysymyssana ilman edeltävää pilkkua.
"""
from __future__ import annotations

import importlib.util
import os
import re

from .tyypit import Varoitus

VANHA = os.path.expanduser("~/Documents/ratkaisu/pilkut.py")
_vanha = None


def _lataa_vanha():
    global _vanha
    if _vanha is None:
        spec = importlib.util.spec_from_file_location("pilkut_vanha", VANHA)
        _vanha = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_vanha)
    return _vanha


def vanha(teksti: str) -> list[Varoitus]:
    m = _lataa_vanha()
    tulos: list[Varoitus] = []
    alku = 0
    for kappale in teksti.split("\n\n"):
        osumat = list(m.TOKEN.finditer(kappale))
        kaapatut = []
        alkuperainen = m.warn
        m.warn = lambda out, lineno, conf, rule, msg, toks, i, sug: kaapatut.append((conf, rule, msg, i))
        try:
            m.check_line(0, kappale, [])
        finally:
            m.warn = alkuperainen
        nahty = set()
        for conf, rule, msg, i in kaapatut:
            if rule == "loppupilkku" or i in nahty:
                continue
            nahty.add(i)
            o = alku + osumat[i].start()
            tulos.append(Varoitus(f"vanha/{rule}", conf, o, o, "lisaa", msg))
        alku += len(kappale) + 2
    return tulos


# --- (b) sanalista -----------------------------------------------------------

SANA = re.compile(r"\w+(?:[-–]\w+)*|[^\w\s]")
ALISTUS = {"että", "jotta", "koska", "kun", "kunnes", "jos", "vaikka", "jollei", "ellei",
           "kunhan", "mikäli", "ettei", "jottei", "jotteivät"}
RELATIIVI = {"joka", "jotka", "jonka", "joiden", "jota", "joita", "jossa", "joissa", "josta",
             "joista", "johon", "joihin", "jolla", "joilla", "jolle", "joille", "jolta",
             "joilta", "jona", "joina", "joksi", "joiksi", "jolloin", "jonne", "joten",
             "jollainen", "jollaisia", "jollaista"}
RINNASTUS = {"ja", "tai", "sekä", "eli", "vai", "mutta", "vaan", "eikä", "sillä"}
# moniosaisen ilmauksen alkuosat (1.2): jos jokin näistä on edellä, pilkku sen eteen riittää
MONIOSAINEN = {"heti", "sitten", "samalla", "aina", "silloin", "niin", "siten", "ilman",
               "jälkeen", "sijaan", "huolimatta", "lisäksi", "aikaa", "mukaa", "vasta",
               "varsinkin", "etenkin", "juuri", "paitsi"}
JOKA_JOKAINEN = {"kerta", "kerran", "päivä", "päivän", "ilta", "illan", "aamu", "aamun",
                 "viikko", "viikon", "vuosi", "vuoden", "hetki", "hetken", "ikinen", "ainoa",
                 "ainoan", "kohdassa", "paikassa", "puolella", "puolelta", "tapauksessa",
                 "suhteessa", "askeleessa", "askeleen", "asiassa", "sana"}
TAKANA_EI_SIDESANA = {"tahansa", "hyvänsä", "ikinä", "vain"}


def sanalista(teksti: str) -> list[Varoitus]:
    tulos: list[Varoitus] = []
    tokenit = list(SANA.finditer(teksti))
    for n, m in enumerate(tokenit):
        w = m.group().lower()
        if w not in ALISTUS and w not in RELATIIVI:
            continue
        if n == 0:
            continue
        ed = tokenit[n - 1].group()
        if not ed[0].isalnum():
            continue                                   # pilkku tai muu merkki edellä
        seur = tokenit[n + 1].group().lower() if n + 1 < len(tokenit) else ""
        if ed.lower() in RINNASTUS or ed.lower() in ALISTUS or ed.lower() in RELATIIVI:
            continue                                   # S1b, S4
        if w == "joka" and seur in JOKA_JOKAINEN:
            continue                                   # 1.14 joka = jokainen
        if seur in TAKANA_EI_SIDESANA:
            continue
        kohta = n
        if ed.lower() in MONIOSAINEN:
            # pilkku riittää ilmauksen eteen (M1)
            k = n - 1
            while k > 0 and tokenit[k - 1].group().lower() in MONIOSAINEN | {"sen", "sitä", "siitä"}:
                k -= 1
            if k == 0 or not tokenit[k - 1].group()[0].isalnum():
                continue
            if tokenit[k - 1].group().lower() in RINNASTUS:
                continue                               # S1b: "ja aina kun"

            kohta = k
        saanto = "S1" if w in ALISTUS else "S2"
        o = tokenit[kohta].start()
        tulos.append(Varoitus(f"lista/{saanto}", "medium", o, o, "lisaa",
                              f"pilkku puuttuu ennen sanaa \"{tokenit[kohta].group()}\"?"))
    return tulos
