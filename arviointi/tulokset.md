# Mittaustulokset

Kultainen otos: `arviointi/kulta/otos_01_20.txt` (luonnos, tarkistamatta). 7 pakollista
puuttuvaa pilkkua, 7 valinnaista, ei ylimääräisiä.

## 2026-09-26 Lähtötasot (V2)

| Tarkistin | osumat | väärät | ohitetut | tarkkuus | kattavuus |
|---|---|---|---|---|---|
| vanha `pilkut.py` | 1 | 0 | 6 | 100 % | 14 % |
| sanalista (`lahtotaso.sanalista`) | 0 | 0 | 7 | – | 0 % |

Sanalista ei kata S3:a eikä R1:tä, joten otoksen pakollisista kohdista se ei löydä yhtään.
Otos on pieni: luvut kertovat suunnan, eivät tarkkuutta.

## 2026-09-26 Lauseistaja, käsintarkistus (V6)

Kultaisen otoksen 1–20 virkkeistä (67 kpl) 30 satunnaista (siemen 2026), `pylkuta --dump lauseet`.

| Tulos | Virkkeitä |
|---|---|
| lausesulut oikein | 25 |
| rajat oikein, liitoskohta tai tyyppi väärin | 3 (v0 *mutta emme tienneet* liitetty kun-lauseeseen; v14 *mitä meidän piti* `acl:relcl` eikä `ccomp`; v31 *mutta*-lause liitetty *tulet*-lauseeseen) |
| raja väärin | 2 (v14 *ja ajattelimme* liitetty että-lauseen sisään; v40 *vihasi* jäsennetty verbiksi: väärä lause *ja suuttumuksesi … tulevat*) |

Rajavirheitä 2/30 = 7 %. Tämä on jäsennykseen perustuvien sääntöjen karkea yläraja
väärille hälytyksille ja ohituksille. v40 tuottaisi väärän R1-varoituksen.

## 2026-09-26 Sääntötarkistin, ensimmäinen versio (V7)

Säännöt: S1, S1a, S1b, S1e, S2, S2a, S3, K1–K3, M1, M3, R1–R4, S4, S6, V1, V2, V5, 1.15;
ylimääräiset V1, L1, R2 (A1/A2 vain `--tyyli`). Valinnaiset pilkut eivät tuota varoitusta.

**Kehitysaineisto** `otos_01_20.txt` (säännöt viritetty tällä):

| Tarkistin | osumat | väärät | ohitetut | tarkkuus | kattavuus |
|---|---|---|---|---|---|
| pylkutus | 7 | 1 | 0 | 88 % | 100 % |

**Testiaineisto** `otos_21_50.txt` (merkitty ennen mittausta, sääntöjä EI viritetty tällä;
15 pakollista puuttuvaa, 5 ylimääräistä):

| Tarkistin | puuttuvat osumat/väärät/ohitetut | tarkkuus | kattavuus | ylimääräiset osumat/ohitetut |
|---|---|---|---|---|
| vanha `pilkut.py` | 4 / 1 / 11 | 80 % | 27 % | 0 / 5 |
| sanalista | 1 / 0 / 14 | 100 % | 7 % | 0 / 5 |
| **pylkutus** | **8 / 1 / 7** | **89 %** | **53 %** | 1 / 4 |

Tämä on ainoa puhdas testiaineistomittaus. Seuraavat korjaukset tehdään tämän aineiston
virheiden perusteella, joten myöhemmät luvut samalla aineistolla ovat optimistisia; puhdas
mittaus vaatii uuden otoksen (kappaleet 51–).

## 2026-09-26 Korjauskierros testiaineiston ja koko dokumentin perusteella (V7)

Korjaukset: kysymyssanalista (*kuinka* ilman `PronType`), apuverbin finiittisyys Voikolla
(*pitää* merkitty `Inf`), lainausmerkit ja loppusulku eivät korvaa pilkkua, `pakko=ei` +
pilkku paikalla = ylimääräinen pilkku (S1b, S4, R2, V1), S3-sanastosääntö (kysymysverbi +
kysymyssana, ei riipu jäsennyksestä), relatiivilauseeseen liitetty päälause (R1), perfektin
passiivi (R1a), *eivätkä/emmekä* (R-säännöt), yhteinen subjekti conj-ketjussa, loppurajat
(S1e, S2a, K3) aina matalalla varmuudella, S6 matalalla varmuudella, L1 pitkä vastike matala.

| Aineisto | puuttuvat osumat/väärät/ohitetut | tarkkuus | kattavuus | ylimääräiset osumat/väärät/ohitetut |
|---|---|---|---|---|
| otos 1–20 (kehitys) | 7 / 1 / 0 | 88 % | 100 % | – |
| otos 21–50 (**ei enää puhdas**) | 14 / 1 / 1 | 93 % | 93 % | 4 / 0 / 1 |

**Koko dokumentti** (`pylkuta "2026-09-14 ratkaisu.md"`): 388 varoitusta (high 14, medium 182,
low 192). Käsin arvioitu 40 satunnaista varoitusta (siemen 7, ennen viimeisiä korjauksia):
30 oikein, 8 väärin, 2 tulkinnanvaraista → tarkkuus 75–79 %. Sääntökohtaisesti:

| Sääntö | otos | oikein | huomio |
|---|---|---|---|
| S3 | 9 | 9 | |
| L1 | 4 | 4 | |
| R1 | 17 | 12 (+2 ?) | väärät: vajaa lause (*jatkaa ja katkaisee*, *eikä päinvastoin*), rinnasteiset relatiivilauseet – kaksi ensimmäistä korjattu |
| S1e | 2 | 0 | kaikki 10 S1e-varoitusta käyty läpi: lähes kaikki jäsennysvirheitä → varmuus low |
| S2 | 1 | 0 | kaikki 16 käyty läpi: 12 oikein, väärät sarakkeiden nimiä (*Ketä vahingoitin*) |
| K1 | – | – | kaikki 13 käyty läpi: oikein |
| V1 | – | – | kaikki 12 käyty läpi: oikein |

**Päätökset:** kaikki säännöt oletuksena päällä. S1e, S2a, K3, S6 ja R1 aina `low`, jotta
`--min medium` antaa tarkan listan. Valinnaiset (S1a, M1-sisäinen, R1a, R3-vajaa, V2, K2, A1,
A2) vain `--tyyli`-lipulla.

**Seuraava puhdas mittaus** vaatii uuden merkityn otoksen (kappaleet 51–100 samalla siemenellä).

## 2026-09-26 Synteettinen UD-mittari (PLAN_KORJAUKSET.md K6)

UD Finnish TDT r2.15, test-jako (ei Stanzan opetusdatassa). Pilkut poistettu todennäköisyydellä
0,5 (siemen 2026, vain pilkut, joita seuraa välilyönti); muut raot oletetaan oikeiksi. Mitattu
ilman `--tyyli`-lippua. K1–K5-refaktoroinnin jälkeinen koodi antaa jäsennintilassa täsmälleen
saman tuloksen kuin baseline `b2607ec`.

| Aineisto | Tila | lisää: osumat / väärät / ohitetut | tarkkuus | kattavuus | poista: väärät |
|---|---|---|---|---|---|
| kaikki (1555 virkettä, 585 poistoa) | Stanza | 311 / 179 / 274 | 63,5 % | 53,2 % | 8 |
| kaikki | kultapuut | 362 / 149 / 223 | 70,8 % | 61,9 % | 11 |
| toimitetut e,j,t,u (434 virkettä, 203 poistoa) | Stanza | 123 / 26 / 80 | 82,6 % | 60,6 % | 4 |
| toimitetut e,j,t,u | kultapuut | 144 / 17 / 59 | 89,4 % | 70,9 % | 5 |

Havainnot:
- Kultapuut vs. Stanza: jäsennysvirheet selittävät noin 9 prosenttiyksikköä kattavuudesta ja
  7 tarkkuudesta. Loput ovat sääntöjen tai mittarin virheitä.
- Tekstilajeittain (kultapuut, tarkkuus): u 92 %, e 87 %, t 86 %, j 84 %, w 71 %, h 68 %,
  s 67 %, b 60 %, f 51 %. Blogeissa ja fiktiossa suuri osa "vääristä" on lähdetekstistä
  puuttuvia pilkkuja (*Kukaan ei edes tiedä missä hän asuu*), ei tarkistimen virheitä.
- Ohitetuista suurin osa on sääntöjä, joita ei ole toteutettu (appositio, lainaukset,
  luettelot ilman konjunktiota lauseenjäsenten välissä ym.).
