import os
import subprocess
import sys
import time

import pytest

from pylkutus.esikasittelija import lue_md
from pylkutus.raportoija import raportoi, suodata
from pylkutus.tyypit import Varoitus

HAK = os.path.dirname(__file__)
JUURI = os.path.dirname(HAK)


def test_rivi_ja_sarake_md_merkinnan_jalkeen():
    leipa, _ = lue_md('# Otsikko\n\n<span id="a"></span>Hän sanoi että tulee.\n')
    o = leipa.teksti.index(" että")
    v = Varoitus("S1", "high", o, o + 1, "lisaa", 'pilkku puuttuu ennen sanaa "että" (S1)')
    rivi = raportoi([v], leipa, "t.md").splitlines()[0]
    assert rivi == 't.md:3:30: [high/S1] pilkku puuttuu ennen sanaa "että" (S1)'


def test_suodatus():
    vv = [Varoitus("S1", "high", 0, 1, "lisaa", ""), Varoitus("R1", "low", 0, 1, "lisaa", ""),
          Varoitus("S3", "medium", 0, 1, "lisaa", "")]
    assert [v.saanto for v in suodata(vv, "medium")] == ["S1", "S3"]
    assert [v.saanto for v in suodata(vv, "low", {"R1"})] == ["R1"]


def _aja(*args):
    return subprocess.run([sys.executable, "-m", "pylkutus", *args], cwd=JUURI,
                          capture_output=True, text=True, check=True)


@pytest.mark.stanza
def test_paasta_paahan():
    tulos = _aja("tests/fixtures/pieni.md")
    with open(os.path.join(HAK, "fixtures", "pieni.odotettu"), encoding="utf-8") as f:
        assert tulos.stdout == f.read()
    assert "Yhteensä 5 varoitusta" in tulos.stderr


@pytest.mark.stanza
def test_valimuisti_nopea():
    _aja("tests/fixtures/pieni.md")          # varmistaa välimuistin
    alku = time.time()
    _aja("tests/fixtures/pieni.md", "--min", "high")
    # välimuistista: ei Stanzan jäsennystä (Voikko ja tuonnit vievät alle sekunnin)
    assert time.time() - alku < 3
