# Tarkistimen virheelliset tulokset

Tähän dokumenttiin kerätään tarkistimen varoituksia, joita pidämme virheellisinä tai harhaanjohtavasti luokiteltuina.

## Varoitus 014 — väärä S3-hälytys

- **Lähde:** [ratkaisu_2026-10-03.md](ratkaisu_2026-10-03.md#L102), sarake 371
- **Tarkistimen tulos:** `[medium/S3] pilkku puuttuu ennen sanaa "mistä"`
- **Katkelma:** `… puhu heille katuojissa, etsien alkoholisteja mistä tahansa vain pystyi, mutta kukaan …`
- **Miksi virheellinen:** *Mistä tahansa vain pystyi* tarkoittaa tässä suunnilleen *kaikkialta, mistä hän vain pystyi etsimään*. Se ei ole epäsuora kysymys, joten S3 ei sovellu. Tarkistin näyttää tulkitsevan *mistä*-rakenteen kysymykseksi, vaikka *tahansa* tekee ilmauksesta vapaavalintaisen paikanilmauksen.
- **Pilkun tarve:** Pilkun puuttumista ei voi perustella S3:lla. Lähin suunnitelman sääntö on S2b, jonka mukaan korrelaatiottoman relatiivilauseen pilkku on valinnainen (*Teen(,) mitä haluan*). Tässä pilkuton muoto on luonteva.

## Muut löydökset raportista

Alla olevat numerot viittaavat [selkeään raporttiin](raportti_ratkaisu_2026-10-03_selkea.md).

### Virheellinen pilkunlisäyshälytys

- **Yhteinen lauseenjäsen, luettelo tai upotettu sivulause:** 004, 032, 057, 081, 082, 167, 195, 213, 227, 245, 248, 282, 356, 361. Pilkku ei erottaisi kahta rinnasteista kokonaista päälausetta; esimerkiksi 081:ssä sama subjekti jatkaa tekemistä (*hän ei pysty lopettamaan ja jatkaa*).
- **Lauseenraja tunnistettu väärästä kohdasta:** 046, 064, 066, 070, 089, 104, 118, 125, 127, 137, 146, 157, 173, 204, 257, 262, 266, 272, 297, 316, 335, 358, 375, 382, 386. Varoitus osuu esimerkiksi vertaukseen (*niin kuin Kolumbus*, 118), kaksoiskonjunktioon (*joten kun*, 204), lainattuun otsikkoon (125), otsikon ja verbin väliin, luettelolyhenteeseen *jne.* tai subjektin ja verbin väliin (137, 157, 316, 335, 358).

### Pilkku on valinnainen

- **028, 029 ja 379:** *mitä haluat* / *mitä haluaa* on tässä vapaasti viittaava relatiivilause, ei pilkkua vaativa epäsuora kysymys. Suunnitelman S2b sallii pilkun.
- **311:** kysymyslauseiden rinnastuksessa pilkku on R1a:n mukaan valinnainen.

### Älä poista pilkkua

- **141, 331, 374 ja 385:** raportti luokittelee pilkun ylimääräiseksi, vaikka se erottaa itsenäiset päälauseet. Pilkku kuuluu säilyttää.

### Epäselvät otsikkokohdat

Varoitukset 205, 256, 271, 274 ja 288–291 osuvat sarakeotsikoihin, jotka on jätetty lainausmerkeittä tai kaksoispisteittä. Tarkistimen pilkkuehdotus ei välttämättä ole oikea korjaus; otsikot kannattaa merkitä selvästi. Varoituksessa 347 rakenne vaikuttaa vertailulta (*paremmalla kuin mitä alkoholi koskaan oli*), joten tarkistimen pilkkuehdotus on epävarma ja lause kaipaa ensisijaisesti sanamuodon tarkistusta.

---
Tila: korjattu valinnaiset (014, 028, 029, 379, 311), ala_poista (141, 331, 374, 385), yhteinen 9/14, raja 9/25, otsikko 1/9.
Loput: ks. PLAN_TARKISTIN_KORJAUKSET.md, "Toteutuksen tila".
