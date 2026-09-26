"""Kultainen standardi ja mittari (PLAN_PILKKU.md, luvut 5 ja 7.3/V1).

Merkintätapa kultaisessa tekstissä:
    [+,]   pakollinen pilkku puuttuu tästä
    [-,]   tässä oleva pilkku on ylimääräinen (merkintä pilkun paikalle)
    [?,]   valinnainen pilkku puuttuu tästä
    [?-,]  tässä oleva pilkku on valinnainen
Merkinnän perään voi kirjoittaa säännön: [+,S1].
"""
from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Callable, Iterable

from .tyypit import Varoitus

MERKINTA = re.compile(r"\[(\?-|\+|-|\?),([A-Za-z0-9]*)\]")


@dataclass(frozen=True)
class Kultakohta:
    offset: int              # lisättävä: raon kohta; poistettava: pilkun indeksi
    laji: str                # "+", "-", "?", "?-"
    saanto: str = ""

    @property
    def toimenpide(self) -> str:
        return "lisaa" if self.laji in ("+", "?") else "poista"

    @property
    def valinnainen(self) -> bool:
        return self.laji.startswith("?")


@dataclass
class Kulta:
    teksti: str
    kohdat: list[Kultakohta]


def normalisoi_rako(teksti: str, offset: int) -> int:
    """Lisättävän pilkun paikka = edellisen ei-välilyöntimerkin jälkeen."""
    while offset > 0 and teksti[offset - 1].isspace():
        offset -= 1
    return offset


def jasenna_kulta(merkitty: str) -> Kulta:
    osat: list[str] = []
    kohdat: list[Kultakohta] = []
    pituus = 0
    edellinen = 0
    for m in MERKINTA.finditer(merkitty):
        vali = merkitty[edellinen:m.start()]
        osat.append(vali)
        pituus += len(vali)
        laji, saanto = m.group(1), m.group(2)
        if laji in ("-", "?-"):
            kohdat.append(Kultakohta(pituus, laji, saanto))
            osat.append(",")
            pituus += 1
        else:
            kohdat.append(Kultakohta(pituus, laji, saanto))
        edellinen = m.end()
    osat.append(merkitty[edellinen:])
    teksti = "".join(osat)
    kohdat = [Kultakohta(normalisoi_rako(teksti, k.offset), k.laji, k.saanto)
              if k.toimenpide == "lisaa" else k for k in kohdat]
    return Kulta(teksti, kohdat)


@dataclass
class Laskuri:
    osumat: int = 0
    vaarat: int = 0          # väärät hälytykset
    ohitukset: int = 0
    valinnaiset: int = 0     # varoitus valinnaiseen kohtaan: ei osuma eikä virhe

    @property
    def tarkkuus(self) -> float | None:
        n = self.osumat + self.vaarat
        return self.osumat / n if n else None

    @property
    def kattavuus(self) -> float | None:
        n = self.osumat + self.ohitukset
        return self.osumat / n if n else None


@dataclass
class Tulos:
    yhteensa: dict[str, Laskuri] = field(default_factory=lambda: defaultdict(Laskuri))
    saannoittain: dict[str, Laskuri] = field(default_factory=lambda: defaultdict(Laskuri))
    varmuuksittain: dict[str, Laskuri] = field(default_factory=lambda: defaultdict(Laskuri))
    vaarat: list[Varoitus] = field(default_factory=list)
    ohitetut: list[Kultakohta] = field(default_factory=list)


def _avain(teksti: str, v: Varoitus) -> tuple[int, str]:
    if v.toimenpide == "lisaa":
        return normalisoi_rako(teksti, v.alku), "lisaa"
    return v.alku, "poista"


def vertaa(varoitukset: Iterable[Varoitus], kulta: Kulta, tulos: Tulos | None = None) -> Tulos:
    """Vertaa varoituksia kultaiseen standardiin. Tulos kertyy annettuun olioon."""
    tulos = tulos or Tulos()
    kohdat = {(k.offset, k.toimenpide): k for k in kulta.kohdat}
    loydetyt = set()
    for v in varoitukset:
        avain = _avain(kulta.teksti, v)
        k = kohdat.get(avain)
        laskurit = [tulos.yhteensa[v.toimenpide], tulos.saannoittain[v.saanto],
                    tulos.varmuuksittain[v.varmuus]]
        if k is None:
            for l in laskurit:
                l.vaarat += 1
            tulos.vaarat.append(v)
        elif k.valinnainen:
            for l in laskurit:
                l.valinnaiset += 1
        else:
            for l in laskurit:
                l.osumat += 1
            loydetyt.add(avain)
    for avain, k in kohdat.items():
        if not k.valinnainen and avain not in loydetyt:
            tulos.yhteensa[k.toimenpide].ohitukset += 1
            tulos.saannoittain[k.saanto or "?"].ohitukset += 1
            tulos.ohitetut.append(k)
    return tulos


def arvioi(tarkistin: Callable[[str], list[Varoitus]], kullat: Iterable[Kulta]) -> Tulos:
    tulos = Tulos()
    for k in kullat:
        vertaa(tarkistin(k.teksti), k, tulos)
    return tulos


def _pros(x: float | None) -> str:
    return "  –  " if x is None else f"{100 * x:5.1f}"


def taulukko(tulos: Tulos) -> str:
    rivit = ["| ryhmä | osumat | väärät | ohitetut | valinn. | tarkkuus % | kattavuus % |",
             "|---|---|---|---|---|---|---|"]
    for otsikko, ryhma in (("", tulos.yhteensa), ("sääntö ", tulos.saannoittain),
                           ("varmuus ", tulos.varmuuksittain)):
        for nimi in sorted(ryhma):
            l = ryhma[nimi]
            rivit.append(f"| {otsikko}{nimi} | {l.osumat} | {l.vaarat} | {l.ohitukset} | "
                         f"{l.valinnaiset} | {_pros(l.tarkkuus)} | {_pros(l.kattavuus)} |")
    return "\n".join(rivit)


def lue_kultatiedosto(polku: str) -> list[Kulta]:
    """Tiedoston kappaleet (tyhjällä rivillä erotetut) omina Kulta-olioinaan.
    Rivit, jotka alkavat merkillä '%', ovat kommentteja."""
    with open(polku, encoding="utf-8") as f:
        rivit = [r for r in f.read().split("\n") if not r.startswith("%")]
    kappaleet = [k.strip() for k in "\n".join(rivit).split("\n\n") if k.strip()]
    return [jasenna_kulta(k) for k in kappaleet]


def _konteksti(teksti: str, offset: int, leveys: int = 45) -> str:
    return (teksti[max(0, offset - leveys):offset] + " ‸ " + teksti[offset:offset + leveys]).replace("\n", " ")


def _tarkistimet() -> dict[str, Callable[[str], list[Varoitus]]]:
    from . import lahtotaso
    t = {"vanha": lahtotaso.vanha, "sanalista": lahtotaso.sanalista}
    try:
        from .saantotarkistin import tarkista_teksti
        t["pylkutus"] = tarkista_teksti
    except ImportError:
        pass
    return t


def main(argv=None):
    import argparse
    tarkistimet = _tarkistimet()
    p = argparse.ArgumentParser(description="Mittaa tarkistimen kultaista otosta vasten.")
    p.add_argument("kulta", nargs="+", help="kultaiset tiedostot")
    p.add_argument("-t", "--tarkistin", choices=sorted(tarkistimet), default="sanalista")
    p.add_argument("-v", "--virheet", action="store_true", help="näytä väärät ja ohitetut")
    a = p.parse_args(argv)
    kullat = [k for polku in a.kulta for k in lue_kultatiedosto(polku)]
    tulos = Tulos()
    virherivit = []
    for n, k in enumerate(kullat, 1):
        ennen_v, ennen_o = len(tulos.vaarat), len(tulos.ohitetut)
        vertaa(tarkistimet[a.tarkistin](k.teksti), k, tulos)
        for v in tulos.vaarat[ennen_v:]:
            virherivit.append(f"VÄÄRÄ    k{n:02d} [{v.varmuus}/{v.saanto}] {_konteksti(k.teksti, v.alku)}")
        for o in tulos.ohitetut[ennen_o:]:
            virherivit.append(f"OHITETTU k{n:02d} [{o.laji}{o.saanto}] {_konteksti(k.teksti, o.offset)}")
    print(taulukko(tulos))
    if a.virheet:
        print("\n".join(virherivit))


if __name__ == "__main__":
    main()
