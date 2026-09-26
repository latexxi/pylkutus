"""Putken ajo: esikäsittely, jäsennys, lauseistus (ja myöhemmin säännöt ja raportti)."""
from __future__ import annotations

from dataclasses import dataclass

from . import jasennin, lauseistaja
from .esikasittelija import lue_md, lue_teksti
from .tyypit import Leipateksti, Lause, Raja, Virke


@dataclass
class Analyysi:
    a: Virke
    b: Virke
    lauseet: list[Lause]       # A:n lauseet
    rajat: list[Raja]          # A:n ja B:n rajat yhdistettyinä


def lue(polku: str) -> Leipateksti:
    with open(polku, encoding="utf-8") as f:
        sisalto = f.read()
    if polku.endswith(".md"):
        return lue_md(sisalto)[0]
    return lue_teksti(sisalto)


def analysoi(leipa: Leipateksti, valimuisti=jasennin.VALIMUISTI) -> list[Analyysi]:
    a, b = jasennin.jasenna(leipa, valimuisti)
    tulos = []
    for va, vb in zip(jasennin.virkkeet(a), jasennin.virkkeet(b)):
        la, ra = lauseistaja.lauseista(va)
        _, rb = lauseistaja.lauseista(vb)
        tulos.append(Analyysi(va, vb, la, lauseistaja.yhdista(ra, rb)))
    return tulos


def dump(analyysit: list[Analyysi], mita: str) -> str:
    rivit = []
    for n, x in enumerate(analyysit):
        if mita == "virkkeet":
            rivit.append(" ".join(t.teksti for t in x.a.tokenit))
        elif mita == "lauseet":
            rivit.append(f"{n:4d} {lauseistaja.sulkeet(x.a, x.lauseet)}")
        elif mita == "rajat":
            rivit.append(f"{n:4d} {lauseistaja.sulkeet(x.a, x.lauseet)}")
            for r in x.rajat:
                sana = x.a.tokenit[r.rako].teksti if r.rako < len(x.a.tokenit) else "∎"
                rivit.append(f"       {r.lahde:<2} {r.laji:<5} {r.lause.deprel:<10} "
                             f"{r.lause.tyyppi:<12} {r.lause.taydellisyys:<13} "
                             f"{'pilkku' if r.merkki else '–':<6} ennen \"{sana}\"")
    return "\n".join(rivit)
