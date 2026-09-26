"""Moduuli 1: leipätekstin poiminta ja offset-kartta (PLAN_PILKKU.md 3.3, 7.3/V4)."""
from __future__ import annotations

import re
from dataclasses import dataclass

from .tyypit import Leipateksti

OTSIKKO_MD = re.compile(r"^#{1,6}\s")
LUETTELO = re.compile(r"^\s*(?:\d+\.|[-*+])\s+")
# Poistettavat merkinnät kappaleen sisältä. Poistetaan vain merkit, loput säilyvät.
POISTETTAVAT = [
    ("span", re.compile(r"</?span[^>]*>")),
    ("lihavointi", re.compile(r"\*\*|__")),
    ("korostus", re.compile(r"(?<![\w*])[*_](?=\w)|(?<=\w)[*_](?![\w*])")),
    ("kenoviiva", re.compile(r"\\(?=\S)")),
    ("pehmea tavuviiva", re.compile("\u00ad")),
    ("muistiinpano", re.compile(r"\s*\+\+.*$")),
    ("loppuvali", re.compile(r"\s+$")),
]
LOPPUMERKKI = re.compile(r"[.?!:…\"”»)—–]\s*$")
VIRKERAJA = re.compile(r"[.?!]\s+[A-ZÅÄÖ]")
OTSIKON_MAKSIMIPITUUS = 100


@dataclass
class Lokirivi:
    rivi: int                # 1-pohjainen
    syy: str
    teksti: str


def _on_otsikon_kaltainen(rivi: str) -> bool:
    """Rivi ilman #-merkkiä, joka näyttää otsikolta."""
    s = rivi.strip()
    if LOPPUMERKKI.search(s):
        return False
    if s.startswith("**") and s.rstrip().endswith("**"):
        return True
    return len(s) < OTSIKON_MAKSIMIPITUUS and not VIRKERAJA.search(s)


def _siivoa(rivi: str) -> tuple[list[int], list[str]]:
    """Palauttaa säilyvien merkkien indeksit rivillä ja poistettujen merkintöjen syyt."""
    poistettu = [False] * len(rivi)
    syyt = []
    for syy, lauseke in POISTETTAVAT:
        for m in lauseke.finditer(rivi):
            if m.start() == m.end():
                continue
            if syy not in ("loppuvali",):
                syyt.append(f"{syy}: {rivi[m.start():m.end()].strip()!r}")
            for i in range(m.start(), m.end()):
                poistettu[i] = True
    m = LUETTELO.match(rivi)
    if m:
        for i in range(m.start(), m.end()):
            poistettu[i] = True
    sailyvat = [i for i, p in enumerate(poistettu) if not p]
    # alun välilyönnit pois
    while sailyvat and rivi[sailyvat[0]].isspace():
        sailyvat.pop(0)
    return sailyvat, syyt


def _lohkot(sisalto: str):
    """Jakaa tiedoston lohkoihin: peräkkäiset ei-tyhjät rivit, paitsi että #-otsikko ja
    luettelon kohta ovat aina omia lohkojaan. Palauttaa (laji, [(nro, rivin_alku, rivi)])."""
    lohko: list[tuple[int, int, str]] = []
    alku = 0
    for nro, rivi in enumerate(sisalto.split("\n"), 1):
        rivin_alku = alku
        alku += len(rivi) + 1
        if not rivi.strip():
            if lohko:
                yield "kappale", lohko
                lohko = []
            continue
        if OTSIKKO_MD.match(rivi) or LUETTELO.match(rivi):
            if lohko:
                yield "kappale", lohko
                lohko = []
            yield ("otsikko" if OTSIKKO_MD.match(rivi) else "luettelo"), [(nro, rivin_alku, rivi)]
            continue
        lohko.append((nro, rivin_alku, rivi))
    if lohko:
        yield "kappale", lohko


def lue_md(sisalto: str) -> tuple[Leipateksti, list[Lokirivi]]:
    loki: list[Lokirivi] = []
    teksti: list[str] = []
    kartta: list[int] = []
    kappaleet: list[tuple[int, int]] = []
    viimeinen = len(sisalto) - 1

    for laji, rivit in _lohkot(sisalto):
        if laji == "otsikko":
            loki.append(Lokirivi(rivit[0][0], "otsikko", rivit[0][2]))
            continue
        merkit: list[tuple[str, int]] = []
        lokirivit: list[Lokirivi] = []
        for nro, rivin_alku, rivi in rivit:
            sailyvat, syyt = _siivoa(rivi)
            lokirivit.extend(Lokirivi(nro, "merkintä", s) for s in syyt)
            if not sailyvat:
                continue
            if merkit:
                # kappaleen sisäinen rivinvaihto -> välilyönti, osoittaa edellisen rivin "\n"-merkkiin
                merkit.append((" ", rivin_alku - 1))
            merkit.extend((rivi[i], rivin_alku + i) for i in sailyvat)
        siivottu = "".join(m for m, _ in merkit)
        if not siivottu:
            continue
        if laji == "kappale" and _on_otsikon_kaltainen(siivottu):
            loki.extend(Lokirivi(nro, "otsikon kaltainen", rivi) for nro, _, rivi in rivit)
            continue
        loki.extend(lokirivit)
        if kappaleet:
            # kappaleraja osoittaa edellisen kappaleen jälkeiseen rivinvaihtoon
            raja = min(kartta[-1] + 1, viimeinen)
            while raja < viimeinen and sisalto[raja] != "\n":
                raja += 1
            teksti.extend("\n\n")
            kartta.extend([raja, raja])
        kappaleen_alku = len(teksti)
        for m, o in merkit:
            teksti.append(m)
            kartta.append(o)
        kappaleet.append((kappaleen_alku, len(teksti)))
    return Leipateksti("".join(teksti), sisalto, kartta, kappaleet), loki


def lue_teksti(sisalto: str) -> Leipateksti:
    """Valmis leipäteksti (esim. kultainen otos): kappaleet tyhjillä riveillä erotettuina."""
    kappaleet = []
    for m in re.finditer(r"[^\n]+(?:\n[^\n]+)*", sisalto):
        kappaleet.append((m.start(), m.end()))
    return Leipateksti(sisalto, sisalto, list(range(len(sisalto))), kappaleet)


def tarkista_kartta(leipa: Leipateksti) -> list[int]:
    """Invariantti: jokainen leipätekstin merkki vastaa alkuperäistä merkkiä.
    Poikkeus: kappalerajat ja rivinvaihdosta syntyneet välilyönnit osoittavat rivinvaihtoon.
    Palauttaa rikkovien merkkien indeksit."""
    virheet = []
    for i, m in enumerate(leipa.teksti):
        o = leipa.alkuperainen[leipa.kartta[i]]
        if m == o or (m in " \n" and o == "\n"):
            continue
        virheet.append(i)
    return virheet


def main(argv=None):
    import argparse
    p = argparse.ArgumentParser(description="Poimii leipätekstin md-tiedostosta.")
    p.add_argument("tiedosto")
    p.add_argument("--leipa", help="kirjoita leipäteksti tähän tiedostoon")
    p.add_argument("--loki", help="kirjoita karsitut rivit tähän tiedostoon")
    a = p.parse_args(argv)
    with open(a.tiedosto, encoding="utf-8") as f:
        leipa, loki = lue_md(f.read())
    virheet = tarkista_kartta(leipa)
    if a.leipa:
        with open(a.leipa, "w", encoding="utf-8") as f:
            f.write(leipa.teksti + "\n")
    if a.loki:
        with open(a.loki, "w", encoding="utf-8") as f:
            for l in loki:
                f.write(f"{l.rivi}\t{l.syy}\t{l.teksti}\n")
    print(f"kappaleita {len(leipa.kappaleet)}, merkkejä {len(leipa.teksti)}, "
          f"karsittuja rivejä {sum(l.syy != 'merkintä' for l in loki)}, "
          f"poistettuja merkintöjä {sum(l.syy == 'merkintä' for l in loki)}, "
          f"karttavirheitä {len(virheet)}")
    return 1 if virheet else 0


if __name__ == "__main__":
    raise SystemExit(main())
