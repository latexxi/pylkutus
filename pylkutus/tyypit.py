"""Putken vaiheiden väliset tietotyypit (PLAN_PILKKU.md, luku 7.2)."""
from __future__ import annotations

import bisect
from dataclasses import dataclass, field
from enum import StrEnum


@dataclass
class Leipateksti:
    """Lähdetiedostosta poimittu leipäteksti ja paikkatieto."""
    teksti: str              # kappaleet erotettu rivillä "\n\n"
    alkuperainen: str        # lähdetiedoston sisältö
    kartta: list[int]        # leipätekstin merkki i -> alkuperäisen merkin indeksi
    kappaleet: list[tuple[int, int]] = field(default_factory=list)  # (alku, loppu) leipätekstissä

    def __post_init__(self):
        self._rivialut = [0]
        for i, m in enumerate(self.alkuperainen):
            if m == "\n":
                self._rivialut.append(i + 1)

    def rivi_sarake(self, i: int) -> tuple[int, int]:
        """Leipätekstin offset -> alkuperäisen tiedoston (rivi, sarake), 1-pohjaiset."""
        o = self.kartta[i]
        r = bisect.bisect_right(self._rivialut, o) - 1
        return r + 1, o - self._rivialut[r] + 1


@dataclass
class Token:
    i: int                   # indeksi virkkeen tokenilistassa (ilman rajamerkkejä)
    teksti: str
    alku: int                # offset leipätekstiin
    loppu: int
    lemma: str = ""
    upos: str = ""
    feats: dict[str, str] = field(default_factory=dict)
    head: int = 0            # 1-pohjainen kuten CoNLL-U, 0 = juuri
    deprel: str = ""


@dataclass
class Virke:
    tokenit: list[Token]     # kaikki sanat paitsi pilkut; muut välimerkit ovat tokeneita
    rako: list[str | None]   # rako[i] = "," jos pilkku tokenin i edellä; pituus len(tokenit) + 1


@dataclass
class Lause:
    paa: int
    alku: int
    loppu: int
    tyyppi: str              # paa | sivu | relatiivi | kysymys | rinnasteinen
    deprel: str
    aloittaja: int | None    # mark-, cc-, relatiivi- tai kysymyssanan indeksi
    finiittinen: bool
    taydellisyys: str        # taydellinen | vajaa | ratkaisematon
    upotettu: bool           # ylempi lause jatkuu tämän jälkeen
    virkkeen_alussa: bool
    projektiivinen: bool = True
    r1a: bool = False        # 1./2. persoona tai passiivi: R1:n pilkku valinnainen
    ylempi: int | None = None  # ylemmän lauseen pään indeksi
    vapaa: bool = False      # vapaasti viittaava lause (mitä haluat, mistä tahansa): S2b


@dataclass
class Raja:
    rako: int                # tokenien rako-1 ja rako välissä
    laji: str                # alku (lause alkaa raosta) | loppu (lause päättyy rakoon)
    lause: Lause             # lause, jonka alku tai loppu raja on
    ylempi: Lause | None     # lause, jonka sisällä raja on
    merkki: str | None       # "," tai None


@dataclass
class Varoitus:
    saanto: str              # esim. "S1"
    varmuus: str             # Varmuus: high | medium | low
    alku: int                # offset leipätekstiin
    loppu: int
    toimenpide: str          # lisaa | poista
    viesti: str


class Pakko(StrEnum):
    """Säännön päätös raosta: vaaditaanko pilkku."""
    KYLLA = "kyllä"
    VALINNAINEN = "valinnainen"
    EI = "ei"


class Varmuus(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

    @property
    def taso(self) -> int:
        return ("low", "medium", "high").index(self.value)

    def alennettu(self) -> Varmuus:
        """Yhtä astetta matalampi (low pysyy low'na)."""
        return Varmuus(("low", "low", "medium")[self.taso])


@dataclass(frozen=True)
class Paatos:
    """Yhden säännön päätös yhdestä raosta."""
    rako: int
    koodi: str
    pakko: Pakko
    varmuus: Varmuus


@dataclass
class Analyysi:
    """Yhden virkkeen analyysi sääntöjä varten."""
    a: Virke
    lauseet: list[Lause]
    rajat: list[Raja]
