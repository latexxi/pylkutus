"""Jäsentää koko dokumentin välimuistiin ja tarkistaa invariantit."""
import sys, time
from pylkutus.esikasittelija import lue_md
from pylkutus import jasennin

polku = sys.argv[1]
with open(polku, encoding="utf-8") as f:
    leipa, _ = lue_md(f.read())
t = time.time()
a, b = jasennin.jasenna(leipa)
print(f"aika {time.time() - t:.0f} s, virkkeitä {len(a)}")
virheet = jasennin.tarkista(leipa, a, b)
print(f"invarianttivirheitä {len(virheet)}")
for v in virheet[:20]:
    print(" ", v)
