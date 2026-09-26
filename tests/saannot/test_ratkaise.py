"""Raon päätösten ratkaisu (saantotarkistin.ratkaise)."""
from pylkutus.saantotarkistin import Ehdotus, ratkaise
from pylkutus.tyypit import Paatos, Pakko, Varmuus

K, V, E = Pakko.KYLLA, Pakko.VALINNAINEN, Pakko.EI
H, M, L = Varmuus.HIGH, Varmuus.MEDIUM, Varmuus.LOW


def p(koodi, pakko, varmuus):
    return Paatos(3, koodi, pakko, varmuus)


def test_pakollinen_puuttuu_varmin_voittaa():
    assert ratkaise([p("R1", K, L), p("S3", K, M)], pilkku=False) == Ehdotus("S3", "lisaa", M, False)


def test_kielto_estaa_lisayksen():
    assert ratkaise([p("S1", K, H), p("S1b", E, H)], pilkku=False) is None


def test_valinnainen_tekee_valinnaiseksi():
    assert ratkaise([p("R1", K, L), p("R1a", V, M)], pilkku=False) == Ehdotus("R1", "lisaa", L, True)


def test_ylimaarainen_pilkku_varmuus_alenee():
    assert ratkaise([p("R2", E, M)], pilkku=True) == Ehdotus("R2", "poista", L, False)
    assert ratkaise([p("S1b", E, H)], pilkku=True) == Ehdotus("S1b", "poista", M, False)


def test_rajamerkki_ei_kiella_pilkkua():
    assert ratkaise([p("1.15", E, H)], pilkku=True) is None


def test_pilkku_paikallaan():
    assert ratkaise([p("S1", K, H)], pilkku=True) is None
