# PLAN_TARKISTIN_KORJAUKSET — virheellisten varoitusten korjaus

Lähde: [tarkistin_virheet.md](tarkistin_virheet.md). Putki: 1 esikasittelija → 2 jasennin →
3 lauseistaja → 4 saantotarkistin → 5 raportoija.

## Löydösten sijoitus vaiheisiin

| Löydösryhmä | Todennäköinen syy | Korjauskohta |
|---|---|---|
| 014 (S3, *mistä tahansa vain pystyi*) | `saannot/sanasto.py` `s3_kysymysverbi` tarkistaa vain yhden seuraavan sanan (`JALKISANAT_EI_KYSYMYS`); *tahansa* on kahden sanan päässä | Vaihe 4: ikkuna *mistä* + 1–3 sanaa; tarkista, kuuluuko *etsiä* KYSYMYSVERBIT-listaan |
| Lauseenraja väärästä kohdasta (046, 064, … 386) | vertaus (*niin kuin*), *joten kun*, lainattu otsikko, *jne.*, subjekti–verbi-väli | Vaihe 3 `lauseista`/`_aloittaja`/`_tyyppi`; kaksoiskonjunktiot osin vaihe 4 `alkupilkku` |
| Yhteinen lauseenjäsen, luettelo, upotettu sivulause (004, 032, 081 …) | `_taydellisyys` ei tunnista periytyvää subjektia → R1 `KYLLA` | Vaihe 3 `_taydellisyys`; vaihe 4 `rinnastus()`: ratkaisematon ei saa tuottaa R1 `KYLLA` |
| Pilkku valinnainen (028, 029, 379, 311) | vapaasti viittaava relatiivi (*mitä haluat*) saa S3 `KYLLA`; 311 R1a ei osu | Vaihe 4: `VALINNAINEN`; vaihe 3: `r1a`-tunnistus |
| Älä poista pilkkua (141, 331, 374, 385) | ylimääräisen pilkun havainto tai `EI`-päätös (R2/S4/V1/L1) osuu päälauseiden väliin | Vaihe 4: selvitä laukeava sääntö; todennäköisesti sama juurisyy kuin `_taydellisyys` |
| Otsikkokohdat (205, 256, 271, 274, 288–291), 347 | otsikoita ei tunnisteta; *kuin mitä* -vertailu | Vaihe 1 `_on_otsikon_kaltainen`; vaihe 4 V1-laajennus |

## Toteutusvaiheet

1. **Jäljitys.** Kunkin löydöksen virke ajetaan `pylkuta --dump rajat` -työkalulla; taulukko
   löydös → sääntö → juurisyy. Ei koodimuutoksia.
2. **Regressiotestit ja baseline.** 1–2 testilausetta ryhmää kohti (`tests/`); baseline
   `arviointi/tilannekuva.py`-työkalulla (ks. PLAN_KORJAUKSET.md).
3. **Korjaukset halvimmasta kalleimpaan, kunkin jälkeen vertailu baselineen:**
   a. 014: S3-ikkuna
   b. valinnaiset (028/029/379/311)
   c. `_taydellisyys` / subjektin periytyminen
   d. lauseenrajat (vertaus, kaksoiskonjunktio, lainatut otsikot, *jne.*)
   e. otsikot esikäsittelijässä
4. **Mittaus.** Varoitusmäärät ja osuvuus kultaiseen otokseen (`arviointi/`) ennen/jälkeen;
   aitoja puuttuvia pilkkuja ei saa menettää.
5. **Dokumentointi.** Päivitä PLAN_PILKKU.md 3.5–3.6 ja merkitse löydökset korjatuiksi
   tarkistin_virheet.md:ssä.

## Arvioinnin huomiot (opus-arviointi) ja suunnitelman tarkennukset

- 014: S3 voi tulla myös `lauseistaja._tyyppi` → `alkupilkku` (kysymys) -polusta, jossa
  `JALKISANAT_EI_KYSYMYS`-poikkeusta ei sovelleta. Jäljityksessä varmistetaan polku ja
  korjataan tarvittaessa molemmat.
- "Yhteinen jäsen / luettelo / upotettu" puretaan alaryhmiin jäljityksessä; ei oleteta yhtä
  juurisyytä. `rinnastus()`:ssa ratkaisematon ja täydellinen palauttavat nyt saman R1-päätöksen.
- S2b on dokumentoitu mutta ei toteutettu: uusi sääntö, ei hienosäätö.
- Lauseenrajaryhmästä erotetaan "jäsennysvirhe (Stanza), ei korjattavissa tässä" -luokka.
- Otsikkokorjaus (esikäsittelijä) muuttaa syötettä kaikille: tehdään ensin tai baseline
  otetaan uudelleen sen jälkeen.
- Ennen `ratkaisematon`-muutosta lisätään regressiotesti aidoille R1-tapauksille; mittari:
  recall/precision kultaisella otoksella (`arviointi/`) per muutos.

## Toteutuksen tila

Toteutettu: S2b (vapaasti viittaava lause), eliptisen/vajaan rinnasteisen lauseen käsittely (R1/R2/S4,
`_taydellisyys`), V1 *niin/siten/samoin kuin*, P1 *sekä … että*, S1b *joten*, aloittava lainausmerkki ja
luettelolyhenteet (*jne.* ym.). Regressiotestit lisätty `tests/saannot/test_esimerkit.py`.

Tulos (ratkaisu_2026-10-03.md): varoituksia 388 → 345. Kultaisen otoksen mittarit ennallaan, 152 testiä läpi.

Ei korjattavissa tässä vaiheessa (jäsennysvirheitä tai lauseen sisällä olevia nimiä, ei erillisiä otsikkorivejä):
- yhteinen: 57, 195, 227, 282, 361
- raja: 64, 70, 89, 127, 137, 146, 157, 257, 266, 272, 297, 316, 335, 358, 375, 386
- otsikko: 205, 256, 271, 274, 288–291 (esikäsittelijä ei voi tunnistaa, koska nimet ovat virkkeen sisällä)

Dokumentaatio: PLAN_PILKKU.md päivitetty (1.3 S2b, 1.9 V1b, 3.5 täydellisyys, 3.6 rajasäännöt). Parirakenne *sekä … että* käyttää koodia P4 (ei P1, joka on *mitä–sitä*).
