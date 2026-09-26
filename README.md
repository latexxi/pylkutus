# pylkutus — suomen kielen pilkkutarkistin

Tarkistin etsii suomenkielisestä tekstistä puuttuvat ja ylimääräiset pilkut Kielitoimiston
ohjepankin sääntöjen mukaan. Se ei muokkaa tiedostoa, vaan tulostaa varoitukset muodossa
`tiedosto:rivi:sarake: [varmuus/sääntö] viesti`.

```
tiedosto.md:6:17: [high/S1] pilkku puuttuu ennen sanaa "että" (S1)
    Ministeri totesi‸ että asia on käsitelty. Kukaan ei tiedä …
tiedosto.md:8:16: [medium/L1] ylimääräinen pilkku ennen sanaa "hän" (L1)
    …Kotiin tultuaan[,] hän söi. Haluan työpaikan joka sopii mi…
```

Säännöt, menetelmä, mittaustulokset ja työn tila: [`PLAN_PILKKU.md`](PLAN_PILKKU.md).

## Toiminta

1. **Esikäsittely**: leipäteksti md-tiedostosta (otsikot, span-tagit ja muu merkintä pois),
   offset-kartta alkuperäisiin riveihin ja sarakkeisiin.
2. **Jäsennys**: Stanza (suomen UD-malli, CPU). Virkejaon korjaus lyhennelistalla. Jäsennys
   tehdään kahdesti: A pilkkujen kanssa, B ilman. Tulokset välimuistiin (`.cache/`).
3. **Lauseistus**: UD-puusta lauseet (sivu-, relatiivi-, kysymys- ja rinnasteiset lauseet),
   finiittisyys (Voikko korjaa Stanzan virheitä) ja lauserajat.
4. **Säännöt**: jokaiselle rajalle luvun 1 sääntö (S1 alistuskonjunktio, S3 epäsuora
   kysymys, R1 täydelliset päälauseet, V1 *kuin*, L1 lauseenvastike …).
5. **Raportti**: varoitukset alkuperäisen tiedoston riveille.

## Asennus

Vaatii Python 3.12:n, järjestelmän `libvoikko`-paketin (Ubuntu: `python3-libvoikko`,
`voikko-fi`) ja `python3.12-venv`:n.

```bash
/usr/bin/python3 -m venv --system-site-packages .venv   # libvoikko järjestelmästä
.venv/bin/pip install stanza pytest
.venv/bin/pip install -e .
.venv/bin/python -c "import stanza; stanza.download('fi')"
```

## Käyttö

```bash
./pylkuta tiedosto.md                  # kaikki varoitukset
./pylkuta tiedosto.md --min medium     # vain varmemmat
./pylkuta tiedosto.md --rule S3        # yksi sääntö
./pylkuta tiedosto.md --tyyli          # myös valinnaiset pilkut
./pylkuta tiedosto.md --dump lauseet   # lausesulut tarkistusta varten
```

Ensimmäinen ajo jäsentää tekstin (noin 4 min 300 000 merkille CPU:lla); seuraavat ajot
käyttävät välimuistia.

## Testit

```bash
.venv/bin/python -m pytest -m "not stanza"   # nopeat, ilman jäsennintä
.venv/bin/python -m pytest                   # kaikki, myös Stanza-testit
```

Mittaus merkittyä otosta vasten (merkintätapa: `pylkutus/arviointi.py`):

```bash
.venv/bin/python -m pylkutus.arviointi -t pylkutus -v kulta.txt
```

Kehityksessä käytetty lähdedokumentti, sen merkityt otokset ja koko tekstin tilannekuvat
eivät ole repossa.

## Lisenssi

MIT, ks. [`LICENSE`](LICENSE). Lisenssi koskee koodia; testeissä ja tulostiedostoissa
lainatut lähdedokumentin virkkeet eivät kuulu sen piiriin.
