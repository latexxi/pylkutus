# PLAN_KORJAUKSET — ensimmäisen version jälkeiset korjaukset

Lähtökohta: katselmointi 2026-09-26 (redundanssi, pyörän uudelleenkeksiminen, rakenne,
mittaus). Tavoite: sama tai parempi tulos, vähemmän koodia, nopeampi ajo, luotettavampi mittari.

## Periaate: jokainen vaihe verrataan baselineen

Baseline = commit `b2607ec` (ensimmäinen versio). `arviointi/tilannekuva.py <nimi>` tallentaa
hakemistoon `arviointi/tilannekuvat/<nimi>/` (ei repossa, sisältää lähdetekstiä):

| Tiedosto | Sisältö |
|---|---|
| `raportti.txt`, `raportti_oletus.txt` | `pylkuta` koko lähdedokumentille `--tyyli`-lipulla ja ilman |
| `lauseet.txt`, `rajat.txt` | `--dump lauseet`, `--dump rajat` |
| `kulta_<otos>_<tarkistin>.txt` | mittaritaulukko ja virheet (`-v`) kultaisista otoksista |
| `testit.txt` | pytestin yhteenveto |
| `ajat.log` | ajoajat (ei diffiin): lämmin välimuisti, kylmä jäsennys (valinnainen `--kylma`) |

Vertailu: `diff -r -x ajat.log arviointi/tilannekuvat/baseline arviointi/tilannekuvat/<vaihe>`.
Refaktorointivaiheissa (K1–K5) odotettu ero on nolla varoituksissa ja mittareissa;
jokainen ero selitetään tai korjataan ennen seuraavaa vaihetta.

## Vaiheet

### K0 Tilannekuvatyökalu ja baseline
`arviointi/tilannekuva.py`, baseline-tilannekuva nykyisestä koodista (kylmä ajo mukana).

### K1 B-jäsennys pois
B ei vaikuta varoituksiin (`saantotarkistin` ohittaa B-rajat, `ylimaaraiset._rajat` käyttää
vain A/AB) ja V3-koe kumosi sen hyödyn. Pois: `jasenna_B`, `Analyysi.b`, `yhdista`,
`Raja.lahde`, B-välimuisti, B-invariantit. `--dump rajat` ilman lähdesaraketta.
Odotus: raportti ja kultamittarit identtiset, `rajat.txt` muuttuu vain lähdesarakkeen osalta,
kylmä jäsennys noin puolet nopeampi.

### K2 Rakenteen siivous
- Sanalistat yhteen: `ALISTUS`, `RINNASTUS*`, `MONIOSAISET`, `KYSYMYSSANAT` → `sanastot.py`.
  `lauseistaja`n laajempi `ALISTUS` (+ *kuin, ennen, sillä*) nimetään omaksi joukokseen.
- `KYSYMYSVERBIT`: taivutetut muodot (*ymmärtämään*, *näkemään*) pois, ne eivät voi osua lemmaan.
- `Analyysi` → `tyypit.py` (säännöt eivät tuo `ajuri`a). `VARMUUS` yhteen paikkaan.
- Voikon finiittisyys yhdeksi funktioksi (`tuntematon`-parametri).
- `conllu.Lause` → `conllu.ConlluVirke` (nimi ei törmää `tyypit.Lause`en).
- Lähtötasot (`lahtotaso.py`, vanhan skriptin polku) pois paketista → `arviointi/`.
Odotus: identtinen tulos.

### K3 Yhtenäinen sääntörajapinta ja rekisteri
- `Pakko` ja `Varmuus` Enumeiksi.
- Kaikki säännöt (raja-, sanasto- ja ylimääräisyyssäännöt) tuottavat `Paatos(rako, koodi,
  pakko, varmuus, toimenpide)`; yksi ratkaisija päättää raon varoituksen.
- Sääntörekisteri: koodi, kuvaus, ohjepankin luku. `pylkuta --saannot` listaa.
Odotus: identtinen tulos (puhdas refaktorointi).

### K4 Kappalekohtainen välimuisti
Välimuistin avain kappaleen tekstistä, ei koko dokumentista. Virkejaon korjaus ei ylitä
kappalerajaa, joten tulos ei muutu. Uudet kappaleet jäsennetään yhdessä erässä.
Odotus: identtinen tulos; yhden kappaleen muutos jäsentää vain sen kappaleen.

### K5 Paketointi
`pyproject.toml`: `dependencies`, `[project.scripts] pylkuta = ...`. Bash-kääre säilyy
kehityskäyttöön. Odotus: identtinen tulos.

### K6 Synteettinen mittari UD-korpuksesta
UD Finnish TDT:n **test**-jako (ei Stanzan opetusdatassa): poistetaan pilkkuja ja lisätään
vääriä, mitataan tuhansilla kohdilla. Kultaiset puut erottavat jäsennys- ja sääntövirheet.
Baseline ajetaan samalla aineistolla (`git worktree` commitista `b2607ec`).

### K7 Dokumentaatio
`PLAN_PILKKU.md` jaetaan: `docs/saannot.md` (spesifikaatio), `arviointi/tulokset.md`
(mittausloki); suunnitelma- ja tilaosuudet historiaan.

### K8 (koe, myöhemmin) Pilkkuluokittelija
FinBERT-tyyppinen raon luokittelija samalla K6-mittarilla. Päätös hybridistä mittauksen perusteella.

## Tila

| Vaihe | Tila | Ero baselineen |
|---|---|---|
| K0 | valmis | baseline: 588 varoitusta (`--tyyli`), 132 testiä, kylmä jäsennys 211 s |
| K1 | valmis | raportti, lauseet, kultamittarit identtiset; `rajat.txt`: 312 B-riviä ja lähdesarake pois; 131 testiä (`test_yhdista` pois); kylmä jäsennys 120 s (−43 %) |
| K2 | valmis | identtinen K1:n kanssa (myös `KYSYMYSVERBIT`-listan taivutetut muodot olivat kuolleita); `lahtotaso.py` jäi pakettiin jäädytettynä, polku `PYLKUTUS_VANHA` |
| K3 | valmis | identtinen baselinen kanssa (myös oletusraportti, 388 varoitusta); 139 testiä (+2 rekisteri, +6 ratkaisija) |
| K4 | valmis | identtinen K3:n kanssa (kappaleittain jäsennetty = koko teksti kerralla); kylmä 121 s, yhden kappaleen muutos 0,7 s (ennen 120 s); 140 testiä |
| K5 | valmis | identtinen K4:n kanssa; `pip install -e ".[dev]"`, komento `pylkuta` venviin |
| K6 | osittain | mittari valmis (`arviointi/ud.py`), baseline = nykyinen molemmissa UD-tiedostoissa; tulokset `arviointi/tulokset.md`. Jäljellä: sääntövirheiden läpikäynti kultapuilla |
| K7 | | |

## Jatko seuraavassa sessiossa

Työ on `main`-haarassa (commit 9c84132, pushattu origin/mainiin). Baseline-commit `b2607ec` on worktreessa
`../pylkutus-baseline` (sen `.cache` on symlinkki tämän repon välimuistiin); poisto:
`git worktree remove ../pylkutus-baseline`.

Tarkistus, että ympäristö toimii (noin 1 min):

```bash
.venv/bin/python -m pytest -q                      # 140 testiä
.venv/bin/python arviointi/ud.py tee               # UD-korpus ja kultatiedostot (ei repossa)
.venv/bin/python arviointi/ud.py tee --lajit e,j,t,u
.venv/bin/python arviointi/tilannekuva.py tarkistus
diff -r -x ajat.log -x 'ud_*' arviointi/tilannekuvat/k5 arviointi/tilannekuvat/tarkistus   # ei eroja
```

Tilannekuvat (`arviointi/tilannekuvat/`, ei repossa) ovat vain tällä koneella. Jos ne puuttuvat,
baseline luodaan uudelleen: `python arviointi/tilannekuva.py baseline --repo ../pylkutus-baseline`.

Seuraavat askeleet:
1. **K6 loppuun:** käy läpi kultapuiden väärät hälytykset toimitetuissa lajeissa
   (`python arviointi/ud.py kultapuut --lajit e,j,t,u -v`). Havaittuja sääntövirheitä:
   S6 lainauksen jälkeen (*"Eikö sinustakin?" kysyit* → sääntö Q3 puuttuu), S1 numeroinnin
   jälkeen (*(11) Jotta*), R2/S4 poista täydellisen lauseen edellä (*pakkaaminen, ja neljältä
   pitäisi istua*; *tautia, eikä enää pysty*). Jokainen korjaus: mittaa UD molemmissa tiloissa
   ja kultaotokset, vertaa k5:een.
2. **K7:** dokumentaation jako (ks. yllä).
3. **K8:** pilkkuluokittelijakoe K6-mittarilla.

Muistettavaa:
- UD-mittarin "väärät" sisältävät korpuksen omia puuttuvia pilkkuja (blogi, fiktio); vertaa
  versioita keskenään, älä tulkitse absoluuttisena tarkkuutena.
- PyTorch kaatuu satunnaisesti importissa (`getCount is non-monotonic`); ajo uudelleen auttaa.
- `pip install -e .` vaatii build-eristyksen (järjestelmän `packaging` 24.0 on liian vanha
  `--no-build-isolation`-tilaan).
