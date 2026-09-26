"""Jokainen säännöissä käytetty koodi on rekisterissä ja päinvastoin."""
import os
import re

from pylkutus.saannot import SAANNOT

HAK = os.path.join(os.path.dirname(__file__), "..", "..", "pylkutus", "saannot")
KOODI = re.compile(r'(?:\(|Paatos\([^,]+, )"([A-Z]\d[a-z]?|1\.15)"')


def _kaytetyt() -> set[str]:
    koodit = set()
    for nimi in ("puuttuvat.py", "sanasto.py", "ylimaaraiset.py"):
        with open(os.path.join(HAK, nimi), encoding="utf-8") as f:
            teksti = f.read()
        koodit |= set(KOODI.findall(teksti))
        koodit |= set(re.findall(r'"(A[12])"', teksti))
        koodit |= set(re.findall(r'"(S2a|S1e|K3)"', teksti))
    return koodit


def test_kaytetyt_rekisterissa():
    assert _kaytetyt() - set(SAANNOT) == set()


def test_rekisteri_kaytossa():
    assert set(SAANNOT) - _kaytetyt() == set()
