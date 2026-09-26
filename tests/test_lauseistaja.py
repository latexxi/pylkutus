"""Lauseistajan testit V3:n jäädytetyillä jäsennyksillä (tests/fixtures/v3_A.conllu)."""
import os

import pytest

from pylkutus import conllu, lauseistaja as L

FIXTURE = os.path.join(os.path.dirname(__file__), "fixtures", "v3_A.conllu")


@pytest.fixture(scope="module")
def virkkeet():
    with open(FIXTURE, encoding="utf-8") as f:
        _, lauseet = conllu.lue(f.read())
    tulos = {}
    for l in lauseet:
        v = conllu.virkkeeksi(l)
        tulos[" ".join(t.teksti for t in v.tokenit)] = v
    return tulos


def hae(virkkeet, alku):
    osumat = [v for k, v in virkkeet.items() if k.startswith(alku)]
    assert len(osumat) == 1, alku
    return osumat[0]


def rajat(v):
    """[(sana raon jälkeen, laji, deprel, pilkku)]"""
    _, rr = L.lauseista(v)
    return [(v.tokenit[r.rako].teksti, r.laji, r.lause.deprel, r.merkki) for r in rr]


def lause(v, paasana):
    ls, _ = L.lauseista(v)
    osumat = [l for l in ls if v.tokenit[l.paa].teksti == paasana]
    assert len(osumat) == 1, paasana
    return osumat[0]


@pytest.mark.parametrize("alku,paa", [
    ("Hän lähti kun hän ei tullut", "tullut"),          # kielto: pää Part, aux Fin
    ("Odotimme koska hän on lähtenyt", "lähtenyt"),      # perfekti
    ("Hän ei ole rikas vaikka hän on opettaja", "opettaja"),  # kopula: pää NOUN
    ("Tiedän että hän ei ole tullut", "tullut"),
])
def test_finiittinen(virkkeet, alku, paa):
    assert lause(hae(virkkeet, alku), paa).finiittinen


@pytest.mark.parametrize("alku,paa", [
    ("Kotiin tultuaan", "tultuaan"),
    ("Hän pyysi neuvoani uskoen", "uskoen"),
    ("Asetuttuaan Mikkeliin", "Asetuttuaan"),
    ("Ensiksi auttaaksemme", "auttaaksemme"),            # Stanza: Fin, Voikko kumoaa
])
def test_lauseenvastike_ei_finiittinen(virkkeet, alku, paa):
    assert not lause(hae(virkkeet, alku), paa).finiittinen


def test_lauseenvastike_ei_rajaa(virkkeet):
    assert rajat(hae(virkkeet, "Kotiin tultuaan")) == []
    assert rajat(hae(virkkeet, "Ensiksi auttaaksemme")) == []
    assert rajat(hae(virkkeet, "Hän pyysi neuvoani uskoen")) == [("että", "alku", "ccomp", ",")]


def test_loppupilkku_alussa_oleva_sivulause(virkkeet):
    assert rajat(hae(virkkeet, "Kun tulin kotiin")) == [("söin", "loppu", "advcl", ",")]


def test_sisakkaiset_sivulauseet(virkkeet):
    assert rajat(hae(virkkeet, "Hän sanoi että jos ehtii")) == [
        ("että", "alku", "ccomp", ","),
        ("jos", "alku", "advcl", None),
        ("hän", "loppu", "advcl", ","),
    ]


def test_upotettu_relatiivilause(virkkeet):
    v = hae(virkkeet, "Pelaajat joiden")
    assert rajat(v) == [("joiden", "alku", "acl:relcl", ","), ("neuvottelevat", "loppu", "acl:relcl", ",")]
    assert lause(v, "mainittu").upotettu


def test_se_mita(virkkeet):
    v = hae(virkkeet, "Se mitä tapahtui")
    l = lause(v, "tapahtui")
    assert l.deprel == "acl:relcl" and l.tyyppi == "relatiivi" and l.upotettu
    assert rajat(v) == [("mitä", "alku", "acl:relcl", None), ("oli", "loppu", "acl:relcl", ",")]


def test_korrelaatiton_subjektilause(virkkeet):
    v = hae(virkkeet, "Mitä tapahtui oli")
    l = lause(v, "tapahtui")
    assert l.deprel.startswith("csubj") and l.virkkeen_alussa
    assert rajat(v) == [("oli", "loppu", "csubj:cop", ",")]


@pytest.mark.parametrize("alku,paa,odotus,r1a", [
    ("Perhe kunnosti", "viimeisteli", "vajaa", False),
    ("Kesäkuussa he", "Kanadassa", "taydellinen", False),
    ("Tulin kotiin ja söin", "söin", "taydellinen", True),
    ("Tämä kauna oli", "näytti", "taydellinen", False),
    ("Aviomieheni palasi lopulta mutta ei kestänyt kauaa .", "kestänyt", "vajaa", False),
    ("Talo rakennettiin", "myytiin", "taydellinen", True),
    ("Salilla on hiljaista", "käy", "taydellinen", False),
])
def test_taydellisyys(virkkeet, alku, paa, odotus, r1a):
    l = lause(hae(virkkeet, alku), paa)
    assert l.tyyppi == "rinnasteinen"
    assert (l.taydellisyys, l.r1a) == (odotus, r1a)


@pytest.mark.parametrize("alku,sana", [
    ("Emme tienneet", "oliko"),
    ("Tämä auttaa sinua", "mistä"),
    ("Kukaan ei tiedä", "missä"),
    ("Tee se joka päivä", "mitä"),
])
def test_epasuora_kysymys(virkkeet, alku, sana):
    v = hae(virkkeet, alku)
    ls, _ = L.lauseista(v)
    kys = [l for l in ls if l.tyyppi == "kysymys"]
    assert len(kys) == 1 and v.tokenit[kys[0].alku].teksti == sana
    assert kys[0].aloittaja == kys[0].alku


def test_joka_jokainen_ei_lause(virkkeet):
    v = hae(virkkeet, "Tee se joka päivä")
    assert [r[0] for r in rajat(v)] == ["ja", "mitä"]


def test_sulkeet(virkkeet):
    v = hae(virkkeet, "Kun tulin kotiin")
    ls, _ = L.lauseista(v)
    assert L.sulkeet(v, ls) == "[[Kun tulin kotiin]advcl , söin]root ."


def test_yhdista():
    from pylkutus.tyypit import Raja
    a = [Raja(2, "alku", None, None, None), Raja(5, "loppu", None, None, None)]
    b = [Raja(2, "alku", None, None, None), Raja(7, "alku", None, None, None)]
    tulos = L.yhdista(a, b)
    assert [(r.rako, r.lahde) for r in tulos] == [(2, "AB"), (5, "A"), (7, "B")]


def test_partisiippimaare_ei_lause(virkkeet):
    v = hae(virkkeet, "Heti kun alat")
    assert not lause(v, "liittyvät").finiittinen
    assert [r[0] for r in rajat(v) if r[1] == "loppu"] == ["niihin"]


def test_eksistentiaalinen_rinnasteinen_taydellinen(virkkeet):
    v = hae(virkkeet, "Hän on jo tehnyt")
    l = lause(v, "syytä")
    assert l.tyyppi == "rinnasteinen" and l.taydellisyys == "taydellinen"
