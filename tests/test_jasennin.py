import os

import pytest

from pylkutus import conllu
from pylkutus.conllu import Sana, Lause
from pylkutus.jasennin import korjaa_virkejako

LAHDE = os.path.expanduser("~/Documents/ratkaisu/2026-09-14 ratkaisu.md")


def S(id, teksti, head, deprel, alku, upos="X"):
    return Sana(id, teksti, teksti.lower(), upos, "", {}, head, deprel, alku, alku + len(teksti))


# --- nopeat testit ---------------------------------------------------------

def test_conllu_edestakaisin():
    l = Lause([Sana(1, "Hän", "hän", "PRON", "Pron", {"Case": "Nom", "Person": "3"}, 2, "nsubj", 0, 3),
               Sana(2, "tuli", "tulla", "VERB", "V", {"VerbForm": "Fin"}, 0, "root", 4, 8)])
    teksti = conllu.kirjoita([l], ["versio"])
    otsake, lauseet = conllu.lue(teksti)
    assert otsake == ["versio"]
    assert lauseet[0].sanat == l.sanat


def test_pilkut_rakoihin():
    # Hän sanoi , että tulee .
    l = Lause([S(1, "Hän", 2, "nsubj", 0), S(2, "sanoi", 0, "root", 4),
               S(3, ",", 5, "punct", 9, "PUNCT"), S(4, "että", 5, "mark", 11),
               S(5, "tulee", 2, "ccomp", 16), S(6, ".", 2, "punct", 21, "PUNCT")])
    v = conllu.virkkeeksi(l)
    assert [t.teksti for t in v.tokenit] == ["Hän", "sanoi", "että", "tulee", "."]
    assert v.rako == [None, None, ",", None, None, None]
    assert [t.head for t in v.tokenit] == [2, 0, 4, 2, 2]


def test_pilkku_paana_ketjutetaan():
    l = Lause([S(1, "a", 0, "root", 0), S(2, ",", 1, "punct", 1, "PUNCT"),
               S(3, "b", 2, "conj", 3)])
    v = conllu.virkkeeksi(l)
    assert v.tokenit[1].head == 1


def test_virkejako_lyhenne_yhdistetaan():
    teksti = "Puhui tri. Virtanen."
    virkkeet = [[("Puhui", 0, 5), ("tri", 6, 9), (".", 9, 10)],
                [("Virtanen", 11, 19), (".", 19, 20)]]
    tulos = korjaa_virkejako(virkkeet, teksti)
    assert len(tulos) == 1
    assert [s[0] for s in tulos[0]] == ["Puhui", "tri.", "Virtanen", "."]


def test_virkejako_pieni_alkukirjain_jatkaa():
    teksti = '"Tuletko?" hän kysyi.'
    virkkeet = [[('"', 0, 1), ("Tuletko", 1, 8), ("?", 8, 9), ('"', 9, 10)],
                [("hän", 11, 14), ("kysyi", 15, 20), (".", 20, 21)]]
    assert len(korjaa_virkejako(virkkeet, teksti)) == 1


def test_virkejako_ei_ylita_kappaletta():
    teksti = "Tuli W.\n\nja meni."
    virkkeet = [[("Tuli", 0, 4), ("W", 5, 6), (".", 6, 7)], [("ja", 9, 11), ("meni", 12, 16), (".", 16, 17)]]
    assert len(korjaa_virkejako(virkkeet, teksti)) == 2


def test_virkejako_iso_alkukirjain_keskella():
    teksti = "Mitä paremmin ymmärrät Isoa kirjaa, sitä parempi."
    virkkeet = [[("Mitä", 0, 4), ("paremmin", 5, 13), ("ymmärrät", 14, 22)],
                [("Isoa", 23, 27), ("kirjaa", 28, 34), (",", 34, 35), ("sitä", 36, 40),
                 ("parempi", 41, 48), (".", 48, 49)]]
    assert len(korjaa_virkejako(virkkeet, teksti)) == 1


def test_virkejako_kaksoispiste_ja_lainaus_paattavat():
    teksti = 'Asia on: Iso kirja toimii. "Hyvä." Hän sanoi.'
    virkkeet = [[("Asia", 0, 4), ("on", 5, 7), (":", 7, 8)],
                [("Iso", 9, 12), ("kirja", 13, 18), ("toimii", 19, 25), (".", 25, 26)],
                [('"', 27, 28), ("Hyvä", 28, 32), (".", 32, 33), ('"', 33, 34)],
                [("Hän", 35, 38), ("sanoi", 39, 44), (".", 44, 45)]]
    assert len(korjaa_virkejako(virkkeet, teksti)) == 4


def test_virkejako_tavallinen_raja_sailyy():
    teksti = "Hän tuli. Hän meni."
    virkkeet = [[("Hän", 0, 3), ("tuli", 4, 8), (".", 8, 9)], [("Hän", 10, 13), ("meni", 14, 18), (".", 18, 19)]]
    assert len(korjaa_virkejako(virkkeet, teksti)) == 2


# --- Stanza-testit -----------------------------------------------------------

@pytest.fixture(scope="module")
def jasenna():
    from pylkutus import jasennin
    from pylkutus.esikasittelija import lue_teksti

    def f(teksti):
        leipa = lue_teksti(teksti)
        a, b = jasennin.jasenna(leipa, valimuisti=None)
        assert jasennin.tarkista(leipa, a, b) == []
        return leipa, a, b
    return f


@pytest.mark.stanza
@pytest.mark.parametrize("teksti,virkkeita", [
    ("Puhuin tri. Virtasen kanssa.", 1),
    ("Bill W. ja tri. Silkworth puhuivat.", 1),
    ("Tapaaminen oli 14. päivä.", 1),
    ('"Tuletko?" hän kysyi.', 1),
    ("Esim. kala on hyvää.", 1),
    ("Hän tuli. Hän meni.", 2),
])
def test_virkejako(jasenna, teksti, virkkeita):
    _, a, _ = jasenna(teksti)
    assert len(a) == virkkeita


@pytest.mark.stanza
def test_desimaalipilkku_ei_rako(jasenna):
    from pylkutus import jasennin
    _, a, b = jasenna("Luku oli 3,5 prosenttia.")
    v = jasennin.virkkeet(a)[0]
    assert "3,5" in [t.teksti for t in v.tokenit]
    assert not any(v.rako)


@pytest.mark.stanza
def test_mwt_samat_sanat(jasenna):
    from pylkutus import jasennin
    _, a, b = jasenna("Hän sanoi, ettei tule.")
    ta = [t.teksti for t in jasennin.virkkeet(a)[0].tokenit]
    tb = [t.teksti for t in jasennin.virkkeet(b)[0].tokenit]
    assert ta == tb
    assert "ei" in ta


@pytest.mark.stanza
def test_toistettavuus(jasenna):
    t = "Kun tulin kotiin, söin. Hän sanoi että jos ehtii hän tulee."
    _, a1, b1 = jasenna(t)
    _, a2, b2 = jasenna(t)
    assert conllu.kirjoita(a1) == conllu.kirjoita(a2)
    assert conllu.kirjoita(b1) == conllu.kirjoita(b2)


@pytest.mark.stanza
@pytest.mark.skipif(not os.path.exists(LAHDE), reason="lähdetiedosto puuttuu")
def test_koko_dokumentti_invariantit():
    from pylkutus import jasennin
    from pylkutus.esikasittelija import lue_md
    with open(LAHDE, encoding="utf-8") as f:
        leipa, _ = lue_md(f.read())
    a, b = jasennin.jasenna(leipa)      # välimuistista, jos ajettu
    assert jasennin.tarkista(leipa, a, b) == []
