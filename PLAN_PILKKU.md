# PLAN_PILKKU — suomen kielen pilkkutarkistin

Tavoite: uusi tarkistin, joka löytää puuttuvat ja ylimääräiset pilkut suomenkielisestä
tekstistä (ensisijaisesti `2026-09-14 ratkaisu.md`). Tarkistin vain varoittaa, ei korjaa.

Tämä dokumentti kerää ensin faktat (säännöt), sitten suunnitelman.

---

## 1. Pilkkusäännöt

Säännöt on tarkistettu Kielitoimiston ohjepankista 2026-09-26 (lähteet kohdassa 1.12).
Merkintä **[ei tarkistettu]** tarkoittaa, ettei ohjepankista löytynyt suoraa ohjetta.

Sarakkeiden merkitys:

- **Pakko** = *kyllä* (pilkku vaaditaan), *ei* (pilkkua ei käytetä), *valinnainen* (molemmat oikein).
- **Tunnistus** arvioi, kuinka helposti sääntö tunnistetaan koneellisesti:
  *helppo* = sanalista riittää, *keski* = tarvitaan morfologia (Voikko),
  *vaikea* = tarvitaan lauserakenteen jäsennys.

### 1.1 Alistuskonjunktiolla alkava sivulause

Alistuskonjunktiot: *että, jotta, koska, kun, kunnes, jos, vaikka, jollei, ellei, kunhan, mikäli*.

| # | Sääntö | Esimerkki | Pakko | Tunnistus |
|---|---|---|---|---|
| S1 | Alistuskonjunktiolla alkava lause erotetaan päälauseesta pilkulla | Ministeri totesi, että asia on käsitelty. | kyllä | helppo (alkupilkku) |
| S1e | Sivulauseen loppu: kun sivulause on virkkeen alussa tai keskellä ja päälause jatkuu sen jälkeen, sivulauseen perään tulee pilkku | Kun tulin kotiin, söin. / Hän sanoi, että jos ehtii, hän tulee. | kyllä | vaikea (loppukohta jäsennyksestä) |
| S1a | Hyvin lyhyt virke: kun päälauseessa on vain yksi sana ja sivulause on 2–3 sanaa, pilkku on valinnainen. Epäsuora kysymys pitää kuitenkin pilkun | Toivon(,) että tulet ajoissa. / Kysyin, onko kaikki kunnossa. | valinnainen | helppo |
| S1b | Kahden peräkkäisen konjunktion väliin ei tavallisesti tule pilkkua | …, mutta jos …; …, että kun … | ei | helppo |
| S1c | Painottava sana konjunktion edellä (*varsinkin, etenkin*): pilkku joko painosanan eteen tai sen ja konjunktion väliin | …, varsinkin jos … / … etenkin, jos … | valinnainen (paikka) | helppo |
| S1d | Välinpitämättömyyttä ilmaisevat rakenteet erotetaan pilkulla muusta virkkeestä | Kävi miten kävi, tämä on voitto. Oli miten oli, … | kyllä | keski |

### 1.2 Moniosaiset konjunktioilmaukset

Ilmaukset: *sitten kun, samalla kun, aina kun, heti kun, sen aikaa kun, silloin kun,
niin että, siten että, sen lisäksi että, ilman että*
(samaa tyyppiä: *sen jälkeen kun, sen sijaan että, siitä huolimatta että, sitä mukaa kuin*).

| # | Sääntö | Esimerkki | Pakko | Tunnistus |
|---|---|---|---|---|
| M1 | Pilkun paikka valinnainen: joko koko ilmauksen eteen tai sen osien väliin. Valinta vaikuttaa painotukseen | Soitan, heti kun pääsen. / Soitan heti, kun pääsen. | valinnainen (paikka). Jossain kohtaa pilkku kuitenkin tarvitaan | helppo |
| M2 | *niin että*: pilkun paikka erottaa tavan (*niin, että*) ja seurauksen (*, niin että*) | | valinnainen | — |
| M3 | Virkkeen alussa (*Sitten kun, Samalla kun, Silloin kun …*) ei *kun*-sanan edelle tarvita pilkkua | Silloin kun tulin, … | ei | helppo |

Tarkistimen kannalta: varoitetaan vain, jos ilmauksen edeltä *ja* sen sisältä puuttuu pilkku.

### 1.3 Relatiivilause

Relatiivisanat: *joka, mikä* ja niiden taivutusmuodot sekä
*jolloin, jonne, joten, jollainen, milloin, minne, miten, millainen*.

| # | Sääntö | Esimerkki | Pakko | Tunnistus |
|---|---|---|---|---|
| S2 | Relatiivilause erotetaan päälauseesta pilkulla | Haluan työpaikan, joka sopii minulle. | kyllä | keski |
| S2a | Päälauseen keskelle upotettu relatiivilause: pilkku molemmin puolin | Pelaajat, joiden nimiä ei mainittu, neuvottelevat. | kyllä | vaikea (loppupilkku) |
| S2b | Korrelaatiton (itsenäinen) relatiivilause: pilkku valinnainen | Teen(,) mitä haluan. (vrt. Teen sitä, mitä haluan.) | valinnainen | keski |

Huom: suomessa relatiivilause erotetaan aina, eikä rajoittavalla ja selittävällä relatiivilauseella ole eroa kuten englannissa.
*joten* on relatiivisana, joten pilkku kuuluu sen eteen.

### 1.4 *se joka*, *se mikä*, *se että*

| # | Sääntö | Esimerkki | Pakko | Tunnistus |
|---|---|---|---|---|
| K1 | Muualla kuin virkkeen alussa: pilkku *se*-pronominin jälkeen | Komitea valitsee sen, joka on pätevin. Kyse on siitä, että … | kyllä | helppo |
| K2 | Virkkeen alussa: pilkku *se*-pronominin jälkeen valinnainen | Se(,) joka saa eniten pisteitä, voittaa. Se(,) että jonottaminen maksaa, harmittaa. | valinnainen | helppo |
| K3 | Keskellä virkettä olevan *joka-, mikä-* tai *että*-lauseen lopussa pilkku ennen päälauseen jatkoa | Se mitä tapahtui, oli outoa. | kyllä | vaikea |

Aineistoon vaikuttaa: *Se mitä tapahtui Billille, voi …* (virkkeen alussa) on oikein.
*…, mutta se mitä tapahtuu, on …* (ei virkkeen alussa) vaatii pilkun: *se, mitä*.
Tämä on rajatapaus: lause alkaa rinnastuskonjunktion jälkeen, mutta ohjepankki puhuu virkkeen
alusta. Tarkistettava. Siihen asti tällaisesta kohdasta varoitetaan matalalla varmuudella.

### 1.5 Epäsuora kysymyslause

| # | Sääntö | Esimerkki | Pakko | Tunnistus |
|---|---|---|---|---|
| S3 | Epäsuora kysymyslause (kysymyssana *kuka, mikä, miten, miksi, missä* … tai *-ko/-kö*) erotetaan pilkulla | Kukaan ei tiedä, missä hän asuu. Kysyin, tuleeko hän. | kyllä | keski |
| S3a | Jos päälause on kysyvä, virkkeen loppuun tulee kysymysmerkki | Tiedättekö, onko huomenna sadetta? | — | — |

*koska* = 'milloin' (puhekieltä) aloittaa epäsuoran kysymyksen, joten pilkku kuuluu:
*kysyvät, koska on oikea hetki*.

### 1.6 Sivulauseiden välissä

| # | Sääntö | Esimerkki | Pakko | Tunnistus |
|---|---|---|---|---|
| S4 | Rinnasteiset sivulauseet, joiden välissä on *ja/tai*: ei pilkkua | …, joka sopii minulle ja jossa voin käyttää kykyjäni. | ei | helppo |
| S5 | Sivulause, joka on alisteinen toiselle sivulauseelle: pilkku | Ilahduin, kun kuulin, että pääset. | kyllä | keski |
| S6 | Rinnasteiset lauseenjäsenet tai sivulauseet ilman konjunktiota: pilkku | He lukivat Kiveä, Saarikoskea, Kilpeä ja Hassista. | kyllä | keski |

### 1.7 Päälauseiden välissä

Rinnastuskonjunktiot: *ja, sekä, tai, vai, eli, mutta, vaan, sillä, eikä*.

| # | Sääntö | Esimerkki | Pakko | Tunnistus |
|---|---|---|---|---|
| R1 | **Täydelliset** päälauseet (oma subjekti ja verbi) erotetaan pilkulla, myös *ja/tai*-sanan edellä | Kesäkuussa he matkustivat Yhdysvalloissa, ja heinäkuussa he olivat Kanadassa. | kyllä | vaikea |
| R1a | Poikkeus: pilkku valinnainen, kun lauseet ovat 1./2. persoonassa, passiivissa, lyhyitä tai kysymyksiä | Tulin kotiin(,) ja söin. | valinnainen | keski |
| R2 | **Vajaat** päälauseet (yhteinen jäsen, yleensä subjekti): ei pilkkua | Perhe kunnosti saunaa ja viimeisteli keittiön. | ei | vaikea |
| R3 | *mutta, vaan*: uusi sääntö noudattaa R1/R2:ta. Täydellinen lause → pilkku. Vajaa lause → pilkku valinnainen (vanha sääntö: aina pilkku, edelleen sallittu) | Salilla on hiljaista, mutta viikonloppuisin siellä käy väkeä. / Lääkärit hyväksyvät akupunktion(,) mutta eivät ginsengiä. | kyllä / valinnainen | keski |
| R4 | *sillä*-lause erotetaan perustelemastaan lauseesta aina pilkulla | Aion kirjoittaa, sillä en osaa muutakaan. | kyllä | keski (*sillä* myös pronomini) |
| R5 | Muut yhdistävät ilmaukset (*kuitenkin, siis, nimittäin, silti* …) täydellisten lauseiden välissä: pilkku | He matkustelivat laajasti, ennättivätpä vielä Havaijillekin. | kyllä | vaikea |

Aineistoon vaikuttaa: esim. *Aviomieheni palasi lopulta mutta ei kestänyt kauaa* on vajaa lause,
joten se on uuden säännön mukaan oikein. Pilkkua ei ole pakko lisätä.

### 1.8 Parirakenteet ja symmetriset rakenteet

| # | Sääntö | Esimerkki | Pakko | Tunnistus |
|---|---|---|---|---|
| P1 | *mitä–sitä, milloin–milloin, toisaalta–toisaalta, yhtäältä–toisaalta, osaksi–osaksi*: pilkku osien väliin | Mitä korkeammalla aurinko on, sitä enemmän altistumme. | kyllä | helppo |
| P2 | *paitsi–myös*: ei yleensä pilkkua | Hän on paitsi nopea myös ketterä. | valinnainen (yleensä ei) | helppo |
| P3 | *saati*: rinnakkaisten ilmausten välissä ei pilkkua. Painokkaan lisäyksen edellä pilkku selventää | ei suuria saati kohtalokkaita / …, saati yöksi pihalle. | valinnainen | helppo |
| P4 | *sekä–että, joko–tai*: rinnastus konjunktiolla, joten yleissäännön (S6) mukaan ei pilkkua lauseenjäsenten väliin. Kokonaisten päälauseiden välissä noudatetaan R1:tä **[ei tarkistettu]** | sekä kehon että mielen / Joko tulet nyt, tai jäät kotiin. | ei / kyllä | helppo / vaikea |
| P5 | *kuten X myös Y*, *samoin kuin X myös Y*: ei pilkkua | Kuten Suomessa myös Saksassa … | ei | helppo |
| P6 | *niin–kuin* (rinnastava): ei pilkkua **[ei tarkistettu]** | niin Suomessa kuin Ruotsissa | ei | helppo |

### 1.9 Vertailu: *kuin*, *kuten*

| # | Sääntö | Esimerkki | Pakko | Tunnistus |
|---|---|---|---|---|
| V1 | Vertailevassa rakenteessa *kuin*-sanan edellä ei yleensä käytetä pilkkua, **myöskään silloin, kun kuin-jaksossa on verbi** | Poika juoksee kuin nuori hirvi. Todellisuus näyttää valoisammalta kuin hän uskalsi toivoa. | ei | helppo |
| V1a | *kuin*-jakso irrallisena jälkilisäyksenä: pilkku valinnainen | Hän vaati huomiota(,) ikään kuin olisi kuuluisuus. | valinnainen | — |
| V2 | *ennen kuin* päälauseen jäljessä: pilkku valinnainen. Päälauseen edellä: pilkku selvyyden vuoksi | Tule(,) ennen kuin sataa. / Ennen kuin lähdet, sammuta valot. | valinnainen / kyllä | keski |
| V3 | *toisin kuin, samoin kuin, aivan kuin*: jos molemmat osat ovat kokonaisia lauseita, pilkku väliin | Toisin kuin monet luulevat, hän ei ole varakas. | kyllä | vaikea |
| V4 | *kuten* = 'esimerkiksi': aina pilkku | Myytävänä oli tarvikkeita, kuten sokeria ja kahvia. | kyllä | keski |
| V5 | *kuten* = 'niin kuin': ei pilkkua, paitsi jos *kuten*-jakso on kokonainen lause | Täällä on mukavaa kuten aina. / Täällä on mukavaa, kuten näette. | ei / kyllä | keski (finiittiverbi) |

### 1.10 Lauseenvastikkeet ja muut rakenteet

| # | Sääntö | Esimerkki | Pakko | Tunnistus |
|---|---|---|---|---|
| L1 | Lauseenvastiketta **ei eroteta** muusta lauseesta pilkulla (temporaalinen, finaalinen, partisiippi-, modaalinen rakenne) | Asetuttuaan Mikkeliin taiteilija toimi … Hän pyysi neuvoani uskoen, että voin auttaa. | ei | keski |
| L2 | Samoin *ilman*-rakenteet ja *tekemällä*-rakenteet: ei pilkkua | | ei | keski |

Aineistoon vaikuttaa: *Ensiksi, auttaaksemme ihmisiä …*. Pilkku on tarpeeton (ks. A2), ja finaalirakennetta *auttaaksemme* ei eroteta.

### 1.11 Lisäykset, puhuttelu, lauseen alun sanat, määritteet

| # | Sääntö | Esimerkki | Pakko | Tunnistus |
|---|---|---|---|---|
| I1 | Puhuttelu erotetaan pilkulla | Maija, tule jo! | kyllä | keski |
| I2 | Appositio eli selittävä lisäys: pilkut molemmin puolin | Mikael Agricola, suomen kirjakielen isä, syntyi Pernajassa. | kyllä | vaikea |
| I3 | Tarkennus erotetaan pilkulla | … takaisin, tosin varsin pitkin hampain. | kyllä | vaikea |
| I4 | *esimerkiksi*-lisäys: pilkku | monet ruoka-aineet, esimerkiksi kala ja pähkinät | kyllä | helppo |
| I5 | Peräkkäiset paikanilmaukset ilman pilkkua | Hän asuu Göteborgissa Ruotsissa. | ei | — |
| I6 | Interjektio ja vastaussana (*kyllä, ei*) erotetaan pilkulla **[ei tarkistettu]** | Voi, miten kaunista! Kyllä, tulen. | kyllä | helppo |
| A1 | Lauseen alun asennetta tai näkökulmaa ilmaiseva sana (*valitettavasti, toisaalta*): ei yleensä pilkkua. Painokkaana pilkku mahdollinen | Valitettavasti lomaan on pitkä aika. | ei (painokkaana valinnainen) | helppo |
| A2 | *ensiksi, toiseksi* jne.: ei tavallisesti pilkkua. Tauottavana tyylikeinona mahdollinen | Ensiksi haluan kiittää. | ei (valinnainen) | helppo |
| A3 | Loppuasemainen asenneilmaus: pilkku tai ajatusviiva | …, ihme kyllä. | kyllä | vaikea |
| D1 | Järjestystä ilmaiseva määrite (*ensimmäinen, toinen, seuraava, entinen, ainoa*) + kuvaileva määrite: pilkku muuttaa merkitystä | toinen korjattu painos ≠ toinen, korjattu painos | merkitysero | — (ei tarkisteta) |
| D2 | Pelkät kuvailevat määritteet: pilkku valinnainen (korostaa) | kapea(,) pitsinen reunus | valinnainen | — |

### 1.12 Lainaukset ja johtolauseet

| # | Sääntö | Esimerkki | Pakko | Tunnistus |
|---|---|---|---|---|
| Q1 | Väitelauseen muotoisen lainauksen jälkeen, ennen johtolausetta: pilkku | "En aio erota", ministeri vastasi. | kyllä | keski (lainausmerkki + johtoverbi) |
| Q2 | Johtolause lainauksen keskellä: pilkut molemmin puolin | "En aio erota", ministeri totesi, "mutta harkitsin sitä." | kyllä | keski |
| Q3 | Kysymys- tai huutomerkki korvaa pilkun | "Pitäisikö minun erota?" ministeri kysyi. | ei | helppo |
| Q4 | Kolmen pisteen jälkeen pilkku valinnainen | "En eroa..."(,) vakuutteli hän. | valinnainen | helppo |

### 1.13 Tavallisimmat virheelliset tai tarpeettomat pilkut

- lauseenvastikkeen ympärillä (L1): *Kotiin tultuaan, hän söi.*
- vajaan päälauseen edellä *ja*-sanan kohdalla (R2): *Perhe kunnosti saunaa, ja viimeisteli keittiön.*
- kahden peräkkäisen konjunktion välissä (S1b): *että, jos*
- *kuin*-vertailun edellä (V1): *pitempi, kuin minä*
- *kuten* = 'niin kuin' ilman verbiä (V5): *mukavaa, kuten aina*
- lauseen alun asenne- tai järjestyssanan jälkeen (A1, A2): *Itse asiassa, kaikki …*, *Ensiksi, …*
- *joka* = jokainen -sanan edellä: *tee se, joka päivä* (sääntö johdettu, ei suoraa ohjetta)
- subjektin ja predikaatin välissä, kun väliin ei ole upotettu sivulausetta: *Iso kirja, on hyvä.*

### 1.14 Sanat, jotka näyttävät sidesanoilta mutta eivät ole

Nämä eivät laukaise sivulausesääntöä (johdettu kieliopista, ei ohjepankin ohje):

- *joka* = jokainen: *joka kerta, joka päivä*
- *sillä* = pronomini: *sillä hetkellä, sillä ei ole väliä*
- *vaan* = puhekielen *vain*: *tuosta vaan*
- *vaikka* = esimerkiksi: *otetaanpa vaikka*
- *mitä* + superlatiivi: *mitä tavallisimmalta*
- *kuka/mikä/mitä tahansa, milloin vain, missä ikinä*: pronomini-ilmauksia, eivät sivulauseen alkuja

### 1.15 Muut

- Desimaalipilkku (*3,5*) ja sivu- ja rivialueet (*10-21*) pitää ohittaa tokenisoinnissa.
- **Muut rajamerkit:** ajatusviiva (*—*, *–*), sulkeet, kaksoispiste ja puolipiste voivat
  merkitä lauserajan pilkun sijasta. Jos rajalla on jokin näistä, pilkkua ei vaadita
  (esim. *Tämä ei ole kenenkään vika — mutta se …*).

### 1.16 Lähteet (Kielitoimiston ohjepankki, luettu 2026-09-26)

- [Pilkku](https://kielitoimistonohjepankki.fi/ohje/pilkku/)
- [Pilkku ja alistuskonjunktiolla alkava lause](https://kielitoimistonohjepankki.fi/ohje/pilkku-ja-alistuskonjunktiolla-esim-etta-jos-alkava-lause/)
- [Pilkku moniosaisissa konjunktioilmauksissa](https://kielitoimistonohjepankki.fi/ohje/pilkku-moniosaisissa-konjunktioilmauksissa-silloin-kun-niin-etta/)
- [Pilkku ja joka-, mikä-relatiivilause](https://kielitoimistonohjepankki.fi/ohje/pilkku-ja-joka-mika-relatiivilause/)
- [Pilkku se joka- ja se että -ilmauksissa](https://kielitoimistonohjepankki.fi/ohje/pilkku-se-joka-ja-se-etta-ilmauksissa/)
- [Pilkku ja epäsuora kysymyslause](https://kielitoimistonohjepankki.fi/ohje/pilkku-ja-epasuora-kysymyslause-han-kysyi-tulenko-ajoissa/)
- [Pilkku sivulauseiden välissä](https://kielitoimistonohjepankki.fi/ohje/pilkku-sivulauseiden-valissa/)
- [Pilkku päälauseiden välissä](https://kielitoimistonohjepankki.fi/ohje/pilkku-paalauseiden-valissa/)
- [Pilkku ja mutta, vaan](https://kielitoimistonohjepankki.fi/ohje/pilkku-ja-mutta-vaan/)
- [Pilkku ja sillä](https://kielitoimistonohjepankki.fi/ohje/pilkku-ja-silla/)
- [Pilkku rinnasteisten lauseenjäsenten ja luettelon osien välissä](https://kielitoimistonohjepankki.fi/ohje/pilkku-rinnasteisten-lauseenjasenten-ja-luettelon-osien-valissa/)
- [Pilkku ja mitä–sitä, toisaalta–toisaalta](https://kielitoimistonohjepankki.fi/ohje/pilkku-ja-mita-sita-toisaalta-toisaalta/)
- [Pilkku ja paitsi–myös](https://kielitoimistonohjepankki.fi/ohje/pilkku-ja-paitsi-myos/)
- [Pilkku ja saati](https://kielitoimistonohjepankki.fi/ohje/pilkku-ja-saati/)
- [Pilkku kuin-ilmauksissa](https://kielitoimistonohjepankki.fi/ohje/pilkku-kuin-ilmauksissa/)
- [Konjunktiot: kuten](https://kielitoimistonohjepankki.fi/ohje/konjunktiot-kuten/)
- [Pilkku ja lauseenvastike](https://kielitoimistonohjepankki.fi/ohje/pilkku-ja-lauseenvastike-auringon-noustua-lahdimme/)
- [Pilkku ja lauseenalkuinen valitettavasti, toisaalta](https://kielitoimistonohjepankki.fi/ohje/pilkku-ja-lauseenalkuinen-valitettavasti-toisaalta/)
- [Pilkku ja puhutteluilmaus, tarkennus tai muu lisäys](https://kielitoimistonohjepankki.fi/ohje/pilkku-ja-puhutteluilmaus-tarkennus-tai-muu-lisays/)
- [Pilkku määritteiden välissä](https://kielitoimistonohjepankki.fi/ohje/pilkku-maaritteiden-valissa-toinen-hyva-vitsi/)
- [Pilkku lainauksen ja johtolauseen jäljessä](https://kielitoimistonohjepankki.fi/ohje/pilkku-lainauksen-ja-johtolauseen-jaljessa/)

Lukematta jäivät: *Pilkku titteleiden välissä* (ei tarkistimen kannalta olennainen).

---

## 2. Havainnot edellisestä skriptistä (`pilkut.py`)

Vanha skripti on lähtötaso, johon uutta tarkistinta verrataan (luku 5).

**Rakenne** (`~/Documents/ratkaisu/pilkut.py`, 284 riviä): käsittelee md-tiedoston rivi
kerrallaan, tokenisoi säännöllisellä lausekkeella ja käyttää Voikkoa finiittisyyden ja
sanaluokan tunnistukseen. Ei jäsennystä. Varoitus osoittaa riviin, ei sarakkeeseen.

**Säännöt:** alistuskonjunktiot (varmuus sanakohtainen: *että* high, *kun/jos/vaikka* low),
relatiivipronominit, demonstratiivi + sivulause (*se mitä*), epäsuora kysymys (finiittiverbi +
kysymyssana), *sillä*, *vaan*, sekä virke, joka alkaa sivulauseella mutta jossa ei ole pilkkua
(loppupilkku). Poikkeuksia: *joka* + substantiivi, *sekä–että*, moniosaisten ilmausten
alkuosat, kysymyssana + *tahansa/hyvänsä/ikinä*.

**Tulos koko dokumentilla** (2026-09-26): 99 varoitusta: kysymys 54 (low), demonstratiivi 24
(high), kun 9, että 5, jos 2, muut 5.

**Kultainen otos 1–20** (arviointi/tulokset.md): tarkkuus 100 %, kattavuus 14 % (1/7).
Löysi yhden epäsuoran kysymyksen; ohitti kolme epäsuoraa kysymystä (*emme tienneet oliko*:
*-ko*-kysymystä ei tunnisteta) ja kaikki kolme R1-tapausta (ei sääntöä).

**Johtopäätös:** vanha skripti on tarkka mutta kattaa vain sanalistalla tunnistettavat
sivulauseen alut. Suurin aukko: *-ko/-kö*-kysymykset ja täydellisten päälauseiden välinen
*ja* (R1).

## 3. Tunnistusmenetelmä

### 3.1 Periaatteet

- **Yksikkö on lause virkkeen sisällä**, ei token. Pilkkusäännöt koskevat lauseiden välisiä
  rajoja (sivulause/päälause, rinnastus). Tokenit ovat välivaihe.
- **Rajojen tunnistus ei saa nojata pilkkuihin**, koska juuri puuttuvat pilkut ovat etsinnän
  kohde. Rajat päätellään sanoista, verbeistä ja jäsennyksestä.
- **Deterministisyys:** sama syöte ja samat mallit antavat aina saman tuloksen. Stanza ajetaan
  CPU:lla, koska GPU-laskenta (CUDA) ei ole bittitarkasti toistettavaa. Kiinnitetään `stanza`-,
  `torch`- ja malliversio.
- **Varoitus osoittaa lähdetiedoston riviin ja sarakkeeseen.** Tiedostoa ei muokata.
- **Jäsennyksen on voitettava lähtötaso.** Jäsennykseen perustuva sääntö otetaan käyttöön vain,
  jos se parantaa sanalistaan perustuvan lähtötason tulosta testiaineistossa (luku 5).

### 3.2 Arkkitehtuuri: yksi paketti, vaiheet moduuleina

Ohjelmisto on yksi Python-paketti. Vaiheet ovat erillisiä moduuleja, joilla on selvät
rajapinnat (dataluokat), joten jokaisen voi testata ja vaihtaa erikseen. Erillisiä prosesseja ja
JSON-välitiedostoja ei tarvita: yhden dokumentin käsittely kestää minuutteja.

Tiedostoon talletetaan vain jäsennykset (`.conllu`), koska jäsennys on ainoa raskas vaihe.
Sääntöjä muutettaessa sitä ei ajeta uudelleen. Muut välitulokset voi tulostaa JSON-muodossa
virheenetsintää varten (`--dump`).

```
alkuperäinen.md
  │ 1. esikasittelija  → leipäteksti + offset-kartta
  │ 2. jasennin        → jasennys_A.conllu + jasennys_B.conllu   (välimuisti)
  │ 3. lauseistaja     → lauseet ja rajat
  │ 4. saantotarkistin → varoitukset
  ▼ 5. raportoija      → tiedosto:rivi:sarake: [varmuus/sääntö] viesti
```

| # | Moduuli | Syöte | Tuloste | Työkalut |
|---|---|---|---|---|
| 1 | `esikasittelija` | alkuperäinen teksti (md, myöhemmin txt/odt) | leipäteksti, offset-kartta | Python, Voikko (tavutus) |
| 2 | `jasennin` | leipäteksti | `jasennys_A.conllu`, `jasennys_B.conllu` | Stanza |
| 3 | `lauseistaja` | jäsennykset | lauseet ja rajat | Python |
| 4 | `saantotarkistin` | lauseet ja rajat, tokenit | varoitukset | Python, sanastot, (Voikko?) |
| 5 | `raportoija` | varoitukset, offset-kartta, alkuperäinen | tekstiraportti | Python |

Komentorivin ajuri (`pylkuta tiedosto.md`) ajaa koko putken ja käyttää välimuistissa olevaa
jäsennystä, jos leipäteksti ja malliversio eivät ole muuttuneet.

Voikon rooli:
- **Tavutuksen purku** esikäsittelijässä.
- **Mahdollinen apulainen** sääntötarkistimessa (finiittisyys, monitulkintaiset sanat).
  Stanzan morfologia voi tehdä tämän tarpeettomaksi; päätetään Stanza-kokeen jälkeen.
- **Oikeinkirjoitus** ei kuulu pilkkuputkeen (ks. 3.8).
- Voikko **ei** tunne pilkkusääntöjä (testattu: puuttuvia pilkkuja ennen *että, mutta, joka*
  ei havaittu).

Ympäristö: `~/pylkutus/.venv`, luotu komennolla
`/usr/bin/python3 -m venv --system-site-packages`, jotta `libvoikko` (järjestelmän paketti) ja
pip-asennettu Stanza toimivat samassa ympäristössä. Vaatii paketin `python3.12-venv`.
Asennettu: `stanza` 1.14.0, `torch` 2.14.0.
UDPipe 1 (`ufal.udpipe`) on valinnainen vertailujäsennin myöhemmin.

### 3.3 Moduuli 1: esikäsittelijä

Tehtävä: poimia **leipäteksti** ja säilyttää paikkatieto.

- Karsitaan: otsikot, sivunumerot, ylä- ja alatunnisteet, sisällysluettelo, kuvatekstit,
  span-tagit ja muu markup, `*`/`_`-korostukset, `\`-merkit, pehmeät tavuviivat (U+00AD).
- **Otsikot tunnistetaan ensisijaisesti rakenteesta** (md:n `#`-otsikot). Lyhyen rivin
  heuristiikka (alle ~30 merkkiä, ei virkkeen loppumerkkiä) on vain varakeino rakenteettomille
  riveille, eikä sitä sovelleta riveihin, joissa on lainausmerkki tai ajatusviiva (repliikit).
- Rivin lopun tavutusviivat puretaan: *toipu-*⏎*minen* → *toipuminen*. Viiva säilyy, jos
  yhdistetty sana ei ole Voikon mukaan oikein mutta viivallinen on (*AA-*⏎*laiset*).
- Kappaleen sisäiset rivinvaihdot muutetaan välilyönneiksi; kappaleraja säilyy tyhjänä rivinä.
- Jokainen karsittu rivi kirjataan lokiin, jotta näkee, ettei leipätekstiä hävinnyt.
- **Offset-kartta:** leipätekstin jokaiselle merkkivälille alkuperäisen tiedoston rivi ja
  sarake. Ilman tätä varoitukset eivät osu alkuperäisiin riveihin.

**Havainnot aineistosta** (`~/Documents/ratkaisu/2026-09-14 ratkaisu.md`, tarkistettu 2026-09-26):
- 2058 riviä, joista 1002 tyhjää. Jokainen kappale on yhdellä rivillä, joten kappaleen sisäisiä
  rivinvaihtoja ei ole.
- Rivin lopun tavutusviivoja ei ole (0 kpl), joten tavutuksen purkua ja Voikkoa ei tarvita
  md-syötteelle. Toiminto toteutetaan vasta txt-syötteen yhteydessä.
- 117 `#`-otsikkoa ja 97 `<span id="anchor-N">`-ankkuria (odt-muunnoksen jäänteitä), 2 pehmeää
  tavuviivaa (*e­sittelee*), `**lihavointi**` ja rivin lopun kaksoisvälilyönti (md:n rivinvaihto).
- 66 luettelon riviä (`1.  Mikä oli ongelma`). Luettelon kohta säilytetään omana kappaleenaan,
  koska se jäsennetään omana virkkeenään eikä haittaa muuta tekstiä.
- Alussa on otsikon kaltaisia rivejä ilman `#`-merkkiä (*OPASTUS ISON KIRJAN OHJELMAAN*).
  Ne tunnistetaan heuristiikalla (ei virkkeen loppumerkkiä, lyhyt tai kokonaan isoilla
  kirjaimilla).
- Lyhyt oikea virke on olemassa (*Kaveri oli tietysti oikeassa.*), joten pelkkä pituusraja ei
  riitä otsikon tunnistukseen: loppumerkki ratkaisee.

### 3.4 Moduuli 2: jäsennin

**Virkkeet ja tokenit**
- Stanzan tokenisointi ja virkkeiden erottelu, jonka tulos tarkistetaan suomen ansoja vasten:
  lyhenteet (*tri., jne., esim., ns., mm., vrt., klo, s.*), järjestysluvut (*14. päivä*),
  päiväykset, nimikirjaimet (*Bill W.*), kolme pistettä, lainauksen sisäinen `?`/`!`
  (*"Tuletko?" hän kysyi*).
- Tarvittaessa oma esierottelu (lyhennelista) ja Stanzalle valmiiksi pilkotut virkkeet.
- Luvut ja alueet (*10-21*, *3,5*) eivät saa hajota pilkuiksi.
- **Tokenisointi tehdään kerran**, jäsennyksen A yhteydessä.

**Kaksoisjäsennys**
- **Jäsennys A:** virke sellaisenaan (Stanzan tokenisointi ja jäsennys).
- **Jäsennys B:** A:n tokenit, joista erottavat pilkut on poistettu, syötetään Stanzalle
  valmiiksi tokenisoituna (`tokenize_pretokenized=True`). Virkejako ja tokenit ovat siksi
  identtiset, kohdistus on pelkkä indeksikartta ja offsetit periytyvät A:sta.
- Vain pilkkutokenit poistetaan. Desimaalipilkku on osa lukutokenia, eikä siihen kosketa
  (koeskriptin `strip_commas` poistaa nyt myös desimaalipilkut ja korjataan).
- Molemmat CoNLL-U-muodossa. Jokaiseen tokeniin talletetaan offset leipätekstiin
  (`MISC`-sarakkeessa, esim. `start_char=…|end_char=…`).
- Mallin versio kirjataan tiedoston alkuun (deterministisyys ja välimuistin mitätöinti).

### 3.5 Moduuli 3: lauseistaja

Tehtävä: UD-puusta lauseet ja niiden väliset rajat.

Pilkku tallennetaan tokenien väliseen rakoon (`comma_before[i]`), ei omaksi tokeniksi. Samoin
muut rajamerkit (1.15).

**Lauseen pää** (*clause head*) on sana, jolla on jokin seuraavista suhteista. Vastaavuus on
hypoteesi, joka tarkistetaan Stanza-kokeessa (vaihe V3, luku 7).

| UD-suhde | Merkitys | Säännöt |
|---|---|---|
| `root` | päälause | — |
| `advcl` | adverbiaalilause (kun, jos, koska, vaikka) | S1, S1e |
| `ccomp` | että-lause, epäsuora kysymys | S1, S1e, S3 |
| `acl:relcl` | relatiivilause, myös *se mitä tapahtui* (kiinnittyy *se*-sanaan) | S2, S2a, K1–K3 |
| `csubj`, `csubj:cop` | korrelaatiton subjektilause (*Mitä tapahtui, oli outoa.*) | S2b, K3 |
| `conj` (verbiin) | rinnasteinen lause | R1, R2, S4 |
| `parataxis` | rinnastus ilman konjunktiota | R1 |

**Finiittisyys (L1).** Lause on finiittinen, jos jokin seuraavista pätee:
- pää on `VerbForm=Fin`
- pään `aux`- tai `cop`-lapsi on `VerbForm=Fin`
- päällä on `mark`-lapsi, joka on alistuskonjunktio.

Stanzan `VerbForm=Fin` hyväksytään vain, jos Voikolla on sanalle finiittinen analyysi tai
Voikko ei tunne sanaa (V3: *auttaaksemme* oli merkitty finiittiseksi; ks. `kokeet/tulokset.md`).

Pelkkä pään `VerbForm` ei riitä, koska suomen UD:ssä monen finiittisen lauseen pää on
partisiippi tai nomini:
- kieltolause *kun hän ei tullut*: pää *tullut* (`Part`), *ei* on `aux`
- perfekti *koska hän on lähtenyt*: pää `Part`, *on* on `aux`
- kopulalause *vaikka hän on opettaja*: pää *opettaja*, *on* on `cop`.

Ei-finiittiset `advcl`, `acl` ja `xcomp` ovat lauseenvastikkeita, eikä niitä eroteta pilkulla.

**Täydellinen vai vajaa lause (R1, R2, R3).** Pelkkä `nsubj`-suhteen puuttuminen ei tee lauseesta
vajaata. Monessa täydellisessä lauseessa ei ole `nsubj`:ia: eksistentiaalilause (*Salilla on
hiljaista*), nesessiivilause (*Minun täytyy lähteä*), säälause (*Sataa*), passiivi sekä 1. ja 2.
persoonan lause ilman pronominia (*Tulin kotiin*). Päättely (alustava, tarkistetaan kokeessa):
- `conj`-lauseella on oma `nsubj` tai `nsubj:cop`: täydellinen.
- Ei subjektia, verbi 1./2. persoonassa tai passiivissa: täydellinen, mutta R1a:n mukaan
  pilkku on valinnainen.
- Ei subjektia, verbi 3. persoonassa, ja edellisellä rinnasteisella lauseella on subjekti,
  joka sopii verbin kanssa: vajaa (yhteinen subjekti).
- Muut tapaukset (esim. eksistentiaali-, nesessiivi- ja säälauseet): ratkaisematon, joten
  varoitus annetaan korkeintaan matalalla varmuudella.

Jokaisesta lauseesta talletetaan:
- ensimmäinen ja viimeinen token (lauseen jänne alipuusta)
- tyyppi (pää-, sivu-, relatiivi-, kysymys- tai rinnasteinen lause)
- aloittava sana: `mark`/`cc`/relatiivi- tai kysymyssana
- finiittisyys (yllä) sekä täydellisyys, persoona ja passiivi (R1, R1a, R2)
- upotettu vai ei (jatkuuko ylempi lause sen jälkeen) → S1e, S2a, K3
- onko virkkeen alussa tai lauseen alussa rinnastuskonjunktion jälkeen → K2, M3, 1.4:n rajatapaus

**Raja** on tokenien väli *i* (tokenien *i−1* ja *i* välissä), jossa jonkin lauseen jänne alkaa
tai päättyy muualla kuin virkkeen reunalla. Kaksi jäsennystä löytävät saman rajan, jos väli on
sama; lausetyyppi saa erota. Jokaisesta rajasta talletetaan: sijainti, lauseet molemmin puolin,
onko pilkku, onko muu rajamerkki (1.15) ja löytyikö raja jäsennyksestä A, B vai molemmista.

### 3.6 Moduuli 4: sääntötarkistin

- Jokaiselle rajalle haetaan sääntö luvun 1 taulukoista: vaaditaanko pilkku, onko se kielletty
  vai valinnainen.
- Jos rajalla on muu rajamerkki (ajatusviiva, sulkeet, kaksoispiste, puolipiste), pilkkua ei
  vaadita.
- Sanastot (ja tarvittaessa Voikko) hoitavat erikoistapaukset ennen sääntöä:
  - moniosaiset ilmaukset (*heti kun, sen jälkeen kun, niin että*): pilkku joko ilmauksen eteen
    tai sen sisälle (M1)
  - kaksi peräkkäistä konjunktiota (S1b)
  - ei-sidesanat (*joka kerta, sillä hetkellä, kuka tahansa, mitä* + superlatiivi, luku 1.14)
  - *kuin*-vertailu (V1), *kuten* (V4/V5), parirakenteet (P1–P6)
- Lisäksi pilkut, jotka eivät ole millään rajalla, tarkistetaan (luku 1.13: lauseenvastike,
  A1/A2, V1 …).
- Jokainen sääntö on oma funktionsa, tunnuksena luvun 1 koodi (S1, R3 …).

**Varmuus: puuttuvat pilkut** arvioidaan jäsennyksestä A. Kun pilkku puuttuu, A:n syötteestä
se puuttuu jo valmiiksi, ja B eroaa A:sta vain muiden pilkkujen osalta. B ei siis tuo kohtaan
lisänäyttöä. Varmuus määräytyy säännön tunnistusluokasta (helppo/keski/vaikea) ja siitä,
perustuuko sääntö sanalistaan vai jäsennykseen.

**Varmuus: ylimääräiset pilkut** arvioidaan A/B-vertailulla. B on jakauman ulkopuolella, koska
malli on opetettu pilkutetulla tekstillä. Se on siis heikompi jäsennys eikä neutraali todistaja,
ja sitä käytetään vain tukena.

| Raja A | Raja B | Pilkku | Tulkinta |
|---|---|---|---|
| on | on/ei | ei | puuttuva pilkku, jos sääntö vaatii (B ei vaikuta) |
| ei | on | ei | ei varoitusta oletuksena; `--min low` näyttää (B:n raja voi olla jäsennysvirhe) |
| ei | ei | ei | kunnossa |
| on | on | on | kunnossa |
| on | ei | on | mahdollisesti ylimääräinen (raja syntyi pilkun ansiosta); varoitus vain, jos sanastosääntö (1.13) tukee |
| ei | on | on | epäjohdonmukainen (A ei näe rajaa pilkusta huolimatta); ei varoitusta, kirjataan lokiin |
| ei | ei | on | pilkku ilman rajaa: tarkistetaan luvun 1.13 säännöt (lauseenvastike, A1/A2, V1 …) |

Sääntötaulukon *pakko*-sarake painaa: *valinnainen* ei tuota varoitusta oletuksena.

### 3.7 Moduuli 5: raportoija

- Yhdistää varoitukset offset-karttaan.
- Tuloste: `tiedosto:rivi:sarake: [varmuus/sääntö] viesti`, konteksti ja ehdotus.
- Suodatus: `--min high|medium|low`, `--rule S1`, `--tyyli` (valinnaiset pilkut mukaan).
- Myöhemmin muita muotoja (esim. HTML, LibreOffice-kommentit).

### 3.8 Oikeinkirjoitus (myöhemmin, ei osa pilkkuputkea)

- Oma komento, joka ajaa Voikko-tarkistuksen sana kerrallaan leipätekstistä; ehdotukset mukaan.
- Kirjoitusvirhe (esim. *Han*) voi sekoittaa jäsentimen, mutta koska virheitä ei korjata
  automaattisesti, tarkistuksen ajaminen ennen jäsennystä ei auta. Tulos on rinnakkainen
  raportti.
- Poikkeuslista (erisnimet, lainasanat: *Silkworth, Akron, Ebby* …) omassa tiedostossaan.

### 3.9 Hakemistorakenne

```
~/pylkutus/
  PLAN_PILKKU.md
  pyproject.toml       # pytest-asetukset ja merkinnät (stanza, hidas)
  .venv/
  kokeet/              # Stanza-koe ja sen tulokset
  pylkutus/
    tyypit.py          # dataclassit: Leipateksti, Token, Virke, Lause, Raja, Varoitus
    esikasittelija.py
    jasennin.py
    conllu.py          # CoNLL-U-luku ja -kirjoitus
    lauseistaja.py
    saannot/           # yksi moduuli sääntöryhmää kohden (s1.py, s2.py, r.py …)
    saantotarkistin.py # sääntörekisteri ja ajo
    raportoija.py
    sanastot.py        # konjunktiot, moniosaiset, ei-sidesanat, poikkeuslistat
    lahtotaso.py       # sanalistaan perustuva vertailutarkistin (luku 5)
    arviointi.py       # kultaisen standardin luku ja mittari
    oikeinkirjoitus.py # myöhemmin
  pylkuta              # ajuri
  tests/
    fixtures/          # pienet md-tiedostot ja jäädytetyt .conllu-tiedostot
    saannot/           # esimerkkiparit luvun 1 taulukoista (oikein/väärin)
  arviointi/           # kultainen standardi, synteettinen aineisto, mittaustulokset
```

### 3.10 Järjestys

Toteutusvaiheet ja niiden testit: ks. luku 7.

## 4. Varmuusluokat ja tulostusmuoto

Alustava luokitus, tarkennetaan mittausten perusteella:

- **high:** sanalistaan perustuva sääntö (tunnistus *helppo*), pakollinen pilkku.
- **medium:** jäsennykseen perustuva sääntö (tunnistus *keski*), pakollinen pilkku.
- **low:** tunnistus *vaikea*, ratkaisematon täydellisyys (3.5), rajatapaukset (esim. 1.4) ja
  ylimääräiset pilkut, joita vain A/B-vertailu tukee.

Alustavat tavoitteet: high-luokan tarkkuus (precision) vähintään 90 %, kaikkien luokkien yhteinen
tarkkuus vähintään 70 %. Kattavuus (recall) raportoidaan, mutta sille ei aseteta alarajaa ennen
lähtötason mittausta.

Tulostusmuoto: ks. 3.7.

## 5. Testiaineisto ja mittari

**Aineistot**
- **Yksikkötestit** (`tests/`): oikein/väärin-esimerkkiparit kustakin luvun 1 säännöstä.
- **Synteettinen aineisto:** toimitettua suomenkielistä tekstiä, josta pilkut poistetaan;
  mitataan, löytyvätkö ne takaisin. Ylimääräisiä pilkkuja varten pilkkuja lisätään
  satunnaisiin kohtiin, jotka eivät ole lauserajoja. UD_Finnish-TDT:tä ja -FTB:tä ei käytetä,
  koska Stanzan oletusmalli (`combined`) on opetettu molemmilla. Tarvitaan muuta toimitettua
  asiatekstiä.
- **Käsin merkitty otos:** noin 50 kappaletta `ratkaisu.md`:stä. Jokainen pilkkukohta ja
  jokainen lauseraja merkitään: pakollinen pilkku puuttuu, ylimääräinen pilkku, valinnainen,
  kunnossa.

**Mittarit**
- Tarkkuus ja kattavuus erikseen puuttuville ja ylimääräisille pilkuille, säännöittäin ja
  varmuusluokittain.
- Valinnaiset kohdat eivät ole virheitä kumpaankaan suuntaan.

**Lähtötaso**
- (a) vanha `pilkut.py`
- (b) sanalistaan perustuva tarkistin: sidesana tai relatiivisana ilman edeltävää pilkkua,
  poikkeuksina luvun 1.14 ei-sidesanat ja luvun 1.2 moniosaiset ilmaukset.

## 6. Avoimet kysymykset

- Varoitetaanko valinnaisista pilkuista (S1a, S2b, K2, M1, R1a, R3, V1a, V2, A1, A2)?
  Ehdotus: ei varoiteta, tai varoitetaan vain erillisellä lipulla (`--tyyli`).
- Toimiiko täydellisen ja vajaan lauseen päättely (3.5) Stanzan puilla? Selviää kokeessa
  (vaihe V3, luku 7).
- I6 (interjektiot), P4 (sekä–että, joko–tai) ja P6 (niin–kuin): ohjepankista ei löytynyt
  suoraa ohjetta.
- K1/K2: onko lauseen alku rinnastuskonjunktion jälkeen "virkkeen alku" (1.4)?
- **Vaihtoehtoinen menetelmä: sekvenssiluokittelija.** Esim. FinBERT, joka ennustaa pilkun
  todennäköisyyden jokaiseen tokenien väliin. Opetusdataa on rajattomasti (mikä tahansa
  toimitettu teksti), ja malli antaa suoraan todennäköisyyden sekä puuttuvalle että
  ylimääräiselle pilkulle. Ei valita nyt, koska se ei nimeä sääntöä (varoitukseen ei saa
  sääntökoodia eikä ohjepankin viitettä) ja opetus vaatii datan valmistelua ja GPU-työtä.
  Palataan, jos jäsennykseen perustuva tarkistin ei voita lähtötasoa. Myös yhdistelmä on
  mahdollinen: malli ehdottaa, säännöt selittävät ja suodattavat.

## 7. Toteutusvaiheet

Jokainen vaihe tuottaa jotain, jonka voi ajaa ja tarkistaa ennen seuraavaa vaihetta. Vaiheen
kuvauksessa on tuotos, rajapinta, automaattiset testit, käsin tehtävä tarkistus ja
**valmis kun** -ehto. Seuraavaan vaiheeseen siirrytään vasta, kun ehto täyttyy.

### 7.1 Testauskäytännöt

- Testikehys `pytest`. Asetukset tiedostossa `pyproject.toml`.
- **Nopeat testit** eivät käytä Stanzaa: ne lukevat jäädytettyjä `.conllu`-tiedostoja
  kansiosta `tests/fixtures/`. Ajo: `pytest -m "not stanza"`, tavoite alle 5 s.
- **Stanza-testit** merkitään `@pytest.mark.stanza`. Ne ajetaan vaiheen lopussa ja aina, kun
  jäsennin tai malliversio muuttuu.
- **Jäädytys:** kun Stanza-tuloste on tarkistettu käsin, se tallennetaan `tests/fixtures/`-kansioon
  ja siitä tulee nopean testin syöte. Näin lauseistajaa ja sääntöjä voi kehittää ilman
  jäsennintä.
- **Tilannekuvatestit** (*snapshot*): koko dokumentin välitulos (leipäteksti, virkejako,
  lausesulut) tallennetaan tekstitiedostoon. Muutos näkyy `git diff`:nä ja hyväksytään käsin.
  Projekti laitetaan versionhallintaan (`git init`) vaiheessa V0.
- **Invariantit** tarkistetaan koko dokumentilla jokaisen ajon yhteydessä (`--tarkista`),
  esim. offsetit osuvat oikeisiin merkkeihin.
- **Mittaus:** vaiheesta V1 alkaen `python -m pylkutus.arviointi` tulostaa tarkkuuden ja
  kattavuuden säännöittäin. Tulokset kirjataan tiedostoon `arviointi/tulokset.md`
  päivämäärän kanssa, jotta kehitys näkyy.

### 7.2 Tietotyypit (`tyypit.py`)

Kirjoitetaan ennen vaihetta V1, koska kaikki vaiheet käyttävät niitä.

```python
@dataclass
class Leipateksti:
    teksti: str              # kappaleet erotettu rivillä "\n\n"
    alkuperainen: str        # lähdetiedoston sisältö
    kartta: list[int]        # leipätekstin merkki i -> alkuperäisen merkin indeksi
    def rivi_sarake(self, i: int) -> tuple[int, int]: ...

@dataclass
class Token:
    i: int                   # indeksi virkkeessä, pilkut mukaan lukien (A)
    teksti: str
    alku: int                # offset leipätekstiin
    loppu: int
    lemma: str; upos: str; feats: dict[str, str]
    head: int; deprel: str   # head 0 = juuri

@dataclass
class Virke:
    tokenit: list[Token]     # kaikki sanat paitsi pilkut; muut välimerkit ovat tokeneita
    rako: list[str | None]   # rako[i] = "," jos pilkku tokenin i edellä, muuten None;
                             # pituus len(tokenit) + 1

@dataclass
class Lause:
    paa: int; alku: int; loppu: int
    tyyppi: str              # paa | sivu | relatiivi | kysymys | rinnasteinen
    aloittaja: int | None    # mark-, cc-, relatiivi- tai kysymyssanan indeksi
    finiittinen: bool
    taydellisyys: str        # taydellinen | vajaa | ratkaisematon
    upotettu: bool; virkkeen_alussa: bool

@dataclass
class Raja:
    rako: int                # tokenien rako-1 ja rako välissä
    vasen: Lause; oikea: Lause
    merkki: str | None
    lahde: str               # A | B | AB

@dataclass
class Varoitus:
    saanto: str              # esim. "S1"
    varmuus: str             # high | medium | low
    alku: int; loppu: int    # offset leipätekstiin
    toimenpide: str          # lisaa | poista
    viesti: str
```

Rajapinta on luonnos. Kentät tarkentuvat vaiheissa, mutta muutos kirjataan tähän.

Muutos V5:ssä: vain pilkut siirretään rakoihin. Muut rajamerkit (ajatusviiva, sulkeet,
kaksoispiste, puolipiste) jäävät tokeneiksi, jotta A:n ja B:n sanalistat ovat identtiset.
A ja B jäsennetään samoista valmiiksi pilkotuista sanoista (tokenisointi ja MWT kerran,
sitten virkejaon korjaus lyhennelistalla, sitten jäsennys).

### 7.3 Vaiheet

#### V0 Ympäristö

- Ladataan suomen malli: `stanza.download("fi")`. Tällä hetkellä `~/.cache/stanza/1.14.0/`
  sisältää vain `resources`-tiedoston, joten mallia ei ole ladattu.
- Asennetaan `pytest`. Luodaan `pyproject.toml`, `git init` ja `.gitignore` (`.venv/`,
  välimuisti).
- Testit (`tests/test_ymparisto.py`):
  - `import libvoikko` ja `Voikko("fi").analyze("talo")` palauttaa analyysin
  - Stanza-putki latautuu CPU:lle ja jäsentää virkkeen *Hän tuli kotiin.* (merkintä `stanza`)
  - versioiden tulostus: `stanza`, `torch`, malli.
- **Valmis kun:** `pytest` menee läpi.

#### V1 Arviointiaineisto ja mittari

Tuotos: `pylkutus/arviointi.py`, `arviointi/kulta/*.md`, `arviointi/synteettinen/`.

**Kultaisen standardin merkintätapa.** Teksti kirjoitetaan sellaisenaan, ja jokainen
pilkkukohta, josta on tehty päätös, merkitään hakasulkeilla:

| Merkintä | Merkitys |
|---|---|
| `[+,]` | pakollinen pilkku puuttuu tästä |
| `[-,]` | tässä oleva pilkku on ylimääräinen (merkintä pilkun paikalle) |
| `[?,]` | valinnainen pilkku puuttuu tästä |
| `[?-,]` | tässä oleva pilkku on valinnainen |

Merkinnän perään voi kirjoittaa säännön: `[+,S1]`. Merkitsemätön kohta tulkitaan oikeaksi.

**Mittari.** `vertaa(varoitukset, kulta) -> Tulos`:
- Varoitus osuu, jos sen rako on sama kuin kultaisen merkinnän rako ja toimenpide sama.
- Valinnaiseen kohtaan osuva varoitus ei ole virhe eikä osuma. Se lasketaan erikseen.
- Tulos säännöittäin ja varmuusluokittain: osumat, väärät hälytykset, ohitukset, tarkkuus,
  kattavuus.

**Aineistot:**
- Kultainen otos: 50 kappaletta `ratkaisu.md`:stä tasaisesti koko dokumentin alueelta
  (siemenluku kiinnitetään). Ensin 20 kappaletta, jotta mittari saadaan käyttöön nopeasti.
  Merkintä: Claude tekee luonnoksen, käyttäjä tarkistaa ja korjaa.
- Synteettinen aineisto: toimitetun tekstin virkkeet (ei TDT eikä FTB, ks. luku 5), joista
  poistetaan kaikki pilkut (kulta: `[+,]` jokaiseen poistettuun kohtaan) ja toiseen versioon
  lisätään pilkkuja satunnaisiin kohtiin, jotka eivät ole lauserajoja (kulta: `[-,]`).
  Huomio: synteettisessä aineistossa kaikki alkuperäiset pilkut tulkitaan pakollisiksi, vaikka
  osa on valinnaisia. Tämä vääristää kattavuutta ylöspäin, joten sitä käytetään vain
  vertailuun menetelmien välillä, ei absoluuttisena lukuna.

**Testit** (`tests/test_arviointi.py`):
- merkintöjen jäsennys: `"Hän sanoi[+,] että"` tuottaa raon oikealle kohdalle ja tekstin
  ilman merkintää
- merkinnät `[-,]` ja `[?-,]` säilyttävät pilkun tekstissä
- mittari leikkiaineistolla: 3 osumaa, 1 väärä hälytys, 1 ohitus antaa tarkkuuden 0,75 ja
  kattavuuden 0,75
- valinnaiseen kohtaan osuva varoitus ei muuta tarkkuutta.

**Valmis kun:** testit menevät läpi ja 20 kappaleen otos on merkitty ja tarkistettu.

#### V2 Lähtötaso

Tuotos: `pylkutus/lahtotaso.py`, luku 2 täytetty, ensimmäinen rivi tiedostoon
`arviointi/tulokset.md`.

- Ajetaan vanha `~/Documents/ratkaisu/pilkut.py` (`/usr/bin/python3`) dokumentille ja
  muunnetaan sen tuloste `Varoitus`-olioiksi (tulosteen rivi ja sarake leipätekstin
  offsetiksi). Kirjataan lukuun 2: mitä sääntöjä se käyttää, millä varmuudella ja mitkä sen
  tyypilliset väärät hälytykset ovat.
- Kirjoitetaan sanalistaan perustuva lähtötaso: sidesana (luku 1.1) tai relatiivisana (1.3)
  ilman edeltävää pilkkua, poikkeuksina 1.14 ja 1.2. Tämä ei tarvitse jäsennintä, joten sitä
  voi käyttää jo ennen vaiheita V4–V5 (tokenointi yksinkertaisella säännöllisellä lausekkeella).
- Testit: lähtötason sääntö luvun 1 esimerkeillä (esim. *Tee se joka päivä* ei varoitusta,
  *Hän sanoi että* varoitus).
- **Valmis kun:** molempien lähtötasojen luvut ovat tiedostossa `arviointi/tulokset.md`.

#### V3 Stanza-koe

Tuotos: `kokeet/stanza_koe.py` korjattuna, `kokeet/tulokset.md`, jäädytetyt esimerkit
kansiossa `tests/fixtures/`.

- Korjataan koeskripti: CPU (`use_gpu=False`), B-jäsennys pretokenisoituna A:n tokeneista,
  pilkut poistetaan tokeneina eikä merkkijonosta (desimaalipilkku säilyy).
- Koevirkkeet, vähintään kaksi kustakin hypoteesista:

| Hypoteesi | Koevirkkeet | Mitä katsotaan |
|---|---|---|
| finiittisyys | *kun hän ei tullut*, *koska hän on lähtenyt*, *vaikka hän on opettaja* | pään `VerbForm`, `aux`/`cop`-lapset |
| lauseenvastike | *Kotiin tultuaan hän söi.*, *Hän pyysi neuvoani uskoen, että voin auttaa.* | `advcl`/`acl`/`xcomp`, ei-finiittisyys |
| *se mitä* | *Se mitä tapahtui, oli outoa.*, *Mitä tapahtui, oli outoa.* | `acl:relcl` vai `csubj` |
| subjektiton lause | *Salilla on hiljaista, mutta …*, *Minun täytyy lähteä ja …*, *Sataa ja …* | `nsubj`-merkinnät |
| täydellinen/vajaa | *Perhe kunnosti saunaa ja viimeisteli keittiön.*, *…, ja heinäkuussa he olivat …* | `conj`, subjektit |
| A/B-ero | nykyiset neljä koevirkettä | eroavat suhteet |
| virkejako | *tri. Virtanen*, *14. päivä*, *Bill W.*, *"Tuletko?" hän kysyi* | virkkeiden määrä |
| toistettavuus | kaikki | kaksi ajoa, identtinen tuloste |

- **Päätöspiste:** jokaisen hypoteesin kohdalla kirjataan *vahvistui* tai *kumoutui*. Jos
  hypoteesi kumoutuu, kohdat 3.5 ja 7.2 korjataan ennen vaihetta V6.
- **Valmis kun:** `kokeet/tulokset.md` sisältää päätöksen jokaisesta hypoteesista ja
  koevirkkeiden `.conllu`-tiedostot on jäädytetty.

#### V4 Esikäsittelijä

Tuotos: `esikasittelija.py`, `lue_md(polku) -> Leipateksti` ja loki karsituista riveistä.

Toteutus:
1. Rivit luokitellaan: otsikko (`#`), otsikon kaltainen (heuristiikka 3.3), luettelon kohta,
   tyhjä, kappale.
2. Kappaleista ja luettelon kohdista poistetaan merkintä: `<span …>`, `</span>`, `**`, `*`,
   `_`, `\`, pehmeä tavuviiva, rivin lopun välilyönnit.
3. Kartta rakennetaan poistojen aikana: jokainen säilyvä merkki muistaa alkuperäisen
   indeksinsä.

Testit (`tests/test_esikasittelija.py`), pienet syötteet merkkijonoina:
- `<span id="anchor-1"></span>Teksti.` tuottaa `Teksti.` ja kartan, jossa T osoittaa oikeaan
  sarakkeeseen
- `**On olemassa ratkaisu**` rivin alussa ilman loppumerkkiä: karsitaan otsikkona
- `e­sittelee` tuottaa `esittelee`
- `# Otsikko` karsitaan, `Kaveri oli tietysti oikeassa.` säilyy
- `1.  Mikä oli ongelma` säilyy omana kappaleenaan ilman luettelonumeroa
- **invariantti** (koko dokumentilla): jokaiselle i pätee
  `alkuperainen[kartta[i]] == teksti[i]`, paitsi kappalerajan rivinvaihdoille
- `rivi_sarake` palauttaa 1-pohjaiset numerot, jotka vastaavat editorin näkymää.

Tilannekuvatesti: koko dokumentin leipäteksti tiedostoon `tests/snapshot/leipateksti.txt` ja
loki tiedostoon `tests/snapshot/karsitut.txt`.

Käsin tehtävä tarkistus: luetaan `karsitut.txt` kokonaan. Siinä saa olla vain otsikoita ja
merkintää.

**Valmis kun:** testit menevät läpi, invariantti pätee koko dokumentilla ja karsittujen
rivien loki on luettu.

#### V5 Jäsennin

Tuotos: `jasennin.py`, `conllu.py`, `jasenna(leipa) -> tuple[list[Virke], list[Virke]]`
(A ja B) ja välimuisti.

Toteutus:
1. Kappale kerrallaan Stanzalle (kappaleraja on aina virkeraja).
2. A: tokenisointi ja jäsennys. Tokenien `start_char`/`end_char` muutetaan leipätekstin
   offseteiksi lisäämällä kappaleen alkukohta.
3. B: A:n tokenit ilman pilkkutokeneita, `tokenize_pretokenized=True`.
4. Tulokset `Virke`-olioiksi: pilkut ja muut rajamerkit siirretään rakoihin (`rako`).
5. Välimuisti: `.cache/<sha256(leipateksti + malliversio)>/A.conllu`, `B.conllu`.
   Malliversio ja `torch`-versio kirjoitetaan tiedoston alkuun kommenttina.

Testit:
- nopeat: `conllu.py` kirjoitus ja luku säilyttävät kaikki kentät (edestakainen muunnos)
- nopeat: pilkkujen siirto rakoihin jäädytetyllä tiedostolla: *Hän sanoi, että* antaa
  `rako[2] == ","` ja tokenit ilman pilkkua
- stanza: virkejako V3:n virkejakovirkkeillä
- stanza: desimaaliluku *3,5 prosenttia* on yksi token, eikä siitä synny rakoa
- stanza: toistettavuus, kaksi ajoa, identtiset `.conllu`-tiedostot
- invariantti (koko dokumentilla): `leipa.teksti[t.alku:t.loppu] == t.teksti` jokaiselle
  tokenille
- invariantti: A:n ja B:n virkkeiden määrä on sama ja tokenit samat.

Tilannekuvatesti: virkejako koko dokumentista, yksi virke riviä kohden
(`tests/snapshot/virkkeet.txt`).

Käsin tehtävä tarkistus: lista virkkeistä, jotka päättyvät lyhenteeseen, numeroon tai
yksittäiseen isoon kirjaimeen (epäilyttävät virkerajat). Virheet korjataan lyhennelistalla
ja esierottelulla.

**Valmis kun:** testit menevät läpi ja epäilyttävien virkerajojen lista on käyty läpi.

#### V6 Lauseistaja

Tuotos: `lauseistaja.py`, `lauseista(virke) -> tuple[list[Lause], list[Raja]]` ja rajojen
yhdistäminen A:sta ja B:stä (`lahde`).

Toteutus osissa, jokainen oma funktionsa ja testinsä:
1. `lauseen_paat(virke)`: suhteet taulukosta 3.5.
2. `janne(virke, paa)`: alipuun ensimmäinen ja viimeinen token, alilauseet mukaan lukien.
   Epäjatkuva (ei-projektiivinen) jänne merkitään, ja siitä ei tehdä rajoja.
3. `finiittinen(virke, paa)`: 3.5:n ehto.
4. `taydellisyys(virke, lause, edellinen)`: 3.5:n päättely.
5. `upotettu`, `virkkeen_alussa`.
6. `rajat(lauseet)`: jänteiden alku- ja loppukohdat raoiksi.
7. `yhdista(rajat_A, rajat_B)`: `lahde` jokaiselle raolle.

Testit jäädytetyillä `.conllu`-tiedostoilla (V3), ilman Stanzaa:
- finiittisyys: kaikki V3:n finiittisyys- ja lauseenvastikevirkkeet
- *Kun tulin kotiin, söin.*: kaksi lausetta, raja raossa ennen *söin*
- *Pelaajat, joiden nimiä ei mainittu, neuvottelevat.*: relatiivilause upotettu, rajat
  molemmin puolin
- *Perhe kunnosti saunaa ja viimeisteli keittiön.*: `conj`, vajaa
- *Kesäkuussa he matkustivat …, ja heinäkuussa he olivat …*: `conj`, täydellinen
- *Tulin kotiin ja söin.*: täydellinen, 1. persoona
- *Salilla on hiljaista, mutta …*: ei vajaa (täydellinen tai ratkaisematon V3:n tuloksen mukaan).

Tilannekuva ja tarkistustyökalu: `pylkuta --dump lauseet tiedosto.md` tulostaa virkkeet
lausesuluin, esim.

```
[Kun tulin kotiin]advcl, [söin]root .
Hän sanoi , [että [jos ehtii]advcl , hän tulee]ccomp .
```

Käsin tehtävä tarkistus: 30 satunnaista virkettä (kiinnitetty siemenluku) kultaisesta
otoksesta. Kirjataan, kuinka monessa lausesulut ovat väärin ja miksi. Tämä luku on
jäsennykseen perustuvien sääntöjen yläraja.

**Valmis kun:** testit menevät läpi ja 30 virkkeen tarkistuksen virheprosentti on kirjattu
tiedostoon `arviointi/tulokset.md`.

#### V7 Sääntötarkistin

Tuotos: `saantotarkistin.py`, `saannot/`, jokainen sääntö oma funktionsa.

Rajapinta:

```python
Saanto = Callable[[Virke, list[Lause], list[Raja]], Iterable[Varoitus]]
SAANNOT: dict[str, Saanto]   # "S1": s1.alkupilkku, ...
```

Säännöt toteutetaan yksi kerrallaan tässä järjestyksessä. Jokaiselle säännölle tehdään sama
kierros:
1. esimerkkitestit luvun 1 taulukosta (`tests/saannot/test_<koodi>.py`): jokainen *oikein*-
   esimerkki ei tuota varoitusta, jokainen *väärin*-esimerkki tuottaa juuri yhden
2. mittaus kultaisella ja synteettisellä aineistolla
3. vertailu lähtötasoon samalla säännöllä
4. tulos tiedostoon `arviointi/tulokset.md`
5. päätös: oletuksena päällä, vain `--tyyli`-lipulla, vai hylätty.

| Järjestys | Säännöt | Perusta | Huomio |
|---|---|---|---|
| 1 | poikkeukset 1.14, S1b, M1, M3 | sanasto | eivät tuota varoituksia vaan estävät niitä, joten testataan yhdessä seuraavan kanssa |
| 2 | S1 (alkupilkku), S3 | sanasto + jäsennys | vertailu suoraan lähtötasoon |
| 3 | K1, K2 | sanasto | 1.4:n rajatapaus matalalla varmuudella |
| 4 | S2 | jäsennys | relatiivisanan tunnistus (*joka* vs. *joka päivä*) |
| 5 | V1, V4, V5, P1–P6 | sanasto | sekä puuttuvat että ylimääräiset |
| 6 | L1, A1, A2 (ylimääräiset) | jäsennys + sanasto | pilkku ilman rajaa (3.6:n taulukon viimeinen rivi) |
| 7 | rajamerkit (1.15) | rako | estää varoituksia |
| 8 | S1e, S2a, K3 | jäsennys | loppupilkut; riippuu jänteen oikeellisuudesta |
| 9 | R4, R3 | jäsennys | *sillä*: pronomini vai konjunktio |
| 10 | R1, R2 | jäsennys | vaikein; täydellisyyden päättely |

Hyväksymisraja oletuksena päällä olevalle säännölle: luvun 4 tavoitteet omassa
varmuusluokassaan ja parempi tarkkuus kuin lähtötasolla samaan virhetyyppiin.

**Valmis kun:** jokaisesta säännöstä on päätös ja mittaustulos.

#### V8 Raportoija ja ajuri

Tuotos: `raportoija.py`, `pylkuta`.

- `raportoi(varoitukset, leipa, polku, suodatus) -> str`.
- Ajuri: `pylkuta tiedosto.md [--min …] [--rule …] [--tyyli] [--dump leipa|virkkeet|lauseet|rajat] [--tarkista]`.

Testit:
- nopea: tunnettu `Varoitus` tuottaa rivin
  `tiedosto.md:12:34: [high/S1] pilkku puuttuu ennen sanaa "että"`
- nopea: suodatus `--min medium` ja `--rule S1`
- stanza, päästä päähän: `tests/fixtures/pieni.md`, jossa on yksi virhe kutakin käytössä
  olevaa sääntöä kohden, sekä span-ankkureita ja lihavointia, jotta sarakkeet siirtyvät.
  Tuloste verrataan tiedostoon `tests/fixtures/pieni.odotettu`
- välimuisti: toinen ajo ei käynnistä Stanzaa (mitataan ajalla tai lokimerkinnällä).

**Valmis kun:** päästä päähän -testi menee läpi ja koko dokumentin raportti on luettu läpi
käsin kerran.

### 7.4 Riippuvuudet ja rinnakkaisuus

```
V0 ─┬─ V1 ── V2 ────────────────────────────┐
    ├─ V3 ──────────┐                       │
    └─ V4 ── V5 ────┴── V6 ── V7 (mittaus) ─┴── V8
```

- V1–V2 ja V3–V5 voidaan tehdä rinnakkain.
- V6 tarvitsee V3:n päätökset ja V5:n virkkeet.
- V7 tarvitsee mittarin (V1) ja lähtötason (V2).
- Kultaisen otoksen merkintä (V1) on käyttäjän työtä ja kulkee muun rinnalla.

### 7.5 Tila (2026-09-26)

| Vaihe | Tila | Tulos |
|---|---|---|
| V0 | valmis | Stanza 1.14.0 + `fi/default` (combined) ladattu, `pytest`, `git init` |
| V1 | valmis (merkintä tarkistamatta) | `arviointi.py` + mittari; kultainen otos 1–20 ja 21–50 Clauden luonnoksena |
| V2 | valmis | vanha `pilkut.py`: 80 % / 27 % testiotoksella; sanalista 100 % / 7 % (luku 2) |
| V3 | valmis | `kokeet/tulokset.md`: hypoteesit vahvistuivat paitsi B neutraalina todistajana; Voikko korjaa Stanzan `Fin`-virheitä |
| V4 | valmis | `esikasittelija.py`; karttainvariantti pätee koko dokumentilla |
| V5 | valmis | `jasennin.py`; virkejaon korjaus (lyhenteet, ison alkukirjaimen katkot: 2780 → 2702 virkettä); 235 s CPU:lla, välimuisti |
| V6 | valmis | `lauseistaja.py`; käsintarkistus 30 virkettä: rajavirheitä 7 % |
| V7 | ensimmäinen versio valmis | testiotos (puhdas mittaus): 89 % / 53 %, korjausten jälkeen 93 % / 93 % (ei puhdas); koko dokumentti 388 varoitusta, arvioitu tarkkuus 75–79 % |
| V8 | valmis | `pylkuta`-ajuri, `raportoija.py`, päästä päähän -testi |

Toteutuksessa lisätyt säännöt ja muutokset suunnitelmaan (yksityiskohdat `arviointi/tulokset.md`):
- **S3-sanastosääntö** (`saannot/sanasto.py`): kysymysverbi + kysymyssana ilman pilkkua.
  Tarvitaan, koska puuttuva pilkku sekoittaa jäsennyksen juuri tässä kohdassa.
- **Ylimääräinen pilkku rajapäätöksestä:** jos rajan sääntö sanoo `ei` (S1b, S4, R2, V1) ja
  pilkku on paikalla, varoitetaan poistosta.
- **Loppurajat (S1e, S2a, K3) aina `low`:** jänne hajoaa helposti puuttuvan pilkun takia.

Seuraavaksi:
1. Käyttäjä tarkistaa kultaiset merkinnät (`arviointi/kulta/otos_01_20.txt`, `otos_21_50.txt`).
2. Uusi puhdas testiotos (kappaleet 51–100) ennen seuraavaa korjauskierrosta.
3. Tunnetut heikkoudet: sarakkeiden nimet tekstissä (*Ketä vahingoitin*), subjektin ja
   predikaatin välinen pilkku (1.13, ei sääntöä), R1:n vajaa/täydellinen-raja, Stanzan
   MWT-virhe (*ongelmaani* → *ongelmaan + i*).
