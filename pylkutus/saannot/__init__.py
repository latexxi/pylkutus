"""Sääntörekisteri: toteutettujen sääntöjen koodit, kuvaukset ja ohjepankin luvut.

Säännöt itse: puuttuvat.py (lauserajat), sanasto.py (sanastoon perustuvat rakopäätökset),
ylimaaraiset.py (ylimääräiset pilkut). Koodit ja luvut: PLAN_PILKKU.md luku 1.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Saanto:
    koodi: str
    luku: str
    kuvaus: str


SAANNOT: dict[str, Saanto] = {s.koodi: s for s in [
    Saanto("S1", "1.1", "alistuskonjunktiolla alkava sivulause erotetaan pilkulla"),
    Saanto("S1a", "1.1", "hyvin lyhyt virke: pilkku valinnainen"),
    Saanto("S1b", "1.1", "kahden peräkkäisen konjunktion väliin ei pilkkua"),
    Saanto("S1e", "1.1", "keskellä virkettä olevan sivulauseen loppuun pilkku"),
    Saanto("M1", "1.2", "moniosainen konjunktioilmaus: pilkku ilmauksen eteen tai osien väliin"),
    Saanto("M3", "1.2", "moniosainen ilmaus rinnastuskonjunktion jälkeen: ei pilkkua"),
    Saanto("S2", "1.3", "relatiivilause erotetaan pilkulla"),
    Saanto("S2a", "1.3", "upotetun relatiivilauseen loppuun pilkku"),
    Saanto("K1", "1.4", "se, joka / se, mitä: pilkku se-pronominin jälkeen"),
    Saanto("K2", "1.4", "virkkeen alussa se(,) joka: pilkku valinnainen"),
    Saanto("K3", "1.4", "se joka -lauseen loppuun pilkku ennen päälauseen jatkoa"),
    Saanto("S2b", "1.3", "vapaasti viittaava lause (mitä haluat, mistä tahansa): pilkku valinnainen"),
    Saanto("S3", "1.5", "epäsuora kysymyslause erotetaan pilkulla"),
    Saanto("S4", "1.6", "rinnasteiset sivulauseet ja/tai-sanan kohdalla: ei pilkkua"),
    Saanto("S6", "1.6", "rinnasteiset lauseet ilman konjunktiota: pilkku"),
    Saanto("R1", "1.7", "täydelliset päälauseet erotetaan pilkulla myös ja/tai-sanan edellä"),
    Saanto("R1a", "1.7", "1./2. persoona tai passiivi: R1:n pilkku valinnainen"),
    Saanto("R2", "1.7", "vajaat päälauseet ja-sanan kohdalla: ei pilkkua"),
    Saanto("R3", "1.7", "mutta/vaan: täydellinen lause pilkku, vajaa valinnainen"),
    Saanto("R4", "1.7", "sillä-lause erotetaan aina pilkulla"),
    Saanto("P4", "1.8", "parirakenne sekä … että: ei pilkkua"),
    Saanto("V1", "1.9", "vertailun kuin-sanan edellä ei pilkkua; niin kuin -vertaus: valinnainen"),
    Saanto("V2", "1.9", "ennen kuin päälauseen jäljessä: pilkku valinnainen"),
    Saanto("V5", "1.9", "kuten = niin kuin: pilkku, jos kuten-jakso on lause"),
    Saanto("L1", "1.10", "lauseenvastiketta ei eroteta pilkulla"),
    Saanto("A1", "1.11", "lauseen alun asennesanan jälkeen ei tavallisesti pilkkua"),
    Saanto("A2", "1.11", "järjestyssanan (ensiksi, toiseksi) jälkeen ei tavallisesti pilkkua"),
    Saanto("1.15", "1.15", "ajatusviiva, sulkeet, kaksoispiste tai puolipiste korvaa pilkun"),
]}


def listaus() -> str:
    return "\n".join(f"{s.koodi:<5} {s.luku:<5} {s.kuvaus}" for s in SAANNOT.values())
