"""Moduuli 2: Stanza-jäsennys (PLAN_PILKKU.md 3.4, 7.3/V5).

Jäsennetään vain alkuperäinen teksti pilkkuineen. Pilkuton rinnakkaisjäsennys (B) poistettiin:
se ei vaikuttanut varoituksiin (kokeet/tulokset.md, PLAN_KORJAUKSET.md K1)."""
from __future__ import annotations

import hashlib
import os

from . import conllu
from .conllu import ConlluVirke, Sana
from .sanastot import LYHENTEET
from .tyypit import Leipateksti, Virke

PROSESSORIT = "tokenize,mwt,pos,lemma,depparse"
VALIMUISTI = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".cache")

_putket: dict[object, object] = {}


VIRKEJAKO_VERSIO = 2   # kasvatetaan, kun tokenisointi tai virkejaon korjaus muuttuu


def versiot() -> str:
    import stanza, torch
    return (f"stanza={stanza.__version__} torch={torch.__version__} malli=fi/default "
            f"virkejako={VIRKEJAKO_VERSIO}")


def putki(pretokenized: bool = False):
    if pretokenized not in _putket:
        import stanza
        import torch
        torch.use_deterministic_algorithms(True, warn_only=True)
        _putket[pretokenized] = stanza.Pipeline(
            "fi", processors=PROSESSORIT, use_gpu=False, verbose=False,
            download_method=None, tokenize_pretokenized=pretokenized)
    return _putket[pretokenized]


def _stanzasta(doc, valit: list[list[tuple[int, int]]] | None = None) -> list[ConlluVirke]:
    """Stanza-dokumentti CoNLL-U-lauseiksi. Jos valit on annettu (pretokenisoitu syöte),
    sanojen offsetit otetaan niistä, koska Stanza laskee ne syötteen omasta tekstistä."""
    lauseet = []
    for n, sent in enumerate(doc.sentences):
        sanat = []
        for k, tok in enumerate(sent.tokens):
            alku, loppu = valit[n][k] if valit else (tok.start_char, tok.end_char)
            for w in tok.words:
                sanat.append(Sana(
                    w.id, w.text, w.lemma or "", w.upos or "", w.xpos or "",
                    conllu._feats_dict(w.feats or "_"), w.head or 0, w.deprel or "",
                    alku, loppu))
        lauseet.append(ConlluVirke(sanat))
    return lauseet


Sanavirke = list[tuple[str, int, int]]   # (sana, alku, loppu)


def tokenisoi(teksti: str) -> list[Sanavirke]:
    """Vaihe 1: Stanzan tokenisointi ja MWT. MWT-tokenin sanat saavat tokenin välin."""
    import stanza
    if "tok" not in _putket:
        _putket["tok"] = stanza.Pipeline("fi", processors="tokenize,mwt", use_gpu=False,
                                         verbose=False, download_method=None)
    doc = _putket["tok"](teksti)
    return [[(w.text, tok.start_char, tok.end_char) for tok in sent.tokens for w in tok.words]
            for sent in doc.sentences]


def _on_lyhenne(sana: str) -> bool:
    return sana.lower() in LYHENTEET or (len(sana) == 1 and sana.isupper())


PAATEMERKIT = {".", "!", "?", "…", ":", ";", "...", "!?", "?!"}
LOPPULAINAUS = {'"', "”", "»", ")", "'"}


def _paattyy(virke: Sanavirke) -> bool:
    """Päättyykö virke loppumerkkiin (myös lainausmerkin tai sulkeen sisällä)."""
    viim = virke[-1][0]
    if viim in PAATEMERKIT or (viim.endswith(".") and len(viim) > 1):
        return True
    if viim in LOPPULAINAUS and len(virke) > 1:
        ed = virke[-2][0]
        return ed in PAATEMERKIT or ed in LOPPULAINAUS
    return False


def korjaa_virkejako(virkkeet: list[Sanavirke], teksti: str) -> list[Sanavirke]:
    """Vaihe 2: yhdistää lyhenteen ja pisteen yhdeksi sanaksi ja virheellisesti katkaistut
    virkkeet. Virke jatkuu, jos edellinen päättyy lyhenteeseen tai nimikirjaimeen ja
    pisteeseen, jos edellinen ei pääty loppumerkkiin (Stanza katkaisee isoon alkukirjaimeen:
    "ymmärrät ‖ Isoa kirjaa") tai jos seuraava alkaa pienellä kirjaimella. Virke ei koskaan
    jatku kappalerajan yli."""
    # lyhenne + piste samaksi sanaksi (vain jos piste on heti perässä)
    yhdistetyt: list[Sanavirke] = []
    for v in virkkeet:
        uusi: Sanavirke = []
        for sana in v:
            if (sana[0] == "." and uusi and uusi[-1][2] == sana[1]
                    and _on_lyhenne(uusi[-1][0])):
                edellinen = uusi.pop()
                uusi.append((edellinen[0] + ".", edellinen[1], sana[2]))
            else:
                uusi.append(sana)
        yhdistetyt.append(uusi)
    tulos: list[Sanavirke] = []
    for v in yhdistetyt:
        if tulos and v:
            ed = tulos[-1]
            kappaleraja = "\n\n" in teksti[ed[-1][2]:v[0][1]]
            jatkuu = (ed[-1][0].endswith(".") and len(ed[-1][0]) > 1
                      and _on_lyhenne(ed[-1][0][:-1]))
            ensimmainen = v[0][0]
            jatkuu = jatkuu or ensimmainen[:1].islower() or not _paattyy(ed)
            if not kappaleraja and jatkuu:
                ed.extend(v)
                continue
        tulos.append(list(v))
    return tulos


def jasenna_sanat(virkkeet: list[Sanavirke], poista_pilkut: bool = False) -> list[ConlluVirke]:
    """Vaihe 3: jäsennys valmiiksi pilkotuista sanoista (pilkut mukana tai ilman)."""
    if poista_pilkut:
        virkkeet = [[s for s in v if s[0] != ","] for v in virkkeet]
    doc = putki(True)([[s[0] for s in v] for v in virkkeet])
    return _stanzasta(doc, [[(s[1], s[2]) for s in v] for v in virkkeet])


def jasenna_teksti(teksti: str) -> list[ConlluVirke]:
    return jasenna_sanat(korjaa_virkejako(tokenisoi(teksti), teksti))


def _avain(teksti: str) -> str:
    return hashlib.sha256((versiot() + "\n" + teksti).encode("utf-8")).hexdigest()[:16]


def _siirra(virkkeet: list[ConlluVirke], siirto: int) -> list[ConlluVirke]:
    for v in virkkeet:
        for s in v.sanat:
            s.alku += siirto
            s.loppu += siirto
    return virkkeet


def _kappaleittain(virkkeet: list[ConlluVirke], alut: list[int]) -> list[list[ConlluVirke]]:
    """Jakaa virkkeet kappaleisiin ensimmäisen sanan offsetin mukaan (alut nousevina)."""
    tulos: list[list[ConlluVirke]] = [[] for _ in alut]
    k = 0
    for v in virkkeet:
        while k + 1 < len(alut) and v.sanat[0].alku >= alut[k + 1]:
            k += 1
        tulos[k].append(v)
    return tulos


def jasenna(leipa: Leipateksti, valimuisti: str | None = VALIMUISTI) -> list[ConlluVirke]:
    """Palauttaa jäsennyksen CoNLL-U-lauseina.

    Välimuisti on kappalekohtainen (avain = kappaleen teksti ja versiot, offsetit kappaleen
    alusta), joten muokattu kappale jäsennetään uudelleen yksinään. Virkejaon korjaus ei ylitä
    kappalerajaa, joten tulos on sama kuin koko tekstin jäsennyksessä. Puuttuvat kappaleet
    jäsennetään yhdessä erässä."""
    kappaleet = leipa.kappaleet or [(0, len(leipa.teksti))]
    tekstit = [leipa.teksti[a:b] for a, b in kappaleet]
    hakemisto = os.path.join(valimuisti, "kappaleet") if valimuisti else None
    polut = [os.path.join(hakemisto, _avain(t) + ".conllu") if hakemisto else None
             for t in tekstit]
    tulos: list[list[ConlluVirke] | None] = [None] * len(kappaleet)
    for n, polku in enumerate(polut):
        if polku and os.path.exists(polku):
            with open(polku, encoding="utf-8") as f:
                tulos[n] = conllu.lue(f.read())[1]
    puuttuvat = [n for n, t in enumerate(tulos) if t is None]
    if puuttuvat:
        alut, osat, pituus = [], [], 0
        for n in puuttuvat:
            alut.append(pituus)
            osat.append(tekstit[n])
            pituus += len(tekstit[n]) + 2
        uudet = _kappaleittain(jasenna_teksti("\n\n".join(osat)), alut)
        for n, alku, virkkeet_ in zip(puuttuvat, alut, uudet):
            tulos[n] = _siirra(virkkeet_, -alku)
            if polut[n]:
                os.makedirs(hakemisto, exist_ok=True)
                with open(polut[n], "w", encoding="utf-8") as f:
                    f.write(conllu.kirjoita(tulos[n], [versiot()]))
    return [v for (alku, _), virkkeet_ in zip(kappaleet, tulos)
            for v in _siirra(virkkeet_, alku)]


def virkkeet(lauseet: list[ConlluVirke]) -> list[Virke]:
    return [conllu.virkkeeksi(l) for l in lauseet]


def tarkista(leipa: Leipateksti, a: list[ConlluVirke]) -> list[str]:
    """Invariantti: sanojen offsetit osuvat tekstiin."""
    virheet = []
    for n, lause in enumerate(a):
        for s in lause.sanat:
            pala = leipa.teksti[s.alku:s.loppu]
            if not pala or (pala != s.teksti and len(pala) == len(s.teksti)
                            and pala.lower() != s.teksti.lower()):
                virheet.append(f"virke {n}: sana {s.teksti!r} osoittaa tekstiin {pala!r}")
    return virheet
