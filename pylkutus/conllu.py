"""CoNLL-U-luku ja -kirjoitus sekä muunnos Virke-olioiksi.

Tallennetaan sanat (ei MWT-rivejä). MISC-sarakkeessa start_char/end_char leipätekstiin;
MWT:stä laajennetut sanat saavat koko tokenin välin.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .tyypit import Token, Virke


@dataclass
class Sana:
    id: int
    teksti: str
    lemma: str
    upos: str
    xpos: str
    feats: dict[str, str]
    head: int
    deprel: str
    alku: int
    loppu: int


@dataclass
class Lause:
    sanat: list[Sana]
    kommentit: list[str] = field(default_factory=list)


def _feats_str(feats: dict[str, str]) -> str:
    return "|".join(f"{k}={v}" for k, v in sorted(feats.items())) or "_"


def _feats_dict(s: str) -> dict[str, str]:
    if s == "_" or not s:
        return {}
    return dict(kv.split("=", 1) for kv in s.split("|"))


def kirjoita(lauseet: list[Lause], otsake: list[str] | None = None) -> str:
    rivit = [f"# {o}" for o in (otsake or [])]
    for l in lauseet:
        rivit.extend(f"# {k}" for k in l.kommentit)
        for s in l.sanat:
            rivit.append("\t".join([
                str(s.id), s.teksti, s.lemma or "_", s.upos or "_", s.xpos or "_",
                _feats_str(s.feats), str(s.head), s.deprel or "_", "_",
                f"start_char={s.alku}|end_char={s.loppu}"]))
        rivit.append("")
    return "\n".join(rivit) + "\n"


def lue(teksti: str) -> tuple[list[str], list[Lause]]:
    """Palauttaa (tiedoston otsakekommentit, lauseet)."""
    otsake: list[str] = []
    lauseet: list[Lause] = []
    nyk = Lause([])
    ensimmainen = True
    for rivi in teksti.split("\n"):
        if not rivi.strip():
            if nyk.sanat:
                lauseet.append(nyk)
                nyk = Lause([])
            ensimmainen = False
            continue
        if rivi.startswith("#"):
            (otsake if ensimmainen and not nyk.sanat else nyk.kommentit).append(rivi[1:].strip())
            continue
        ensimmainen = False
        c = rivi.split("\t")
        misc = dict(kv.split("=", 1) for kv in c[9].split("|") if "=" in kv)
        nyk.sanat.append(Sana(int(c[0]), c[1], "" if c[2] == "_" else c[2],
                              "" if c[3] == "_" else c[3], "" if c[4] == "_" else c[4],
                              _feats_dict(c[5]), int(c[6]), "" if c[7] == "_" else c[7],
                              int(misc["start_char"]), int(misc["end_char"])))
    if nyk.sanat:
        lauseet.append(nyk)
    return otsake, lauseet


def on_pilkku(s: Sana) -> bool:
    return s.teksti == "," and s.upos in ("PUNCT", "")


def virkkeeksi(lause: Lause) -> Virke:
    """Poistaa pilkut tokeneista ja siirtää ne rakoihin. Päät numeroidaan uudelleen.
    Jos sanan pää on pilkku, pääksi tulee pilkun pää (ketjutetaan)."""
    sanat = lause.sanat
    id_sana = {s.id: s for s in sanat}
    uusi_id: dict[int, int] = {}
    tokenit: list[Token] = []
    rako: list[str | None] = []
    pilkku_edella = False
    for s in sanat:
        if on_pilkku(s):
            pilkku_edella = True
            continue
        rako.append("," if pilkku_edella else None)
        pilkku_edella = False
        uusi_id[s.id] = len(tokenit) + 1
        tokenit.append(Token(len(tokenit), s.teksti, s.alku, s.loppu, s.lemma, s.upos,
                             dict(s.feats), s.head, s.deprel))
    rako.append("," if pilkku_edella else None)
    for t in tokenit:
        h = t.head
        nahty = set()
        while h and on_pilkku(id_sana[h]) and h not in nahty:
            nahty.add(h)
            h = id_sana[h].head
        t.head = uusi_id.get(h, 0) if h else 0
    return Virke(tokenit, rako)
