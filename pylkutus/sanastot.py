"""Sanalistat (PLAN_PILKKU.md luku 1)."""

# Lyhenteet, joiden perässä oleva piste ei päätä virkettä (pienaakkosin, ilman pistettä).
LYHENTEET = {
    "tri", "esim", "jne", "ns", "mm", "vrt", "klo", "s", "ss", "n", "ym", "yms", "ks",
    "prof", "rva", "hra", "nti", "jms", "ekr", "jkr", "milj", "mrd", "v", "vv", "ts",
    "yl", "ao", "em", "kpl", "tms", "puh", "os", "lk", "nro", "vol", "ed",
}

# Alistuskonjunktiot (1.1)
ALISTUS = {"että", "jotta", "koska", "kun", "kunnes", "jos", "vaikka", "jollei", "ellei",
           "kunhan", "mikäli"}

# Moniosaiset konjunktioilmaukset (1.2): pilkku joko koko ilmauksen eteen tai ennen viimeistä osaa.
MONIOSAISET = [
    ("sitten", "kun"), ("samalla", "kun"), ("aina", "kun"), ("heti", "kun"),
    ("sen", "aikaa", "kun"), ("silloin", "kun"), ("niin", "että"), ("siten", "että"),
    ("sen", "lisäksi", "että"), ("ilman", "että"), ("sen", "jälkeen", "kun"),
    ("sen", "sijaan", "että"), ("siitä", "huolimatta", "että"), ("sitä", "mukaa", "kuin"),
    ("siihen", "mennessä", "kun"), ("sen", "vuoksi", "että"), ("siksi", "että"),
    ("vasta", "kun"), ("varsinkin", "kun"), ("etenkin", "kun"), ("varsinkin", "jos"),
    ("etenkin", "jos"), ("paitsi", "jos"), ("paitsi", "että"), ("juuri", "kun"),
    ("sen", "takia", "että"),
]

# Rinnastuskonjunktiot (1.7) ryhmittäin
RINNASTUS_JA = {"ja", "tai", "sekä", "eli", "vai", "eikä"}
RINNASTUS_MUTTA = {"mutta", "vaan"}
RINNASTUS_SILLA = {"sillä"}

# Välimerkit, jotka täyttävät lauserajan pilkun sijasta (1.15). Lainausmerkit ja loppusulku
# eivät korvaa pilkkua: "ylläpitoaskeleiksi" ja he …, (liitteenä) on …
RAJAMERKIT_EDELLA = {"—", "–", "-", ":", ";", "("}
RAJAMERKIT_JALJESSA = {"—", "–", "-", ":", ";", "("}

# Lauseen alun asenne- ja järjestyssanat (A1, A2): ei tavallisesti pilkkua perään
A1_A2 = {"valitettavasti", "toisaalta", "onneksi", "ilmeisesti", "tietysti", "kuitenkin",
         "ensiksi", "toiseksi", "kolmanneksi", "neljänneksi", "viimeiseksi", "lopuksi",
         "ensinnäkin", "siksi", "silti", "todellakin"}

# Verbit, joiden objektina on usein epäsuora kysymys (S3-sanastosääntö). Perusmuodot.
KYSYMYSVERBIT = {
    "tietää", "kysyä", "huomata", "huomioida", "nähdä", "katsoa", "ymmärtää", "miettiä",
    "selittää", "kertoa", "näyttää", "tajuta", "muistaa", "arvata", "pohtia", "päättää",
    "selvittää", "tutkia", "ihmetellä", "epäillä", "oppia", "osoittaa", "sanoa", "kuvata",
    "kuvailla", "tarkistaa", "arvioida", "harkita", "keskustella", "tarkastella", "havaita",
    "ymmärtämään", "punnita", "näkemään", "kuulla", "aavistaa", "unohtaa", "tuntea",
}
