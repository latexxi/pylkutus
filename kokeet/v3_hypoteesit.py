"""V3: Stanza-koe. Tulostaa koevirkkeiden puut (A ja B) ja jäädyttää ne testiaineistoksi.

Käyttö: python kokeet/v3_hypoteesit.py > kokeet/v3_tuloste.txt
Jäädytetyt tiedostot: tests/fixtures/v3_A.conllu, tests/fixtures/v3_B.conllu
"""
import os

from pylkutus import conllu, jasennin
from pylkutus.esikasittelija import lue_teksti

HYPOTEESIT = {
    "finiittisyys": [
        "Hän lähti, kun hän ei tullut ajoissa.",
        "Odotimme, koska hän on lähtenyt jo aamulla.",
        "Hän ei ole rikas, vaikka hän on opettaja.",
        "Tiedän, että hän ei ole tullut.",
    ],
    "lauseenvastike": [
        "Kotiin tultuaan hän söi.",
        "Hän pyysi neuvoani uskoen, että voin auttaa.",
        "Ensiksi auttaaksemme ihmisiä kirjoitimme tämän.",
        "Asetuttuaan Mikkeliin taiteilija toimi opettajana.",
    ],
    "se_mita": [
        "Se mitä tapahtui, oli outoa.",
        "Mitä tapahtui, oli outoa.",
        "Komitea valitsee sen, joka on pätevin.",
        "Tämä ei ole kenenkään vika, mutta se mitä tapahtuu, on outoa.",
    ],
    "subjektiton": [
        "Salilla on hiljaista, mutta viikonloppuisin siellä käy väkeä.",
        "Minun täytyy lähteä, ja sinun täytyy jäädä.",
        "Sataa, ja tuulee.",
        "Talo rakennettiin, ja se myytiin.",
    ],
    "taydellisyys": [
        "Perhe kunnosti saunaa ja viimeisteli keittiön.",
        "Kesäkuussa he matkustivat Yhdysvalloissa, ja heinäkuussa he olivat Kanadassa.",
        "Tulin kotiin ja söin.",
        "Tämä kauna oli hänen äitiään kohtaan ja se näytti valtavalta.",
        "Aviomieheni palasi lopulta mutta ei kestänyt kauaa.",
    ],
    "loppupilkku": [
        "Kun tulin kotiin, söin.",
        "Hän sanoi, että jos ehtii, hän tulee.",
        "Pelaajat, joiden nimiä ei mainittu, neuvottelevat.",
    ],
    "epasuora_kysymys": [
        "Emme tienneet, oliko se normaalia.",
        "Tämä auttaa sinua näkemään, mistä vihasi tulee.",
        "Kukaan ei tiedä, missä hän asuu.",
    ],
    "ab_ero": [
        "Tämä ei tietenkään ole kenenkään vika — mutta se mitä tapahtuu, on että jotkut vanhemmat "
        "toipuneet jäsenet eivät enää tunne samaistuvansa näiden ihmisten kanssa ja ovat aika "
        "väsyneitä kuuntelemaan heidän juttujaan, joten he jäävät kotiin.",
        "Hän vastasi, että hänestä tuntuu kuin hän olisi syntynyt uudelleen.",
        "Aviomieheni palasi lopulta mutta ei kestänyt kauaa, kun ymmärsin totuuden.",
        "Tee se joka päivä kahden viikon ajan, ja katso mitä tapahtuu.",
    ],
    "otos_virheet": [
        "Heti kun alat maksaa takaisin ihmisille, niihin ihmisiin liittyvät pelkosi ja velkasi katoavat.",
        "Hän on jo tehnyt sinulle kaiken pahimman mahdollisen vastustamalla tapaamistanne ja jos hän "
        "on tehnyt pahimpansa ja sinä olet tehnyt parhaimpasi, niin ei ole mitään syytä pelätä häntä "
        "enää, jolloin häneen liittyvä pelko häviää.",
    ],
}

LAUSESUHTEET = {"root", "advcl", "ccomp", "acl:relcl", "csubj", "csubj:cop", "conj",
                "parataxis", "acl", "xcomp", "xcomp:ds"}


def rivi(t, v):
    head = v.tokenit[t.head - 1].teksti if t.head else "ROOT"
    vf = t.feats.get("VerbForm", "")
    muut = ",".join(f"{k}={t.feats[k]}" for k in ("Person", "Voice", "Mood") if k in t.feats)
    return f"{t.teksti:<14}{t.upos:<6}{t.deprel:<11}{head:<14}{vf:<5}{muut}"


def main():
    virkkeet = [v for vv in HYPOTEESIT.values() for v in vv]
    teksti = "\n\n".join(virkkeet)
    leipa = lue_teksti(teksti)
    a, b = jasennin.jasenna(leipa, valimuisti=None)
    assert jasennin.tarkista(leipa, a, b) == [], jasennin.tarkista(leipa, a, b)
    assert len(a) == len(virkkeet), (len(a), len(virkkeet))
    va, vb = jasennin.virkkeet(a), jasennin.virkkeet(b)
    n = 0
    for ryhma, lista in HYPOTEESIT.items():
        print("#" * 100)
        print("#", ryhma)
        for _ in lista:
            x, y = va[n], vb[n]
            print("=" * 100)
            print(virkkeet[n])
            for t, u in zip(x.tokenit, y.tokenit):
                pilkku = "," if x.rako[t.i] else " "
                ero = "  " if (t.deprel, t.head) == (u.deprel, u.head) else "≠ "
                bhead = y.tokenit[u.head - 1].teksti if u.head else "ROOT"
                merkki = "*" if t.deprel in LAUSESUHTEET else " "
                print(f"{pilkku}{merkki} {rivi(t, x):<62}| {ero}{u.deprel:<11}{bhead}")
            n += 1
    hak = os.path.join(os.path.dirname(__file__), "..", "tests", "fixtures")
    for nimi, l in (("A", a), ("B", b)):
        with open(os.path.join(hak, f"v3_{nimi}.conllu"), "w", encoding="utf-8") as f:
            f.write(conllu.kirjoita(l, [jasennin.versiot(), f"jasennys = {nimi}"]))


if __name__ == "__main__":
    main()
