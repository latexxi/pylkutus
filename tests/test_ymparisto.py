import pytest


def test_voikko():
    import libvoikko
    v = libvoikko.Voikko("fi")
    assert v.analyze("talo")
    assert v.spell("talo")
    assert not v.spell("taloxq")


@pytest.mark.stanza
def test_stanza_cpu():
    import stanza
    nlp = stanza.Pipeline("fi", processors="tokenize,mwt,pos,lemma,depparse",
                          use_gpu=False, verbose=False, download_method=None)
    doc = nlp("Hän tuli kotiin.")
    sanat = [w.text for w in doc.sentences[0].words]
    assert sanat == ["Hän", "tuli", "kotiin", "."]
    assert [w.deprel for w in doc.sentences[0].words].count("root") == 1


def test_versiot(capsys):
    import stanza, torch
    print(f"stanza {stanza.__version__}, torch {torch.__version__}")
    assert stanza.__version__ == "1.14.0"
