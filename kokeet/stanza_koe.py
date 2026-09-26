"""Stanza-koe: sama virke pilkuilla (A) ja ilman (B), UD-puu rinnakkain."""
import re
import sys

import stanza

SENTENCES = [
    "Tämä ei tietenkään ole kenenkään vika — mutta se mitä tapahtuu, on että jotkut vanhemmat "
    "toipuneet jäsenet eivät enää tunne samaistuvansa näiden ihmisten kanssa ja ovat aika "
    "väsyneitä kuuntelemaan heidän juttujaan, joten he jäävät kotiin.",
    "Hän vastasi että hänestä tuntuu kuin hän olisi syntynyt uudelleen.",
    "Aviomieheni palasi lopulta mutta ei kestänyt kauaa, kun ymmärsin totuuden.",
    "Tee se joka päivä kahden viikon ajan, ja katso mitä tapahtuu.",
]

nlp = stanza.Pipeline("fi", processors="tokenize,mwt,pos,lemma,depparse",
                      use_gpu=True, verbose=False)


def strip_commas(s):
    return re.sub(r"\s*,", "", s)


def dump(doc):
    rows = []
    for sent in doc.sentences:
        for w in sent.words:
            head = sent.words[w.head - 1].text if w.head > 0 else "ROOT"
            rows.append((w.id, w.text, w.upos, w.deprel, head,
                         (w.feats or "").replace("|", " ")))
    return rows


for s in SENTENCES:
    a = dump(nlp(s))
    b = dump(nlp(strip_commas(s)))
    print("=" * 100)
    print(s)
    print(f"{'A (pilkuilla)':<50}| B (ilman pilkkuja)")
    bi = iter(b)
    for ra in a:
        if ra[1] == ",":
            print(f"{ra[0]:>3} {ra[1]:<14}{ra[3]:<12}{ra[4]:<18}|")
            continue
        rb = next(bi)
        mark = "  " if (ra[3], ra[4]) == (rb[3], rb[4]) else "≠ "
        print(f"{ra[0]:>3} {ra[1]:<14}{ra[3]:<12}{ra[4]:<18}| {mark}{rb[3]:<12}{rb[4]:<18} {ra[2]}")
