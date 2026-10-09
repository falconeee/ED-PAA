import subprocess
import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
TIPOS = ["unif_rand", "sorted", "reverse_sorted", "nearly_sorted"]
TAMANHOS = [100000, 1000000]
VERSOES = ["v1", "v2", "v3", "v4", "v5", "v6", "v7"]
COM_CUTOFF = ["v2", "v4", "v6", "v7"]  # versões que usam o valor de cut-off
CUTOFFS = [1, 4, 8, 16, 32, 64]  # Valores de cut-off a testar


def medir(versao, tipo, n, cutoff=None):
    cmd = [sys.executable, str(DIR / "cliente.py"), str(n), versao]
    if cutoff is not None:
        cmd += ["--cutoff", str(cutoff)]
    with open(DIR / "input" / tipo / f"{n}.txt") as entrada:
        r = subprocess.run(cmd, stdin=entrada, stdout=subprocess.DEVNULL,
                           stderr=subprocess.PIPE, text=True, check=True)
    # última linha do stderr: "merge sort v1, N = 100000: 0.131566 s"
    return float(r.stderr.strip().rsplit(":", 1)[1].split()[0])


def fmt(t):
    return f"{t * 1000:.1f} ms" if t < 1 else f"{t:.2f} s"


def exp_versoes():
    for tipo in TIPOS:
        for v in VERSOES:
            for n in TAMANHOS:
                t = medir(v, tipo, n)
                print(f"{v} {tipo} N = {n}: {fmt(t)}", flush=True)


def exp_cutoff():
    for tipo in TIPOS:
        for v in COM_CUTOFF:
            for c in CUTOFFS:
                for n in TAMANHOS:
                    t = medir(v, tipo, n, c)
                    print(f"{v} {tipo} cutoff = {c} N = {n}: {fmt(t)}", flush=True)


exp_versoes()
exp_cutoff()
