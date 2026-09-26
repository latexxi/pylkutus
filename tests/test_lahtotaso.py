import os

import pytest

from pylkutus.lahtotaso import sanalista, vanha, VANHA


def paikat(varoitukset, teksti):
    return [teksti[v.alku:].split()[0] for v in varoitukset]


@pytest.mark.parametrize("teksti,odotus", [
    ("Hän sanoi että hän tulee huomenna.", ["että"]),
    ("Hän sanoi, että hän tulee huomenna.", []),
    ("Tee se joka päivä kahden viikon ajan.", []),
    ("Haluan työpaikan joka sopii minulle.", ["joka"]),
    ("Hän sanoi, että jos ehtii, hän tulee.", []),          # S1b
    ("Soitan heti kun pääsen kotiin illalla.", ["heti"]),     # M1: ilmauksen eteen
    ("Soitan, heti kun pääsen kotiin illalla.", []),
    ("Soitan heti, kun pääsen kotiin illalla.", []),
    ("Kun tulin kotiin söin.", []),                           # virkkeen alku
    ("Joka tahansa voi tulla ja mennä.", []),
    ("Kävin kaupassa ja jos ehdin, myös kirjastossa.", []),
    ("Jatkat inventaaria ja aina kun olet väärässä, myönnät sen.", []),
])
def test_sanalista(teksti, odotus):
    assert paikat(sanalista(teksti), teksti) == odotus


@pytest.mark.skipif(not os.path.exists(VANHA), reason="vanha skripti puuttuu")
def test_vanha_osoittaa_oikeaan_sanaan():
    teksti = "Ensimmäinen kappale on tässä.\n\nMinisteri totesi että asia on käsitelty loppuun asti."
    v = vanha(teksti)
    assert paikat(v, teksti) == ["että"]
    assert v[0].saanto.startswith("vanha/")
