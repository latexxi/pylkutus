# V3 Stanza-koe: tulokset (2026-09-26)

Ajo: `python kokeet/v3_hypoteesit.py > kokeet/v3_tuloste.txt`. Stanza 1.14.0, torch 2.14.0,
malli `fi/default` (= combined: TDT + FTB), CPU. Jäädytetty: `tests/fixtures/v3_A.conllu`,
`tests/fixtures/v3_B.conllu`.

| Hypoteesi | Päätös | Havainto |
|---|---|---|
| Finiittisyys vaatii `aux`/`cop`-lapsen tarkistuksen | **vahvistui** | *kun hän ei tullut*, *koska hän on lähtenyt*: pää `tullut`/`lähtenyt` on `Part`, `aux` on `Fin`. *vaikka hän on opettaja*: pää NOUN, `cop` `Fin`. |
| Lauseenvastike = ei-finiittinen `advcl`/`acl`/`xcomp` | **vahvistui, yksi poikkeus** | *tultuaan*, *asetuttuaan* (`Part`), *uskoen* (`Inf`) oikein. **Virhe:** *auttaaksemme* merkitty `root`, `VerbForm=Fin`. Voikko antaa sille vain A-infinitiivin, joten `Fin` tarkistetaan Voikolla (ks. alla). |
| *se mitä* = `acl:relcl` *se*-sanaan | **vahvistui** | *Se mitä tapahtui, oli outoa.* ja *…, mutta se mitä tapahtuu, on …*: `acl:relcl` → *se*. |
| Korrelaatiton *Mitä tapahtui* = `csubj` | **vahvistui** | Suhde on alatyyppi `csubj:cop`. Lausesuhteiksi hyväksytään kaikki `csubj*`-alatyypit. |
| Subjektittomien lauseiden merkintä | **selvitetty** | Nesessiivi: *Minun* = `nsubj` (genetiivisubjekti merkitään). Eksistentiaali *Salilla on hiljaista*: ei `nsubj`:ia, pää *Salilla*. Passiivi: `Voice=Pass`, ei `nsubj`:ia. *Sataa*: morfologia väärin (`Person=2`). |
| Täydellinen/vajaa `conj`-lause | **vahvistui** | 5/5 oikein 3.5:n päättelyllä: *Perhe kunnosti … ja viimeisteli* vajaa; *… ja heinäkuussa he olivat* täydellinen (`nsubj:cop`); *Tulin kotiin ja söin* 1. persoona; *… ja se näytti* täydellinen; *palasi … mutta ei kestänyt* vajaa. |
| Loppupilkun paikka jänteestä | **vahvistui (A)** | *Kun tulin kotiin, söin*, *että jos ehtii, hän tulee*, *Pelaajat, joiden … mainittu, neuvottelevat*: A:n jänteet oikein. |
| Epäsuora kysymys | **vahvistui** | *oliko*, *mistä*, *missä*: `ccomp`. *-ko*-sana voi olla `cop`-lapsi (*oliko se normaalia*: pää *normaalia*). |
| B neutraalina todistajana | **kumoutui** | B jäsentää upotetut sivulauseet väärin ilman pilkkuja: *että jos ehtii hän tulee*, *Pelaajat joiden nimiä ei mainittu neuvottelevat*, *Mitä tapahtui oli outoa* – kaikissa B:n puu on rikki. Tukee päätöstä käyttää puuttuvien pilkkujen etsintään vain A:ta. |
| *joka* = jokainen | **oikein** | *Tee se joka päivä*: *joka* = `det`. |
| *kuin*-vertailu | **huomio** | *tuntuu kuin hän olisi syntynyt*: `advcl` + `mark kuin`. V1 on käsiteltävä ennen S1:tä, muuten syntyy väärä varoitus. |
| Toistettavuus | **vahvistui** | `test_toistettavuus`: kaksi ajoa, identtiset CoNLL-U-tiedostot. |

## Muutokset suunnitelmaan

1. **Finiittisyys:** token on finiittinen, jos Stanza merkitsee `VerbForm=Fin` *ja* Voikolla
   on sanalle finiittinen analyysi (indikatiivi, konditionaali, imperatiivi, potentiaali tai
   kieltosana) tai Voikko ei tunne sanaa lainkaan.
2. **Lausesuhteet:** `csubj*`, `ccomp`, `advcl`, `acl:relcl`, `conj`, `parataxis`, `root`;
   myös `acl`, `xcomp`, jos finiittinen.
3. Lauseen pää voi olla myös AUX (*on* `conj`-suhteessa), joten pään sanaluokkaa ei rajata.
4. Synteettiseen aineistoon ei voi käyttää FTB:tä eikä TDT:tä: oletusmalli on opetettu
   molemmilla (`combined`).

## Koko dokumentti

`kokeet/jasenna_koko.py`: 231 s (CPU, 24 min prosessoriaikaa), 2780 virkettä,
invarianttivirheitä 0.
