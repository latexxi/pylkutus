import os

import pytest

from pylkutus.esikasittelija import lue_md, lue_teksti, tarkista_kartta
from pylkutus.saantotarkistin import tarkista

LAHDE = os.path.expanduser("~/Documents/ratkaisu/2026-09-14 ratkaisu.md")


def md(s):
    leipa, loki = lue_md(s)
    assert tarkista_kartta(leipa) == []
    return leipa, loki


def test_span_poistetaan_ja_kartta_osuu():
    leipa, _ = md("Alku.\n\n<span id=\"anchor-1\"></span>Teksti jatkuu.\n")
    assert leipa.teksti == "Alku.\n\nTeksti jatkuu."
    i = leipa.teksti.index("T")
    assert leipa.rivi_sarake(i) == (3, 28)


def test_md_otsikot_karsitaan():
    leipa, loki = md("# Otsikko\n\nKaveri oli tietysti oikeassa.\n\n## <span id=\"a\"></span>Toinen\n")
    assert leipa.teksti == "Kaveri oli tietysti oikeassa."
    assert [l.syy for l in loki] == ["otsikko", "otsikko"]


def test_lihavoitu_otsikko_ilman_loppumerkkia():
    leipa, loki = md("**On olemassa ratkaisu**  \nOpastus Ison kirjan ohjelmaan\n\nVirke tässä.\n")
    assert leipa.teksti == "Virke tässä."
    assert loki[0].syy == "otsikon kaltainen"


def test_isoin_kirjaimin_otsikko():
    leipa, _ = md("OPASTUS ISON KIRJAN OHJELMAAN\n\nVirke.\n")
    assert leipa.teksti == "Virke."


def test_pilkullinen_otsikko_ilman_loppumerkkia():
    leipa, _ = md("Itsekkyydestä, epärehellisyydestä ja pelosta irti kasvaminen\n\nVirke.\n")
    assert leipa.teksti == "Virke."


def test_pitka_kappale_ilman_loppumerkkia_sailyy():
    s = ("Iso kirja antaa sinulle mahdollisuuden ymmärtää ongelma. Se myös esittelee "
         "ratkaisun ja näyttää miten voit soveltaa ohjelmaa omaan elämääsi")
    leipa, _ = md(s + "\n")
    assert leipa.teksti == s


def test_pehmea_tavuviiva():
    leipa, _ = md("Se myös e­sittelee ratkaisun.\n")
    assert leipa.teksti == "Se myös esittelee ratkaisun."


def test_luettelo_omina_kappaleinaan():
    leipa, _ = md("Johdanto:\n\n1.  Mikä oli ongelma\n2.  Mikä oli ratkaisu\n\nLoppu.\n")
    assert leipa.teksti == "Johdanto:\n\nMikä oli ongelma\n\nMikä oli ratkaisu\n\nLoppu."
    assert len(leipa.kappaleet) == 4
    i = leipa.teksti.index("Mikä oli r")
    assert leipa.rivi_sarake(i) == (4, 5)


def test_taulukon_otsake_ohitetaan_ja_solut_erotetaan():
    leipa, loki = md(
        "Ennen.\n\n"
        "| Mitä tein? | Loukkasin tai uhkasin |\n"
        "| --- | --- |\n"
        "| Menin kotiin. | Sitten söin. |\n\n"
        "Jälkeen."
    )
    assert leipa.teksti == (
        "Ennen.\n\nMenin kotiin.\n\nSitten söin.\n\nJälkeen."
    )
    assert len(leipa.kappaleet) == 4
    assert leipa.rivi_sarake(leipa.teksti.index("Menin")) == (5, 3)
    assert [r.syy for r in loki] == ["taulukon otsake", "taulukon erotin"]


@pytest.mark.stanza
def test_taulukon_solujen_valille_ei_synny_keinoista_lauseketta():
    leipa, _ = md(
        "| Sarake 1 | Sarake 2 |\n"
        "| --- | --- |\n"
        "| Kukaan ei tiedä | missä hän asuu. |\n"
        "| Hän sanoi että palaa. | Toinen solu. |"
    )
    varoitukset = tarkista(leipa)
    assert [
        (v.saanto, v.toimenpide, leipa.teksti[v.alku:].lstrip(", ").split()[0])
        for v in varoitukset
    ] == [("S1", "lisaa", "että")]


def test_muistiinpano_poistetaan():
    leipa, loki = md("Juominen on rankempaa. ++ 14.9.2026 ++ jatka tästä\n")
    assert leipa.teksti == "Juominen on rankempaa."
    assert any("muistiinpano" in l.teksti for l in loki)


def test_kappaleen_sisainen_rivinvaihto():
    leipa, _ = md("Eka rivi ja\ntoka rivi.\n")
    assert leipa.teksti == "Eka rivi ja toka rivi."
    assert leipa.rivi_sarake(leipa.teksti.index("toka")) == (2, 1)


def test_desimaalipilkku_ja_korostus_ei_sotkeudu():
    leipa, _ = md("Luku 3,5 ja *tärkeä* sana sekä snake_case.\n")
    assert leipa.teksti == "Luku 3,5 ja tärkeä sana sekä snake_case."


def test_lue_teksti_identiteettikartta():
    leipa = lue_teksti("Eka.\n\nToka kappale.")
    assert leipa.kappaleet == [(0, 4), (6, 19)]
    assert leipa.rivi_sarake(6) == (3, 1)


@pytest.mark.skipif(not os.path.exists(LAHDE), reason="lähdetiedosto puuttuu")
def test_koko_dokumentti_invariantti():
    with open(LAHDE, encoding="utf-8") as f:
        leipa, loki = lue_md(f.read())
    assert tarkista_kartta(leipa) == []
    assert "<span" not in leipa.teksti and "**" not in leipa.teksti and "­" not in leipa.teksti
    assert "++" not in leipa.teksti
    assert len(leipa.kappaleet) > 800


def test_ajatusviivaan_paattyva_johdanto_sailyy():
    leipa, _ = md("Jos käymme tämän läpi, hämmästymme —\n\n1.  Saamme kokea vapautta.\n")
    assert leipa.teksti == "Jos käymme tämän läpi, hämmästymme —\n\nSaamme kokea vapautta."
