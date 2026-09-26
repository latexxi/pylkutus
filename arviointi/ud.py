"""Synteettinen mittari UD Finnish TDT:n test-jaosta (PLAN_KORJAUKSET.md, K6).

Test-jako ei ole Stanzan fi/default-mallin opetusdatassa. Jokainen pilkku poistetaan
todennäköisyydellä p (kiinteä siemen); poistetut merkitään kultaiseen tekstiin [+,].
Muut raot oletetaan oikeiksi: jäljelle jääneet pilkut ovat paikallaan, eikä pilkuttomiin
rakoihin kuulu pilkkua. Oletus on karkea (korpuksessa on valinnaisia ja virheellisiä pilkkuja),
joten luvut sopivat versioiden vertailuun, eivät absoluuttiseksi tarkkuudeksi. Blogeissa (b) ja
fiktiossa (f) pilkkuja puuttuu jo lähtötekstistä; toimitetut lajit: --lajit e,j,t,u.

    python arviointi/ud.py tee [--lajit e,j,t,u]  # lataa korpuksen, kirjoittaa ud/ud_test_p50*.txt
    python -m pylkutus.arviointi -t pylkutus arviointi/ud/ud_test_p50.txt   # jäsentimellä
    python arviointi/ud.py kultapuut          # säännöt UD:n kultaisilla puilla
"""
from __future__ import annotations

import argparse
import os
import random
import urllib.request
from dataclasses import dataclass

from pylkutus import arviointi, conllu, lauseistaja, saantotarkistin
from pylkutus.conllu import ConlluVirke, Sana
from pylkutus.tyypit import Analyysi

HAK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ud")
URL = ("https://raw.githubusercontent.com/UniversalDependencies/UD_Finnish-TDT/"
       "r2.15/fi_tdt-ud-test.conllu")
KORPUS = os.path.join(HAK, "fi_tdt-ud-test.conllu")
SIEMEN = 2026


@dataclass
class UdVirke:
    id: str
    teksti: str
    sanat: list[Sana]        # offsetit virkkeen tekstiin, pilkut mukana


def lataa() -> str:
    if not os.path.exists(KORPUS):
        os.makedirs(HAK, exist_ok=True)
        urllib.request.urlretrieve(URL, KORPUS)
    return KORPUS


def lue_ud(polku: str) -> list[UdVirke]:
    """CoNLL-U → virkkeet. Sanojen offsetit haetaan # text -rivistä pintamuotojen mukaan;
    MWT:n sanat saavat koko tokenin välin (kuten pylkutus.conllu)."""
    virkkeet: list[UdVirke] = []
    with open(polku, encoding="utf-8") as f:
        lohkot = f.read().strip().split("\n\n")
    for lohko in lohkot:
        teksti, tunnus = "", ""
        sanat: list[Sana] = []
        kursori = 0
        mwt_loppu, mwt_vali = 0, (0, 0)
        for rivi in lohko.split("\n"):
            if rivi.startswith("# text = "):
                teksti = rivi[len("# text = "):]
                continue
            if rivi.startswith("# sent_id = "):
                tunnus = rivi[len("# sent_id = "):]
                continue
            if rivi.startswith("#"):
                continue
            c = rivi.split("\t")
            if "." in c[0]:
                continue                                   # tyhjät solmut
            if "-" in c[0]:
                a, b = c[0].split("-")
                alku = teksti.index(c[1], kursori)
                kursori = alku + len(c[1])
                mwt_loppu, mwt_vali = int(b), (alku, kursori)
                continue
            i = int(c[0])
            if i <= mwt_loppu:
                alku, loppu = mwt_vali
            else:
                alku = teksti.index(c[1], kursori)
                loppu = kursori = alku + len(c[1])
            sanat.append(Sana(i, c[1], "" if c[2] == "_" else c[2], c[3], c[4],
                              conllu._feats_dict(c[5]), int(c[6]), c[7], alku, loppu))
        virkkeet.append(UdVirke(tunnus, teksti, sanat))
    return virkkeet


def laji(v: UdVirke) -> str:
    return v.id.rstrip("0123456789.")


def valitse(virkkeet: list[UdVirke], poistot: list[list[int]], lajit: set[str] | None):
    """Rajaus tekstilajeihin vioituksen jälkeen, jotta poistot ovat samat kaikissa rajauksissa."""
    return [(v, p) for v, p in zip(virkkeet, poistot) if not lajit or laji(v) in lajit]


def _poistettavat(v: UdVirke, rng: random.Random, p: float) -> list[int]:
    """Poistettavien pilkkujen offsetit. Vain pilkut, joita seuraa välilyönti."""
    tulos = []
    for s in v.sanat:
        if conllu.on_pilkku(s) and v.teksti[s.loppu:s.loppu + 1] == " " and rng.random() < p:
            tulos.append(s.alku)
    return tulos


def vioita(virkkeet: list[UdVirke], p: float, siemen: int = SIEMEN) -> list[list[int]]:
    rng = random.Random(siemen)
    return [_poistettavat(v, rng, p) for v in virkkeet]


def merkitty(v: UdVirke, poistot: list[int]) -> str:
    osat, ed = [], 0
    for o in poistot:
        osat.append(v.teksti[ed:o] + "[+,]")
        ed = o + 1
    return "".join(osat) + v.teksti[ed:]


def tee(p: float, lajit: set[str] | None) -> str:
    virkkeet = lue_ud(lataa())
    valitut = valitse(virkkeet, vioita(virkkeet, p), lajit)
    loppu = "_" + "".join(sorted(lajit)) if lajit else ""
    polku = os.path.join(HAK, f"ud_test_p{int(p * 100)}{loppu}.txt")
    with open(polku, "w", encoding="utf-8") as f:
        f.write(f"% UD Finnish TDT test, pilkut poistettu todennäköisyydellä {p}, siemen {SIEMEN}"
                f"{', lajit ' + ','.join(sorted(lajit)) if lajit else ''}\n")
        f.write("% Luotu: python arviointi/ud.py tee. Merkinnät: pylkutus/arviointi.py\n\n")
        f.write("\n\n".join(merkitty(v, pp) for v, pp in valitut) + "\n")
    print(f"{polku}: {len(valitut)} virkettä, {sum(len(pp) for _, pp in valitut)} poistettua pilkkua")
    return polku


def kultapuu(v: UdVirke, poistot: list[int]) -> Analyysi:
    """Kultainen puu vioitettuun tekstiin: poistetut pilkut pois raoista, offsetit siirretty."""
    def siirra(o: int) -> int:
        return o - sum(1 for p in poistot if p < o)
    sanat = [Sana(s.id, s.teksti, s.lemma, s.upos, s.xpos, dict(s.feats), s.head, s.deprel,
                  siirra(s.alku), siirra(s.loppu)) for s in v.sanat]
    virke = conllu.virkkeeksi(ConlluVirke(sanat))
    poistetut = {siirra(p) for p in poistot}
    for i in range(1, len(virke.tokenit) + 1):
        if virke.rako[i] and virke.tokenit[i - 1].loppu in poistetut:
            virke.rako[i] = None
    return Analyysi(virke, *lauseistaja.lauseista(virke))


def kultapuut(p: float, lajit: set[str] | None, virheet: bool) -> None:
    virkkeet = lue_ud(lataa())
    tulos = arviointi.Tulos()
    for v, pp in valitse(virkkeet, vioita(virkkeet, p), lajit):
        kulta = arviointi.jasenna_kulta(merkitty(v, pp))
        x = kultapuu(v, pp)
        ennen = len(tulos.vaarat)
        arviointi.vertaa(saantotarkistin.tarkista_analyysi(x, kulta.teksti), kulta, tulos)
        if virheet:
            for w in tulos.vaarat[ennen:]:
                print(f"VÄÄRÄ    {v.id:<8} [{w.varmuus}/{w.saanto}] "
                      f"{arviointi._konteksti(kulta.teksti, w.alku)}")
    print(arviointi.taulukko(tulos))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("toiminto", choices=["tee", "kultapuut"])
    ap.add_argument("-p", type=float, default=0.5, help="pilkun poistotodennäköisyys")
    ap.add_argument("--lajit", help="tekstilajit pilkulla erotettuina (sent_id:n etuliite)")
    ap.add_argument("-v", "--virheet", action="store_true")
    a = ap.parse_args()
    lajit = set(a.lajit.split(",")) if a.lajit else None
    if a.toiminto == "tee":
        tee(a.p, lajit)
    else:
        kultapuut(a.p, lajit, a.virheet)


if __name__ == "__main__":
    main()
