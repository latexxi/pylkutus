"""Tallentaa tarkistimen tilannekuvan vertailua varten (PLAN_KORJAUKSET.md, K0).

Käyttö: python arviointi/tilannekuva.py <nimi> [--kylma] [--repo HAKEMISTO]
Tulos: arviointi/tilannekuvat/<nimi>/. Vertailu: diff -r tilannekuvat/baseline tilannekuvat/<nimi>

Kaikki ajetaan aliprosesseina repon omalla tulkilla, jotta työkalu toimii myös vanhalle
commitille (git worktree) ilman, että se tuo pakettia itse.
"""
import argparse
import os
import re
import subprocess
import sys
import tempfile
import time

TAMA = os.path.dirname(os.path.abspath(__file__))
LAHDE = os.path.expanduser("~/Documents/ratkaisu/2026-09-14 ratkaisu.md")
OTOKSET = ["otos_01_20", "otos_21_50"]
TARKISTIMET = ["pylkutus", "sanalista", "vanha"]

KYLMA = """
import sys, time
from pylkutus import ajuri
leipa = ajuri.lue(sys.argv[1])
t = time.time()
ajuri.analysoi(leipa, valimuisti=sys.argv[2])
print(f"{time.time() - t:.1f}")
"""


def aja(repo: str, python: str, args: list[str]) -> tuple[str, float]:
    t = time.time()
    p = subprocess.run([python, *args], cwd=repo, capture_output=True, text=True)
    kesto = time.time() - t
    tulos = p.stdout
    if p.stderr.strip():
        tulos += "\n--- stderr\n" + p.stderr
    if p.returncode:
        tulos += f"\n--- paluuarvo {p.returncode}\n"
    return tulos, kesto


def main():
    p = argparse.ArgumentParser()
    p.add_argument("nimi")
    p.add_argument("--kylma", action="store_true", help="mittaa myös kylmä jäsennys (~4 min)")
    p.add_argument("--repo", default=os.path.dirname(TAMA))
    p.add_argument("--testit", action="store_true", help="aja myös kaikki testit (hidas)")
    a = p.parse_args()
    repo = os.path.abspath(a.repo)
    python = os.path.join(os.path.dirname(TAMA), ".venv", "bin", "python")
    kohde = os.path.join(TAMA, "tilannekuvat", a.nimi)
    os.makedirs(kohde, exist_ok=True)
    kulta = os.path.join(TAMA, "kulta")

    def kirjoita(nimi: str, sisalto: str):
        with open(os.path.join(kohde, nimi), "w", encoding="utf-8") as f:
            f.write(sisalto)

    ajat = []
    teksti, kesto = aja(repo, python, ["-m", "pylkutus", LAHDE, "--tyyli"])
    kirjoita("raportti.txt", teksti)
    ajat.append(f"raportti (lämmin välimuisti): {kesto:.1f} s")
    teksti, _ = aja(repo, python, ["-m", "pylkutus", LAHDE])
    kirjoita("raportti_oletus.txt", teksti)
    for mita in ("lauseet", "rajat"):
        teksti, _ = aja(repo, python, ["-m", "pylkutus", LAHDE, "--dump", mita])
        kirjoita(f"{mita}.txt", teksti)
    for otos in OTOKSET:
        for t in TARKISTIMET:
            teksti, _ = aja(repo, python, ["-m", "pylkutus.arviointi", "-t", t, "-v",
                                           os.path.join(kulta, f"{otos}.txt")])
            kirjoita(f"kulta_{otos}_{t}.txt", teksti)
    merkit = [] if a.testit else ["-m", "not stanza"]
    teksti, kesto = aja(repo, python, ["-m", "pytest", "-q", "-p", "no:cacheprovider", *merkit])
    yhteenveto = teksti.strip().split("\n")[-1]
    kirjoita("testit.txt", re.sub(r" in [\d.]+s", "", yhteenveto) + "\n")
    ajat.append(f"testit ({'kaikki' if a.testit else 'nopeat'}): {kesto:.1f} s")
    if a.kylma:
        with tempfile.TemporaryDirectory() as tmp:
            teksti, _ = aja(repo, python, ["-c", KYLMA, LAHDE, tmp])
        ajat.append(f"kylmä jäsennys: {teksti.strip()} s")
    # ajat vaihtelevat, joten ne eivät kuulu diffiin
    with open(os.path.join(kohde, "ajat.log"), "w", encoding="utf-8") as f:
        f.write("\n".join(ajat) + "\n")
    print("\n".join(ajat))


if __name__ == "__main__":
    main()
