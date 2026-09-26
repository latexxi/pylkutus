"""Sanastoon perustuvat puuttuvan pilkun säännöt, jotka eivät riipu lauserajoista.

Käytetään, koska puuttuva pilkku voi sekoittaa jäsennyksen (huomioi mitkä … → mitkä määritteenä).
Tuottaa Paatos-olioita samaan ratkaisuun kuin lauserajasäännöt.
"""
from __future__ import annotations

from typing import Iterator

from ..sanastot import KYSYMYSSANAT, KYSYMYSVERBIT
from ..tyypit import Analyysi, Paatos, Pakko, Varmuus

JALKISANAT_EI_KYSYMYS = {"tahansa", "hyvänsä", "ikinä", "vain", "muuta", "muutakaan", "kaikkea"}


def s3_kysymysverbi(x: Analyysi) -> Iterator[Paatos]:
    """S3: kysymysverbi + kysymyssana tai -ko/-kö-verbi ilman pilkkua."""
    tt = x.a.tokenit
    for i in range(1, len(tt)):
        if x.a.rako[i]:
            continue
        ed, t = tt[i - 1], tt[i]
        if ed.upos != "VERB" or ed.lemma.lower() not in KYSYMYSVERBIT:
            continue
        seur = tt[i + 1].teksti.lower() if i + 1 < len(tt) else ""
        kysymyssana = t.teksti.lower() in KYSYMYSSANAT and seur not in JALKISANAT_EI_KYSYMYS \
            and t.feats.get("Degree") != "Sup" and not seur.endswith(("in", "immin"))
        ko = "Ko" in t.feats.get("Clitic", "") and t.feats.get("VerbForm") == "Fin"
        if kysymyssana or ko:
            yield Paatos(i, "S3", Pakko.KYLLA, Varmuus.MEDIUM)


SAANNOT = [s3_kysymysverbi]
