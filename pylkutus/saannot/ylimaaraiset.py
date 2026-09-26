"""Ylimääräiset pilkut (luku 1.13). Palauttaa (rako, sääntö, pakko, varmuus)."""
from __future__ import annotations

from typing import Iterator

from ..ajuri import Analyysi
from ..sanastot import A1_A2

Havainto = tuple[int, str, str, str]


def _rajat(x: Analyysi) -> set[int]:
    return {r.rako for r in x.rajat if r.lahde in ("A", "AB")}


def v1_kuin(x: Analyysi) -> Iterator[Havainto]:
    """V1: vertailun kuin-sanan edellä ei pilkkua (komparatiivi + kuin)."""
    tt = x.a.tokenit
    for i, t in enumerate(tt):
        if t.teksti.lower() != "kuin" or not x.a.rako[i] or i < 1:
            continue
        ed = tt[i - 1]
        if ed.feats.get("Degree") == "Cmp" or ed.lemma.lower() in ("muu", "toinen") \
                or ed.teksti.lower().startswith(("enemm", "enemp", "vähemm", "vähemp")):
            yield (i, "V1", "ei", "medium")


def l1_lauseenvastike(x: Analyysi) -> Iterator[Havainto]:
    """L1: virkkeen alussa olevan lauseenvastikkeen jälkeen ei pilkkua (Kotiin tultuaan, hän söi)."""
    rajat = _rajat(x)
    for l in x.lauseet:
        if l.finiittinen or l.deprel not in ("advcl", "acl") or not l.virkkeen_alussa:
            continue
        if x.a.tokenit[l.alku].teksti.lower() in ("kuten", "kuin"):
            continue            # Kuten sanottu, …
        rako = l.loppu + 1
        if rako < len(x.a.tokenit) and x.a.rako[rako] and rako not in rajat:
            pitka = l.loppu - l.alku + 1 > 5
            yield (rako, "L1", "ei", "low" if pitka else "medium")


def a1_a2_alkusana(x: Analyysi) -> Iterator[Havainto]:
    """A1/A2: lauseen alun asenne- tai järjestyssanan jälkeen ei tavallisesti pilkkua."""
    tt = x.a.tokenit
    eka = next((i for i, t in enumerate(tt) if t.upos != "PUNCT"), None)
    if eka is None or eka + 1 >= len(tt):
        return
    if tt[eka].teksti.lower() in A1_A2 and x.a.rako[eka + 1] and eka + 1 not in _rajat(x):
        yield (eka + 1, "A2" if tt[eka].teksti.lower().endswith("ksi") else "A1",
               "valinnainen", "high")


# R2 ja muut rajapäätöksiin perustuvat: saantotarkistin (pakko=ei + pilkku paikalla)
SAANNOT = [v1_kuin, l1_lauseenvastike, a1_a2_alkusana]
