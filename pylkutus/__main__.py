import argparse
import sys

from . import ajuri, raportoija, saannot, saantotarkistin


def main(argv=None):
    p = argparse.ArgumentParser(prog="pylkuta", description="Suomen kielen pilkkutarkistin.")
    p.add_argument("tiedosto", nargs="?", help="md- tai tekstitiedosto (tekstissä kappaleet tyhjin rivein)")
    p.add_argument("--min", choices=["high", "medium", "low"], default="low",
                   help="vähimmäisvarmuus (oletus low)")
    p.add_argument("--rule", action="append", help="näytä vain tämä sääntö (voi toistaa)")
    p.add_argument("--tyyli", action="store_true", help="näytä myös valinnaiset pilkut")
    p.add_argument("--dump", choices=["virkkeet", "lauseet", "rajat"],
                   help="tulosta välitulos varoitusten sijaan")
    p.add_argument("--saannot", action="store_true", help="listaa säännöt ja lopeta")
    a = p.parse_args(argv)
    if a.saannot:
        print(saannot.listaus())
        return 0
    if not a.tiedosto:
        p.error("tiedosto puuttuu")
    leipa = ajuri.lue(a.tiedosto)
    analyysit = ajuri.analysoi(leipa)
    if a.dump:
        print(ajuri.dump(analyysit, a.dump))
        return 0
    varoitukset = saantotarkistin.tarkista(leipa, analyysit, tyyli=a.tyyli)
    varoitukset = raportoija.suodata(varoitukset, a.min, set(a.rule) if a.rule else None)
    if varoitukset:
        print(raportoija.raportoi(varoitukset, leipa, a.tiedosto))
    print(raportoija.yhteenveto(varoitukset), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
