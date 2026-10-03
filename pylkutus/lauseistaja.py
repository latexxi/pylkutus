"""Moduuli 3: lauseet ja lauserajat UD-puusta (PLAN_PILKKU.md 3.5, 7.3/V6)."""
from __future__ import annotations

from functools import lru_cache

from .sanastot import (ALISTUS_MARK, KYSYMYSSANAT, VAPAA_ALOITTAJAT, VAPAA_JALKISANAT,
                       VAPAA_RELATIIVIN_VERBIT)
from .tyypit import Lause, Raja, Virke

LAUSESUHTEET = {"root", "advcl", "ccomp", "acl:relcl", "conj", "parataxis", "acl", "xcomp",
                "xcomp:ds"}
FINIITTISET_MODUKSET = {"indicative", "conditional", "imperative", "potential"}
SUBJEKTIT = {"nsubj", "nsubj:cop", "nsubj:pass", "csubj", "csubj:cop"}


@lru_cache(maxsize=None)
def _voikko():
    import libvoikko
    return libvoikko.Voikko("fi")


@lru_cache(maxsize=100_000)
def voikko_finiittinen(sana: str, tuntematon: bool = True) -> bool:
    """Onko Voikolla sanalle finiittinen analyysi (moduksellinen muoto tai kieltosana).
    Tuntemattomalle sanalle palautetaan `tuntematon`."""
    analyysit = _voikko().analyze(sana)
    if not analyysit:
        return tuntematon
    return any(a.get("CLASS") == "kieltosana" or a.get("MOOD") in FINIITTISET_MODUKSET
               for a in analyysit)


def on_lausesuhde(deprel: str) -> bool:
    return deprel in LAUSESUHTEET or deprel.startswith("csubj")


def lapset(v: Virke) -> list[list[int]]:
    tulos: list[list[int]] = [[] for _ in v.tokenit]
    for t in v.tokenit:
        if t.head:
            tulos[t.head - 1].append(t.i)
    return tulos


def _fin_token(v: Virke, i: int) -> bool:
    t = v.tokenit[i]
    return t.feats.get("VerbForm") == "Fin" and voikko_finiittinen(t.teksti)


def finiittinen(v: Virke, paa: int, lps: list[list[int]] | None = None) -> bool:
    lps = lps or lapset(v)
    if v.tokenit[paa].deprel == "acl" and not any(v.tokenit[c].deprel == "mark" for c in lps[paa]):
        return False        # partisiippimääre (liittyvät pelkosi), vaikka merkitty Fin
    if _fin_token(v, paa):
        return True
    for c in lps[paa]:
        t = v.tokenit[c]
        if t.deprel.split(":")[0] in ("aux", "cop") and (
                _fin_token(v, c) or voikko_finiittinen(t.teksti, tuntematon=False)):
            return True         # Stanza voi merkitä apuverbin väärin (pitää: Inf)
        if t.deprel == "mark" and t.lemma.lower() in ALISTUS_MARK:
            return True
    return False


def alipuu(lps: list[list[int]], i: int) -> list[int]:
    tulos, pino = [], [i]
    while pino:
        x = pino.pop()
        tulos.append(x)
        pino.extend(lps[x])
    return sorted(tulos)


def janne(v: Virke, paa: int, lps: list[list[int]]) -> tuple[int, int, bool]:
    """Alipuun ensimmäinen ja viimeinen ei-välimerkkitoken sekä jatkuvuus."""
    puu = [i for i in alipuu(lps, paa) if v.tokenit[i].upos != "PUNCT" or i == paa]
    if not puu:
        return paa, paa, True
    jatkuva = puu[-1] - puu[0] + 1 == len(puu) or all(
        v.tokenit[i].upos == "PUNCT" for i in range(puu[0], puu[-1] + 1) if i not in puu)
    return puu[0], puu[-1], jatkuva


def _persoona_tai_passiivi(v: Virke, paa: int, lps: list[list[int]]) -> tuple[str | None, bool]:
    ehdokkaat = [paa] + [c for c in lps[paa] if v.tokenit[c].deprel.split(":")[0] in ("aux", "cop")]
    persoona, passiivi = None, False
    for i in ehdokkaat:
        f = v.tokenit[i].feats
        if f.get("Voice") == "Pass" and f.get("VerbForm") in ("Fin", "Part") and not (
                f.get("VerbForm") == "Part" and i == paa and len(ehdokkaat) == 1):
            passiivi = True     # myös perfektin passiivi: on singottu (Part + aux)
        if f.get("VerbForm") == "Fin" and f.get("Person") and persoona is None:
            persoona = f["Person"]
    return persoona, passiivi


def _on_subjekti(v: Virke, i: int, lps: list[list[int]]) -> bool:
    return any(v.tokenit[c].deprel in SUBJEKTIT for c in lps[i])


def _tyyppi(v: Virke, paa: int, alku: int) -> str:
    d = v.tokenit[paa].deprel
    if d == "root":
        return "paa"
    if d in ("conj", "parataxis"):
        return "rinnasteinen"
    if d == "acl:relcl":
        return "relatiivi"
    eka = v.tokenit[alku]
    if (d == "ccomp" or d.startswith("csubj")) and (
            eka.feats.get("PronType") == "Int" or "Ko" in eka.feats.get("Clitic", "")
            or eka.teksti.lower() in KYSYMYSSANAT
            or d == "ccomp" and eka.feats.get("PronType") == "Rel"):
        return "kysymys"
    if d.startswith("csubj") and eka.feats.get("PronType") == "Rel":
        return "relatiivi"
    return "sivu"


def _vapaa(v: Virke, paa: int, alku: int, loppu: int) -> bool:
    """S2b: vapaasti viittaava lause, ei epäsuora kysymys (mitä haluat, mistä tahansa vain pystyi)."""
    d = v.tokenit[paa].deprel
    if d not in ("ccomp", "acl:relcl", "advcl") and not d.startswith("csubj"):
        return False
    eka = v.tokenit[alku]
    if eka.teksti.lower() not in VAPAA_ALOITTAJAT:
        return False
    if any(t.teksti.lower() in VAPAA_JALKISANAT for t in v.tokenit[alku + 1:loppu + 1]):
        return True
    ed = v.tokenit[alku - 1] if alku > 0 else None
    if ed is not None and ed.feats.get("Degree") == "Cmp":
        return True             # paljon paremmalla mitä alkoholi koskaan oli
    yl = v.tokenit[v.tokenit[paa].head - 1] if v.tokenit[paa].head > 0 else None
    return d in ("ccomp", "acl:relcl") and yl is not None and yl.lemma.lower() in VAPAA_RELATIIVIN_VERBIT


def _aloittaja(v: Virke, alku: int) -> int | None:
    t = v.tokenit[alku]
    if t.deprel in ("mark", "cc") or t.feats.get("PronType") in ("Rel", "Int") \
            or "Ko" in t.feats.get("Clitic", "") or t.lemma.lower() in ("joten", "jolloin") \
            or t.teksti.lower() in KYSYMYSSANAT:
        return alku
    return None


def _ylempi_lause(v: Virke, i: int, paat: set[int]) -> int | None:
    h = v.tokenit[i].head
    while h:
        if h - 1 in paat:
            return h - 1
        h = v.tokenit[h - 1].head
    return None


def lauseista(v: Virke) -> tuple[list[Lause], list[Raja]]:
    """Virkkeen lauseet (myös ei-finiittiset ehdokkaat) ja finiittisten lauseiden rajat."""
    lps = lapset(v)
    ehdokkaat = [t.i for t in v.tokenit if on_lausesuhde(t.deprel)]
    fin = {i: finiittinen(v, i, lps) for i in ehdokkaat}
    # conj on lause vain, jos sen pää on finiittinen (muuten luettelon jäsen)
    paat = {i for i in ehdokkaat if fin[i] or v.tokenit[i].deprel == "root"}
    ensimmainen = next((t.i for t in v.tokenit if t.upos != "PUNCT"), 0)

    lauseet: dict[int, Lause] = {}
    for i in ehdokkaat:
        alku, loppu, jatkuva = janne(v, i, lps)
        persoona, passiivi = _persoona_tai_passiivi(v, i, lps)
        lauseet[i] = Lause(
            paa=i, alku=alku, loppu=loppu, tyyppi=_tyyppi(v, i, alku),
            deprel=v.tokenit[i].deprel, aloittaja=_aloittaja(v, alku),
            finiittinen=fin[i], taydellisyys="taydellinen", upotettu=False,
            virkkeen_alussa=alku == ensimmainen, projektiivinen=jatkuva,
            r1a=passiivi or persoona in ("1", "2") or "Ko" in v.tokenit[i].feats.get("Clitic", ""),
            ylempi=_ylempi_lause(v, i, paat), vapaa=_vapaa(v, i, alku, loppu))

    for i, l in lauseet.items():
        if l.ylempi is not None:
            yl = lauseet[l.ylempi]
            l.upotettu = yl.loppu > l.loppu
        if l.deprel in ("conj", "parataxis") and i in paat:
            l.taydellisyys = _taydellisyys(v, l, lauseet, lps)

    rajat: list[Raja] = []
    for i in sorted(paat):
        l = lauseet[i]
        if l.deprel == "root" or not l.projektiivinen:
            continue
        yl = lauseet.get(l.ylempi) if l.ylempi is not None else None
        if yl is not None and not yl.finiittinen and v.tokenit[yl.paa].upos in ("VERB", "AUX"):
            continue            # ylempi verbi ei-finiittinen (auttaaksemme): puu todennäköisesti väärin
        if l.alku > ensimmainen:
            rajat.append(Raja(l.alku, "alku", l, yl, v.rako[l.alku]))
        if l.upotettu:
            rajat.append(Raja(l.loppu + 1, "loppu", l, yl, v.rako[l.loppu + 1]))
    rajat.sort(key=lambda r: (r.rako, r.laji))
    return list(lauseet.values()), rajat


def _eksistentiaalinen(v: Virke, i: int, lps) -> bool:
    """Eksistentiaalilause: partitiivinen nominipää + olla-kopula (ei ole mitään syytä)."""
    t = v.tokenit[i]
    return (t.upos in ("NOUN", "PRON") and t.feats.get("Case") == "Par"
            and any(v.tokenit[c].deprel == "cop" and v.tokenit[c].lemma == "olla" for c in lps[i]))


def _taydellisyys(v: Virke, l: Lause, lauseet: dict[int, Lause], lps) -> str:
    if _on_subjekti(v, l.paa, lps) or _eksistentiaalinen(v, l.paa, lps):
        return "taydellinen"
    if l.r1a:
        return "taydellinen"
    # ei predikaattia: eliptinen rinnastus (eikä synti, eikä päinvastoin) ei ole oma päälauseensa
    paa = v.tokenit[l.paa]
    if paa.upos not in ("VERB", "AUX") and not any(
            v.tokenit[c].deprel in ("cop", "aux") and v.tokenit[c].upos in ("VERB", "AUX")
            and v.tokenit[c].lemma.lower() != "ei" for c in lps[l.paa]):
        return "vajaa"
    # yhteinen subjekti voi olla ylempänä ketjussa: hän ei pysty lopettamaan ja jatkaa
    ed = paa.head - 1
    while ed >= 0:
        if _on_subjekti(v, ed, lps):
            return "vajaa"
        ed = v.tokenit[ed].head - 1
    return "ratkaisematon"


def sulkeet(v: Virke, lauseet: list[Lause]) -> str:
    """Virke lausesuluin tarkistusta varten: [Kun tulin kotiin]advcl , [söin]root ."""
    avaa: dict[int, list[str]] = {}
    sulje: dict[int, list[str]] = {}
    for l in sorted(lauseet, key=lambda l: (l.alku, -l.loppu)):
        if not l.finiittinen and l.deprel != "root":
            continue
        avaa.setdefault(l.alku, []).append("[")
        sulje.setdefault(l.loppu, []).insert(0, "]" + l.deprel)
    osat = []
    for t in v.tokenit:
        if v.rako[t.i]:
            osat.append(v.rako[t.i])
        osat.append("".join(avaa.get(t.i, [])) + t.teksti + "".join(sulje.get(t.i, [])))
    if v.rako[len(v.tokenit)]:
        osat.append(v.rako[len(v.tokenit)])
    return " ".join(osat)
