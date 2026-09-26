from pylkutus.arviointi import jasenna_kulta, vertaa, Kulta, Kultakohta, lue_kultatiedosto
from pylkutus.tyypit import Varoitus


def V(alku, toimenpide="lisaa", saanto="S1", varmuus="high"):
    return Varoitus(saanto, varmuus, alku, alku, toimenpide, "")


def test_lisattava_merkinta():
    k = jasenna_kulta("Hän sanoi[+,S1] että tulee.")
    assert k.teksti == "Hän sanoi että tulee."
    assert k.kohdat == [Kultakohta(9, "+", "S1")]


def test_lisattava_valilyonnin_jalkeen_normalisoidaan():
    k = jasenna_kulta("Hän sanoi [+,] että tulee.")
    assert k.teksti == "Hän sanoi  että tulee."
    assert k.kohdat[0].offset == 9


def test_poistettava_sailyttaa_pilkun():
    k = jasenna_kulta("Kotiin tultuaan[-,L1] hän söi.")
    assert k.teksti == "Kotiin tultuaan, hän söi."
    assert k.kohdat == [Kultakohta(15, "-", "L1")]
    assert k.teksti[15] == ","


def test_valinnainen_olemassa():
    k = jasenna_kulta("Toivon[?-,] että tulet.")
    assert k.teksti == "Toivon, että tulet."
    assert k.kohdat[0].valinnainen and k.kohdat[0].toimenpide == "poista"


def test_useita_merkintoja():
    k = jasenna_kulta("A[+,] b[-,] c[?,] d.")
    assert k.teksti == "A b, c d."
    assert [(x.offset, x.laji) for x in k.kohdat] == [(1, "+"), (3, "-"), (6, "?")]


def test_mittari_leikkiaineisto():
    # 4 pakollista puuttuvaa kohtaa: 3 löydetään, 1 ohitetaan; 1 väärä hälytys
    k = jasenna_kulta("a[+,] b[+,] c[+,] d[+,] e f.")
    alut = [x.offset for x in k.kohdat]
    varoitukset = [V(alut[0]), V(alut[1]), V(alut[2]), V(k.teksti.index("e") + 1)]
    t = vertaa(varoitukset, k)
    l = t.yhteensa["lisaa"]
    assert (l.osumat, l.vaarat, l.ohitukset) == (3, 1, 1)
    assert l.tarkkuus == 0.75 and l.kattavuus == 0.75


def test_valinnainen_ei_muuta_tarkkuutta():
    k = jasenna_kulta("a[+,] b[?,] c.")
    t = vertaa([V(k.kohdat[0].offset), V(k.kohdat[1].offset)], k)
    l = t.yhteensa["lisaa"]
    assert (l.osumat, l.vaarat, l.valinnaiset) == (1, 0, 1)
    assert l.tarkkuus == 1.0


def test_varoitus_valilyonnin_kohdalla_osuu():
    k = jasenna_kulta("Hän sanoi[+,] että.")
    t = vertaa([V(10)], k)          # osoittaa välilyönnin jälkeen
    assert t.yhteensa["lisaa"].osumat == 1


def test_vaara_toimenpide_ei_osu():
    k = jasenna_kulta("a[-,] b.")
    t = vertaa([V(1, "lisaa")], k)
    assert t.yhteensa["lisaa"].vaarat == 1
    assert t.yhteensa["poista"].ohitukset == 1


def test_kultatiedosto(tmp_path):
    p = tmp_path / "k.txt"
    p.write_text("% kommentti\nEka[+,] kappale.\n\nToka[-,] kappale.\n", encoding="utf-8")
    kk = lue_kultatiedosto(str(p))
    assert [k.teksti for k in kk] == ["Eka kappale.", "Toka, kappale."]
