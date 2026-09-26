"""Moduuli 4: sääntötarkistin (PLAN_PILKKU.md 3.6, 7.3/V7).

Säännöt tuottavat Paatos-olioita kahdessa perheessä:
- rakopäätökset (lauserajasäännöt ja sanastosäännöt): kuuluuko rakoon pilkku. Raon kaikki
  päätökset ratkaistaan yhdessä (`ratkaise`), ja tulos riippuu siitä, onko raossa jo pilkku.
- pilkkuhavainnot (ylimaaraiset.SAANNOT): olemassa oleva pilkku on ylimääräinen. Nämä eivät
  kumoa rakopäätöksiä, vaan kilpailevat niiden kanssa samasta raosta varmuuden perusteella.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator

from . import ajuri
from .esikasittelija import lue_teksti
from .saannot import puuttuvat, sanasto, ylimaaraiset
from .tyypit import Analyysi, Leipateksti, Paatos, Pakko, Varmuus, Varoitus

# Säännöt, jotka on poistettu oletuksesta mittausten perusteella (arviointi/tulokset.md).
POIS_OLETUKSESTA: set[str] = set()


@dataclass(frozen=True)
class Ehdotus:
    """Ratkaistu toimenpide yhteen rakoon."""
    koodi: str
    toimenpide: str          # lisaa | poista
    varmuus: Varmuus
    valinnainen: bool        # näytetään vain --tyyli-lipulla


def rakopaatokset(x: Analyysi) -> Iterator[Paatos]:
    for r in x.rajat:
        if r.rako:
            p = puuttuvat.paata(x, r)
            if p:
                yield p
    # sanastosäännöt lisäävät päätöksiä rakoihin, joissa jäsennys ei näe rajaa
    for saanto in sanasto.SAANNOT:
        yield from saanto(x)


def ratkaise(paatokset: list[Paatos], pilkku: bool) -> Ehdotus | None:
    """Yhden raon päätökset → toimenpide. Samanvarmuisista voittaa ensimmäinen."""
    kyllä_tai_valinnainen = any(p.pakko in (Pakko.KYLLA, Pakko.VALINNAINEN) for p in paatokset)
    if pilkku:
        # ylimääräinen, jos jokin sääntö kieltää eikä mikään vaadi; 1.15 ei kiellä pilkkua
        kieltavat = [p for p in paatokset if p.pakko == Pakko.EI and p.koodi != "1.15"]
        if kieltavat and not kyllä_tai_valinnainen:
            p = max(kieltavat, key=lambda p: p.varmuus.taso)
            return Ehdotus(p.koodi, "poista", p.varmuus.alennettu(), False)
        return None
    # jos jokin sääntö kieltää tai tekee valinnaiseksi, pakollista ei vaadita
    if any(p.pakko == Pakko.EI for p in paatokset):
        return None
    pakolliset = [p for p in paatokset if p.pakko == Pakko.KYLLA]
    if pakolliset and not any(p.pakko == Pakko.VALINNAINEN for p in paatokset):
        p = max(pakolliset, key=lambda p: p.varmuus.taso)
        return Ehdotus(p.koodi, "lisaa", p.varmuus, False)
    if paatokset:
        p = paatokset[0]
        return Ehdotus(p.koodi, "lisaa", p.varmuus, True)
    return None


def pilkkuhavainto(p: Paatos) -> Ehdotus | None:
    if p.pakko == Pakko.KYLLA:
        return None
    return Ehdotus(p.koodi, "poista", p.varmuus, p.pakko == Pakko.VALINNAINEN)


def _pilkun_offset(leipa_teksti: str, x: Analyysi, rako: int) -> int:
    alku = x.a.tokenit[rako - 1].loppu
    loppu = x.a.tokenit[rako].alku if rako < len(x.a.tokenit) else alku + 2
    i = leipa_teksti.find(",", alku, loppu + 1)
    return i if i >= 0 else alku


def _viesti(koodi: str, toimenpide: str, sana: str) -> str:
    if toimenpide == "lisaa":
        return f'pilkku puuttuu ennen sanaa "{sana}" ({koodi})'
    return f'ylimääräinen pilkku ennen sanaa "{sana}" ({koodi})'


def _varoitus(x: Analyysi, teksti: str, rako: int, e: Ehdotus) -> Varoitus:
    tt = x.a.tokenit
    if e.toimenpide == "poista":
        o = _pilkun_offset(teksti, x, rako)
    else:
        if e.koodi == "M1":
            # M1: varoitus koko moniosaisen ilmauksen eteen (heti kun → ", heti kun")
            m = puuttuvat.moniosainen(x, rako)
            if m is not None and m > 0:
                rako = m
        o = tt[rako - 1].loppu
    sana = tt[rako].teksti if rako < len(tt) else "∎"
    return Varoitus(e.koodi, e.varmuus, o, o + 1, e.toimenpide, _viesti(e.koodi, e.toimenpide, sana))


def tarkista_analyysi(x: Analyysi, teksti: str, tyyli: bool = False) -> list[Varoitus]:
    """Yhden virkkeen varoitukset. Samasta raosta ja toimenpiteestä vain varmin varoitus."""
    ehdotukset: list[tuple[int, Ehdotus]] = []
    raoittain: dict[int, list[Paatos]] = {}
    for p in rakopaatokset(x):
        raoittain.setdefault(p.rako, []).append(p)
    for rako, paatokset in raoittain.items():
        e = ratkaise(paatokset, bool(x.a.rako[rako]))
        if e:
            ehdotukset.append((rako, e))
    for saanto in ylimaaraiset.SAANNOT:
        for p in saanto(x):
            e = pilkkuhavainto(p)
            if e:
                ehdotukset.append((p.rako, e))

    parhaat: dict[tuple[int, str], tuple[int, Ehdotus]] = {}
    for rako, e in ehdotukset:
        if e.koodi in POIS_OLETUKSESTA or (e.valinnainen and not tyyli):
            continue
        avain = (rako, e.toimenpide)
        if avain not in parhaat or e.varmuus.taso > parhaat[avain][1].varmuus.taso:
            parhaat[avain] = (rako, e)
    varoitukset = [_varoitus(x, teksti, rako, e) for rako, e in parhaat.values()]
    return sorted(varoitukset, key=lambda v: v.alku)


def tarkista(leipa: Leipateksti, analyysit: list[Analyysi] | None = None,
             tyyli: bool = False) -> list[Varoitus]:
    analyysit = analyysit if analyysit is not None else ajuri.analysoi(leipa)
    tulos = []
    for x in analyysit:
        tulos.extend(tarkista_analyysi(x, leipa.teksti, tyyli))
    return tulos


def tarkista_teksti(teksti: str) -> list[Varoitus]:
    """Arviointia varten: tarkistaa valmiin leipätekstin (käyttää jäsennysvälimuistia)."""
    return tarkista(lue_teksti(teksti))
