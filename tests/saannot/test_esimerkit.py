"""Luvun 1 esimerkit: oikein-muoto ei tuota varoitusta, väärin-muoto tuottaa odotetun.

Odotus: lista (sääntö, toimenpide, sana raon jälkeen).
"""
import pytest

from pylkutus.saantotarkistin import tarkista_teksti

pytestmark = pytest.mark.stanza


def varoitukset(teksti):
    tulos = []
    for v in tarkista_teksti(teksti):
        loppu = teksti[v.alku:].lstrip(", ")
        tulos.append((v.saanto, v.toimenpide, loppu.split()[0].strip(".,")))
    return tulos


OIKEIN = [
    # S1, S1a, S1b
    "Ministeri totesi, että asia on käsitelty.",
    "Hän sanoi, että jos ehtii, hän tulee.",
    "Kävin kaupassa ja jos ehdin, myös kirjastossa.",
    # S1e
    "Kun tulin kotiin, söin.",
    # M1, M3
    "Soitan, heti kun pääsen.",
    "Soitan heti, kun pääsen.",
    "Silloin kun tulin, kaikki olivat jo lähteneet.",
    # S2, S2a
    "Haluan työpaikan, joka sopii minulle.",
    "Pelaajat, joiden nimiä ei mainittu, neuvottelevat.",
    # K1, K2, K3
    "Komitea valitsee sen, joka on pätevin.",
    "Se mitä tapahtui, oli outoa.",
    # S3
    "Kukaan ei tiedä, missä hän asuu.",
    "Kysyin, tuleeko hän.",
    # S2b: vapaasti viittaava lause, pilkku valinnainen
    "Ota mitä haluat ja jätä loput.",
    "Hän etsi alkoholisteja mistä tahansa vain pystyi.",
    "Yhteiskunta voi tehdä mitä haluaa kanssani.",
    # eliptinen rinnastus ja yhteinen subjekti: ei R1-varoitusta
    "Toveriseura syntyi ohjelmasta eikä päinvastoin.",
    "Kun hän aloittaa syömisen, hän ei pysty lopettamaan ja jatkaa syömiskierteeseen.",
    "Elänkö sopusoinnussa tämän Voiman kanssa vai elänkö päinvastoin?",
    # eikä-vastakohta: pilkku sallittu
    "Se oli meidän yhteinen tietomme, eikä vain yhden henkilön.",
    # V1 (niin kuin), P1 (sekä … että), S1b (joten kun), jne., aloittava lainausmerkki
    "Me teimme niin kuin Kolumbus.",
    "Molemmat ovat helppoja sekä harjoitella että muistaa.",
    "Se pätee kaikille, joten kun olet valmis, voit aloittaa.",
    "Et voi tehdä neljättä askelta, ennen kuin olet tehnyt kolmannen jne.",
    'Hän sanoi: "Ei kiitos, minua väsyttää."',
    # S4
    "Haluan työpaikan, joka sopii minulle ja jossa voin käyttää kykyjäni.",
    # R1, R2, R3, R4
    "Kesäkuussa he matkustivat Yhdysvalloissa, ja heinäkuussa he olivat Kanadassa.",
    "Perhe kunnosti saunaa ja viimeisteli keittiön.",
    "Salilla on hiljaista, mutta viikonloppuisin siellä käy väkeä.",
    "Aion kirjoittaa, sillä en osaa muutakaan.",
    # V1, V5
    "Todellisuus näyttää valoisammalta kuin hän uskalsi toivoa.",
    "Täällä on mukavaa kuten aina.",
    # L1
    "Kotiin tultuaan hän söi.",
    "Asetuttuaan Mikkeliin taiteilija toimi opettajana.",
    # 1.14
    "Tee se joka päivä kahden viikon ajan.",
    # 1.15
    "Tämä ei ole kenenkään vika — mutta se, mitä tapahtuu, on outoa.",
    "Kerro meille: mitä tapahtui?",
]


@pytest.mark.parametrize("teksti", OIKEIN)
def test_oikein_ei_varoitusta(teksti):
    assert varoitukset(teksti) == []


VAARIN = [
    ("Ministeri totesi että asia on käsitelty.", [("S1", "lisaa", "että")]),
    ("Kun tulin kotiin söin hyvin.", [("S1e", "lisaa", "söin")]),
    ("Soitan heti kun pääsen kotiin.", [("M1", "lisaa", "heti")]),
    ("Haluan työpaikan joka sopii minulle.", [("S2", "lisaa", "joka")]),
    ("Komitea valitsee sen joka on pätevin.", [("K1", "lisaa", "joka")]),
    ("Se mitä tapahtui oli outoa.", [("K3", "lisaa", "oli")]),
    ("Kukaan ei tiedä missä hän asuu.", [("S3", "lisaa", "missä")]),
    ("Kysyin tuleeko hän huomenna.", [("S3", "lisaa", "tuleeko")]),
    ("Kesäkuussa he matkustivat Yhdysvalloissa ja heinäkuussa he olivat Kanadassa.",
     [("R1", "lisaa", "ja")]),
    ("Salilla on hiljaista mutta viikonloppuisin siellä käy väkeä.", [("R3", "lisaa", "mutta")]),
    ("Aion kirjoittaa sillä en osaa muutakaan.", [("R4", "lisaa", "sillä")]),
    ("Todellisuus näyttää valoisammalta, kuin hän uskalsi toivoa.", [("V1", "poista", "kuin")]),
    ("Kotiin tultuaan, hän söi.", [("L1", "poista", "hän")]),
    # 1.4: lause alkaa rinnastuskonjunktion jälkeen, pilkku vaaditaan (matala varmuus)
    ("Tämä ei ole kenenkään vika — mutta se mitä tapahtuu, on outoa.", [("K1", "lisaa", "mitä")]),
]


@pytest.mark.parametrize("teksti,odotus", VAARIN)
def test_vaarin_varoitus(teksti, odotus):
    assert varoitukset(teksti) == odotus
