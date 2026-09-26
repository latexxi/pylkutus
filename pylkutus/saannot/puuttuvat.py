"""Puuttuvat pilkut lauserajoilla (luvut 1.1–1.9).

Jokainen sääntö saa rajan ja palauttaa päätöksen: (koodi, pakko, varmuus) tai None, jos
sääntö ei koske rajaa. pakko: "kyllä" | "valinnainen" | "ei".
"""
from __future__ import annotations

from ..ajuri import Analyysi
from ..sanastot import (MONIOSAISET, RAJAMERKIT_EDELLA, RAJAMERKIT_JALJESSA, RINNASTUS_JA,
                        RINNASTUS_MUTTA, RINNASTUS_SILLA)
from ..tyypit import Lause, Raja, Token

Paatos = tuple[str, str, str]      # (sääntö, pakko, varmuus)
LAINAUSMERKIT = {'"', "”", "“", "»", "«", "'"}


def _kieltokonjunktio(t: Token) -> bool:
    """eikä, emmekä, eivätkä … toimivat kuten ja."""
    return t.lemma.lower() == "ei" and t.teksti.lower().endswith(("kä", "ka"))


def _sana(x: Analyysi, i: int) -> str:
    return x.a.tokenit[i].teksti.lower() if 0 <= i < len(x.a.tokenit) else ""


def _lemma(x: Analyysi, i: int) -> str:
    return x.a.tokenit[i].lemma.lower() if 0 <= i < len(x.a.tokenit) else ""


def rajamerkki_edella(x: Analyysi, rako: int) -> bool:
    """1.15: ajatusviiva, sulkeet, kaksoispiste, puolipiste tai lainausmerkki raon kohdalla."""
    tt = x.a.tokenit
    i = rako - 1
    while i >= 0 and tt[i].teksti in LAINAUSMERKIT:
        i -= 1                  # sanoi: "Bill …
    j = rako
    while j < len(tt) and tt[j].teksti in LAINAUSMERKIT:
        j += 1
    return (i >= 0 and tt[i].teksti in RAJAMERKIT_EDELLA) or \
        (j < len(tt) and tt[j].teksti in RAJAMERKIT_JALJESSA)


def moniosainen(x: Analyysi, rako: int) -> int | None:
    """M1: jos raon edellä on moniosaisen ilmauksen alkuosa, palauttaa ilmauksen alun."""
    sanat = [t.teksti.lower() for t in x.a.tokenit]
    for ilmaus in sorted(MONIOSAISET, key=len, reverse=True):
        n = len(ilmaus) - 1
        if rako - n < 0 or rako >= len(sanat):
            continue
        if tuple(sanat[rako - n:rako + 1]) == ilmaus and not any(x.a.rako[rako - n + 1:rako + 1]):
            return rako - n
    return None


def _moniosainen_alussa(x: Analyysi, l: Lause) -> int | None:
    """Jos lauseen alussa on moniosainen ilmaus (heti kun), palauttaa viimeisen osan indeksin."""
    sanat = [t.teksti.lower() for t in x.a.tokenit]
    for ilmaus in MONIOSAISET:
        n = len(ilmaus)
        if tuple(sanat[l.alku:l.alku + n]) == ilmaus:
            return l.alku + n - 1
    return None


def _ylin_paalause(x: Analyysi, l: Lause) -> bool:
    """Onko rinnasteisen lauseen ylempi lause päälause (tai päälauseen rinnasteinen)."""
    lauseet = {k.paa: k for k in x.lauseet}
    yl = lauseet.get(l.ylempi) if l.ylempi is not None else None
    while yl is not None and yl.tyyppi == "rinnasteinen":
        yl = lauseet.get(yl.ylempi) if yl.ylempi is not None else None
    return yl is None or yl.tyyppi == "paa"


def _paalause_relatiivin_sisalla(x: Analyysi, l: Lause) -> bool:
    """Relatiivilauseeseen liitetty conj, jolla on oma subjekti mutta ei relatiivisanaa:
    todennäköisesti rinnasteinen päälause (miehen, jolla oli lapsia ja se vaikutti …)."""
    lauseet = {k.paa: k for k in x.lauseet}
    yl = lauseet.get(l.ylempi) if l.ylempi is not None else None
    if yl is None or yl.tyyppi != "relatiivi" or l.taydellisyys != "taydellinen" or l.r1a:
        return False
    alku = x.a.tokenit[l.alku + 1:l.alku + 3]
    if any(t.feats.get("PronType") in ("Rel", "Int") or t.lemma.lower() in ("joka", "mikä")
           for t in alku):
        return False
    return any(t.head - 1 == l.paa and t.deprel.startswith("nsubj") for t in x.a.tokenit)


def alkupilkku(x: Analyysi, r: Raja) -> Paatos | None:
    l = r.lause
    alku = l.alku
    eka = _sana(x, alku)
    ed = _sana(x, alku - 1)
    ed_token: Token = x.a.tokenit[alku - 1]

    if l.tyyppi == "rinnasteinen":
        return rinnastus(x, r)

    # S1b: kaksi peräkkäistä konjunktiota ("että jos", "ja kun")
    if ed_token.deprel in ("mark", "cc") or ed in RINNASTUS_JA | RINNASTUS_MUTTA:
        return ("S1b", "ei", "high")
    if x.a.tokenit[alku].deprel == "cc":
        return None             # "ja jos ehdin", ", mutta kun": cc kuuluu sivulauseeseen, ei päätöstä

    # V2: "ennen kuin" päälauseen jäljessä: pilkku valinnainen
    if eka == "ennen" and _sana(x, alku + 1) == "kuin":
        return ("V2", "valinnainen", "high")

    # M1: moniosainen ilmaus lauseen alussa ("heti kun" jäsennetty sivulauseen sisään)
    m = _moniosainen_alussa(x, l)
    if m is not None:
        if x.a.rako[m]:                              # "heti, kun": pilkku ilmauksen sisällä
            return ("M1", "valinnainen", "high")
        if _sana(x, alku - 1) in RINNASTUS_JA | RINNASTUS_MUTTA:
            return ("M3", "ei", "high")
        return ("M1", "kyllä", "high")

    if l.aloittaja is not None and x.a.tokenit[l.aloittaja].deprel == "mark":
        mark = eka
        if mark == "sillä":
            return ("R4", "kyllä", "medium")
        if mark == "kuin":
            if ed == "ennen":
                return ("V2", "valinnainen", "high")
            return ("V1", "ei", "high")
        if mark == "kuten":
            return ("V5", "kyllä", "medium")
        # M1/M3: moniosainen ilmaus
        m = moniosainen(x, alku)
        if m is not None:
            if m == 0 or x.a.rako[m] or rajamerkki_edella(x, m) \
                    or _sana(x, m - 1) in RINNASTUS_JA | RINNASTUS_MUTTA:
                return ("M1", "valinnainen", "high")
            return ("M1", "kyllä", "high")
        # S1a: hyvin lyhyt virke
        ennen = [t for t in x.a.tokenit[:alku] if t.upos != "PUNCT"]
        if len(ennen) == 1 and l.loppu - l.alku + 1 <= 3 and l.tyyppi != "kysymys":
            return ("S1a", "valinnainen", "high")
        return ("S1", "kyllä", "high")

    if l.tyyppi == "kysymys":
        return ("S3", "kyllä", "medium")

    if l.tyyppi == "relatiivi":
        # K1/K2: "se, joka" / "se, mitä"
        if _lemma(x, alku - 1) == "se" and x.a.tokenit[alku - 1].upos == "PRON":
            se = alku - 1
            if se == 0 or all(t.upos == "PUNCT" for t in x.a.tokenit[:se]):
                return ("K2", "valinnainen", "high")
            if _sana(x, se - 1) in RINNASTUS_JA | RINNASTUS_MUTTA:
                return ("K1", "kyllä", "low")       # 1.4: rajatapaus
            return ("K1", "kyllä", "medium")
        if l.aloittaja is None:
            return None                              # relatiivisanaa ei tunnistettu
        return ("S2", "kyllä", "medium")

    if l.tyyppi == "sivu":
        if l.aloittaja is None:
            return None                              # esim. finiittinen acl ilman sidesanaa
        return ("S1", "kyllä", "medium")
    return None


def rinnastus(x: Analyysi, r: Raja) -> Paatos | None:
    l = r.lause
    eka = _sana(x, l.alku)
    if _kieltokonjunktio(x.a.tokenit[l.alku]):
        eka = "eikä"
    if not _ylin_paalause(x, l):
        # S4: rinnasteiset sivulauseet; ilman konjunktiota S6
        if eka in RINNASTUS_JA:
            if _paalause_relatiivin_sisalla(x, l):
                return ("R1", "kyllä", "low")
            return ("S4", "ei", "medium")
        if eka in RINNASTUS_MUTTA:
            return ("R3", "valinnainen" if l.taydellisyys == "vajaa" else "kyllä", "low")
        return ("S6", "kyllä", "low")
    if eka in RINNASTUS_SILLA:
        return ("R4", "kyllä", "medium")
    if eka in RINNASTUS_MUTTA:
        if l.taydellisyys == "vajaa":
            return ("R3", "valinnainen", "medium")
        return ("R3", "kyllä", "medium" if l.taydellisyys == "taydellinen" else "low")
    if eka in RINNASTUS_JA:
        if l.taydellisyys == "vajaa":
            return ("R2", "ei", "medium")
        if l.r1a:
            return ("R1a", "valinnainen", "medium")
        if l.taydellisyys == "ratkaisematon":
            return ("R1", "kyllä", "low")
        return ("R1", "kyllä", "low")
    if x.a.tokenit[l.alku].deprel == "cc":
        return None                                  # muu konjunktio (esim. "saati")
    return ("S6", "kyllä", "low")              # V7: tarkkuus heikko koko dokumentilla


def loppupilkku(x: Analyysi, r: Raja) -> Paatos | None:
    l = r.lause
    if l.tyyppi == "rinnasteinen":
        return None
    seur = r.rako
    if seur < len(x.a.tokenit) and x.a.tokenit[seur].upos == "PUNCT":
        return None             # sulku, lainausmerkki tms. heti lauseen jälkeen
    seur_sana = _sana(x, seur)
    if seur_sana in RINNASTUS_JA | RINNASTUS_MUTTA:
        return None             # sivulause päättyy, rinnastus jatkuu: R-säännöt ratkaisevat
    koodi = {"relatiivi": "S2a", "kysymys": "S1e", "sivu": "S1e"}.get(l.tyyppi, "S1e")
    if l.tyyppi == "relatiivi" and _lemma(x, l.alku - 1) == "se":
        koodi = "K3"
    if l.virkkeen_alussa and l.tyyppi == "sivu" and _sana(x, l.alku) == "ennen":
        return ("V2", "kyllä", "medium")
    # V7: loppurajat perustuvat jänteeseen, joka hajoaa helposti puuttuvan pilkun takia;
    # koko dokumentilla S1e-varoituksista lähes kaikki vääriä, joten aina matala varmuus.
    return (koodi, "kyllä", "low")


def paata(x: Analyysi, r: Raja) -> Paatos | None:
    if rajamerkki_edella(x, r.rako):
        return ("1.15", "ei", "high")
    if r.laji == "alku":
        return alkupilkku(x, r)
    return loppupilkku(x, r)
