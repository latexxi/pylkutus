# Poikkeustapaukset pilkutuksessa

## Tarkoitus

Tämä dokumentti kuvaa, miksi pilkkutarkistimen varoituksia ei voi kaikissa teksteissä tulkita tavallisten virkepilkkusääntöjen mukaan, mitä poikkeuksia ohjelma käsittelee erikseen ja mitä on vielä ratkaisematta.

## Miksi poikkeukset ovat hankalia

Säännöt olettavat usein, että tarkasteltava kohta on kokonainen päälause tai sivulause. Markdown-dokumentissa vastaan tulee myös otsikoita, taulukon soluja, luetteloiden otsakkeita, lyhyitä ohjeita, lainattuja nimikkeitä ja virkkeen osia. Niissä sama sanajono voi olla esimerkiksi:

- kokonainen lause, johon pilkkusääntö soveltuu
- lauseenjäsen tai luettelon osa, jonka sisällä pilkkua ei tarvita
- otsake tai nimike, jonka rajaus kuuluu ilmaista esimerkiksi lainausmerkeillä tai kaksoispisteellä
- elliptinen tai muuten vajaa rakenne, jossa tavallisen virkkeen syntaksia ei voi soveltaa suoraan

Jäsennin voi antaa tällaiselle tekstille näennäisen lauserakenteen. Säännön paikallinen tunnistus voi sen jälkeen tuottaa itsevarmankin varoituksen, vaikka rakenne onkin otsake tai lauseenosa.

## Nykyinen käsittely

Markdown-esikäsittelijä ([esikasittelija.py](pylkutus/esikasittelija.py)) poistaa eksplisiittiset `#`-otsikot tekstistä ja tunnistaa osan otsikonkaltaisista riveistä heuristiikalla. Luettelomerkit poistetaan ja luettelokohdat erotetaan omiksi lohkoikseen, mutta niiden sisältö jatkaa tavalliseen tapaan analyysiin. GFM-tyylinen taulukko tunnistetaan otsakerivin ja erotinrivin perusteella: otsake ja erotin jätetään analyysistä pois, ja jokainen sisältösolu analysoidaan erillisenä jaksona. Näin sarakkeiden välinen teksti ei muodosta keinotekoista virkettä. Lähdekohdistus säilyy solujen sisällä.

Esimerkiksi seuraavassa taulukossa sarakeotsakkeita ei analysoida, ja kaksi sisältösolua tarkistetaan toisistaan riippumatta:

```markdown
| Kysymys | Vastaus |
| --- | --- |
| Mitä tapahtui? | Hän sanoi että lähtee. |
```

Taulukoksi tunnistaminen vaatii otsake- ja erotinrivillä pystyviivan (`|`) sekä yhtä monta erotinsolua kuin otsakesolua. Erotinsoluissa on vähintään kolme yhdysmerkkiä, joiden alussa tai lopussa voi olla kaksoispiste. Sisältörivejä käsitellään taulukon soluina niin kauan kuin ne ovat ei-tyhjiä ja sisältävät pystyviivan; kenoviivalla suojatut pystyviivat eivät jaa solua.

Esikäsittelyn tulos ([tyypit.py](pylkutus/tyypit.py)) sisältää tekstin, lähdekohdistuksen ja kappalerajat, mutta ei yleistä luokitusta tekstijaksojen poikkeustyypeistä. Taulukon käsittely tehdään esikäsittelyssä rakenteellisena erikoistapauksena. Sääntötarkistin ([saantotarkistin.py](pylkutus/saantotarkistin.py)) ratkaisee muut pilkun lisäykset ja poistot tunnistettujen lauserajojen ja sääntöpäätösten perusteella; se ei edelleenkään luokittele yleisesti lainauksia, nimikkeitä tai virkkeenosia.

Koodi tunnistaa kuitenkin joitakin rajattuja poikkeuksia:

- lauseen täydellisyys (`täydellinen`, `vajaa`, `ratkaisematon`) vaikuttaa rinnasteisten päälauseiden R1/R2-ratkaisuun
- R1a, S2b, S1b ja moniosaisia konjunktioita koskevat säännöt käsittelevät tiettyjä valinnaisia tai kiellettyjä pilkkuja
- merkit, kuten ajatusviiva ja kaksoispiste, voivat joissakin rajapäätöksissä estää lisäpilkkuhälytyksen

Nämä ovat sääntökohtaisia poikkeuksia, eivät yleinen kyky tunnistaa, ettei kohta ole tavallinen virke. Pieni varmuusluokka ei itsessään tarkoita, että ohjelma tunnisti poikkeustapauksen; se kuvaa päätöksen epävarmuutta. Esimerkiksi `puuttuvat.py`-tiedoston kommentti toteaa S1e-loppurajojen olevan helposti rikkoutuvia ja lähes kaikkien kyseisen dokumentin S1e-varoitusten olleen vääriä, mutta matalan varmuuden varoitukset voidaan silti näyttää oletusasetuksilla.

## Havaitut seuraukset

Raportin [388 varoituksen tarkistuksessa](raportti_ratkaisu_2026-10-03_selkea.md) kirjattiin 48 varoitusta virheellisiksi tai harhaanjohtaviksi. Yleisiä tapauksia olivat:

- **Otsakkeet ja nimikkeet:** sarakkeiden nimet kuten *Mitä tein?* ja *Loukkasin tai uhkasin* tulkittiin kysymys- tai lauserakenteiksi. Esimerkkejä: varoitukset 205, 256, 271, 274 ja 288–291. Näissä oikea rajaus voi vaatia otsakkeen merkitsemistä, ei tarkistimen ehdottamaa pilkkua.
- **Lauseenosa tulkittiin lauseeksi:** varoitus 064 ehdotti pilkkua rakenteeseen *meidät valtasi kiihkeä ja jännittävä tunne*; 137 ja 157 kohdistuivat lauseen subjektin ja verbin väliin; 316 osui objektin ja infinitiivin rajaan.
- **Luettelot ja parirakenteet:** varoitus 262 ehdotti pilkkua rakenteeseen *sekä harjoitella että muistaa*. Varoitukset 070 ja 173 osuivat luettelomaiseen jatkoon tai lyhenteeseen *jne.*
- **Lainaukset ja nimikkeet:** varoitus 125 käsitteli kirjan luvun nimeä lauserajana; varoitukset 066 ja 361 osuivat lainattujen vaihtoehtojen sisälle.
- **Sääntöjen yhteensovitus:** varoitus 204 vaati pilkkua peräkkäisten sanojen *joten kun* väliin, vaikka kyse on kaksoiskonjunktion rakenteesta. Varoitus 057 ei huomioinut rinnasteisten sivulauseiden tapausta.
- **Väärä poistoehdotus:** varoitukset 141, 331, 374 ja 385 luokittelivat itsenäisiä päälauseita erottavan pilkun ylimääräiseksi.

Osa muista raportin kohdista jäi aidosti tulkinnanvaraiseksi. Esimerkiksi korrelaatiottoman relatiivilauseen pilkku voi olla valinnainen, ja vertailurakenne voi vaatia sanamuodon tarkistusta pilkun sijaan. Tarkemmat varoitusnumerot ja perustelut on kirjattu tiedostoon [tarkistin_virheet.md](tarkistin_virheet.md).

## Rajaus

Taulukon tunnistus edellyttää Markdown-taulukolle ominaista otsake- ja erotinriviparia. Toteutus ei yritä tunnistaa taulukoita, joista erotinrivi puuttuu, eikä tulkitse yksittäisiä virkkeen sisäisiä nimikkeitä tai lainauksia poikkeuksiksi. Kunkin solun Markdown-muotoilu siivotaan samoilla säännöillä kuin muukin teksti. Luokittelun laajentaminen näihin muihin tapauksiin vaatii erilliset, regressiotesteihin perustuvat päätökset.
