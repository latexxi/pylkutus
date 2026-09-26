"""Moduuli 5: raportoija (PLAN_PILKKU.md 3.7, 7.3/V8)."""
from __future__ import annotations

from .tyypit import Leipateksti, Varoitus

VARMUUS = {"low": 0, "medium": 1, "high": 2}


def suodata(varoitukset: list[Varoitus], min_varmuus: str = "low",
            saannot: set[str] | None = None) -> list[Varoitus]:
    return [v for v in varoitukset
            if VARMUUS[v.varmuus] >= VARMUUS[min_varmuus]
            and (not saannot or v.saanto in saannot)]


def konteksti(teksti: str, v: Varoitus, leveys: int = 40) -> str:
    """Varoituksen ympäristö: pilkun paikka merkitty ‸ (lisää) tai [,] (poista)."""
    a = max(0, v.alku - leveys)
    b = min(len(teksti), v.alku + 1 + leveys)
    if v.toimenpide == "lisaa":
        s = teksti[a:v.alku] + "‸" + teksti[v.alku:b]
    else:
        s = teksti[a:v.alku] + "[,]" + teksti[v.alku + 1:b]
    alku = "…" if a > 0 else ""
    loppu = "…" if b < len(teksti) else ""
    return alku + s.replace("\n", " ") + loppu


def raportoi(varoitukset: list[Varoitus], leipa: Leipateksti, polku: str) -> str:
    rivit = []
    for v in sorted(varoitukset, key=lambda v: v.alku):
        rivi, sarake = leipa.rivi_sarake(min(v.alku, len(leipa.teksti) - 1))
        rivit.append(f"{polku}:{rivi}:{sarake}: [{v.varmuus}/{v.saanto}] {v.viesti}")
        rivit.append(f"    {konteksti(leipa.teksti, v)}")
    return "\n".join(rivit)


def yhteenveto(varoitukset: list[Varoitus]) -> str:
    laskut: dict[str, int] = {}
    for v in varoitukset:
        laskut[v.varmuus] = laskut.get(v.varmuus, 0) + 1
    osat = [f"{k}={laskut[k]}" for k in ("high", "medium", "low") if k in laskut]
    return f"Yhteensä {len(varoitukset)} varoitusta" + (": " + ", ".join(osat) if osat else "")
