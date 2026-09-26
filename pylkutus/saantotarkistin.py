"""Moduuli 4: sääntötarkistin (PLAN_PILKKU.md 3.6, 7.3/V7)."""
from __future__ import annotations

from . import ajuri, jasennin
from .esikasittelija import lue_teksti
from .saannot import puuttuvat, sanasto, ylimaaraiset
from .tyypit import Leipateksti, Varoitus

VARMUUS = {"low": 0, "medium": 1, "high": 2}
# Säännöt, jotka on poistettu oletuksesta mittausten perusteella (arviointi/tulokset.md).
POIS_OLETUKSESTA: set[str] = set()


def _pilkun_offset(leipa_teksti: str, x: ajuri.Analyysi, rako: int) -> int:
    alku = x.a.tokenit[rako - 1].loppu
    loppu = x.a.tokenit[rako].alku if rako < len(x.a.tokenit) else alku + 2
    i = leipa_teksti.find(",", alku, loppu + 1)
    return i if i >= 0 else alku


def _viesti(koodi: str, toimenpide: str, sana: str) -> str:
    if toimenpide == "lisaa":
        return f'pilkku puuttuu ennen sanaa "{sana}" ({koodi})'
    return f'ylimääräinen pilkku ennen sanaa "{sana}" ({koodi})'


def tarkista_analyysi(x: ajuri.Analyysi, teksti: str, tyyli: bool = False) -> list[Varoitus]:
    """Yhden virkkeen varoitukset. Samasta raosta vain varmin varoitus."""
    parhaat: dict[tuple[int, str], Varoitus] = {}

    def lisaa(rako: int, koodi: str, pakko: str, varmuus: str, toimenpide: str):
        if koodi in POIS_OLETUKSESTA:
            return
        if pakko == "valinnainen" and not tyyli:
            return
        if pakko not in ("kyllä", "valinnainen"):
            return
        sana = x.a.tokenit[rako].teksti if rako < len(x.a.tokenit) else "∎"
        if toimenpide == "lisaa":
            o = x.a.tokenit[rako - 1].loppu
        else:
            o = _pilkun_offset(teksti, x, rako)
        v = Varoitus(koodi, varmuus, o, o + 1, toimenpide, _viesti(koodi, toimenpide, sana))
        avain = (rako, toimenpide)
        if avain not in parhaat or VARMUUS[varmuus] > VARMUUS[parhaat[avain].varmuus]:
            parhaat[avain] = v

    # puuttuvat: A:n rajat (B:n pelkät rajat eivät tuota varoitusta, ks. 3.6)
    paatetyt: dict[int, list[tuple[str, str, str]]] = {}
    for r in x.rajat:
        if r.lahde == "B" or r.rako == 0:
            continue
        p = puuttuvat.paata(x, r)
        if p:
            paatetyt.setdefault(r.rako, []).append(p)
    # sanastosäännöt lisäävät päätöksiä rakoihin, joissa jäsennys ei näe rajaa
    for saanto in sanasto.SAANNOT:
        for rako, koodi, pakko, varmuus in saanto(x):
            paatetyt.setdefault(rako, []).append((koodi, pakko, varmuus))
    for rako, paatokset in paatetyt.items():
        if x.a.rako[rako]:
            # pilkku paikalla: ylimääräinen, jos jokin sääntö kieltää eikä mikään vaadi
            kieltavat = [p for p in paatokset if p[1] == "ei" and p[0] != "1.15"]
            if kieltavat and not any(p[1] in ("kyllä", "valinnainen") for p in paatokset):
                p = max(kieltavat, key=lambda p: VARMUUS[p[2]])
                varmuus = {"high": "medium", "medium": "low", "low": "low"}[p[2]]
                lisaa(rako, p[0], "kyllä", varmuus, "poista")
            continue
        # jos jokin sääntö kieltää tai tekee valinnaiseksi, pakollista ei vaadita
        if any(p[1] == "ei" for p in paatokset):
            continue
        pakolliset = [p for p in paatokset if p[1] == "kyllä"]
        if pakolliset and not any(p[1] == "valinnainen" for p in paatokset):
            p = max(pakolliset, key=lambda p: VARMUUS[p[2]])
            lisaa(rako, p[0], "kyllä", p[2], "lisaa")
        elif paatokset:
            p = paatokset[0]
            lisaa(rako, p[0], "valinnainen", p[2], "lisaa")
    # M1: varoitus koko ilmauksen eteen
    # (puuttuvat.alkupilkku palauttaa M1/kyllä raon kohdalle; siirretään ilmauksen alkuun)
    for avain, v in list(parhaat.items()):
        if v.saanto == "M1" and v.toimenpide == "lisaa":
            rako = avain[0]
            m = puuttuvat.moniosainen(x, rako)
            if m is not None and m > 0:
                o = x.a.tokenit[m - 1].loppu
                sana = x.a.tokenit[m].teksti
                parhaat[avain] = Varoitus("M1", v.varmuus, o, o + 1, "lisaa",
                                          _viesti("M1", "lisaa", sana))
    # ylimääräiset
    for saanto in ylimaaraiset.SAANNOT:
        for rako, koodi, pakko, varmuus in saanto(x):
            lisaa(rako, koodi, "kyllä" if pakko == "ei" else pakko, varmuus, "poista")
    return sorted(parhaat.values(), key=lambda v: v.alku)


def tarkista(leipa: Leipateksti, analyysit: list[ajuri.Analyysi] | None = None,
             tyyli: bool = False) -> list[Varoitus]:
    analyysit = analyysit if analyysit is not None else ajuri.analysoi(leipa)
    tulos = []
    for x in analyysit:
        tulos.extend(tarkista_analyysi(x, leipa.teksti, tyyli))
    return tulos


def tarkista_teksti(teksti: str) -> list[Varoitus]:
    """Arviointia varten: tarkistaa valmiin leipätekstin (käyttää jäsennysvälimuistia)."""
    return tarkista(lue_teksti(teksti))
