# Roda o cliente para cada versão/entrada e imprime as tabelas de tempo em markdown.
# Cada tempo é a mediana de --reps execuções do cliente (só o tempo de ordenação).
#
#   python3 experimentos.py versoes                 # 7 versões x 4 entradas x 2 tamanhos
#   python3 experimentos.py cutoff v2 unif_rand     # varre o cut-off da versão v2

import argparse
import statistics
import subprocess
import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
TIPOS = ["unif_rand", "sorted", "reverse_sorted", "nearly_sorted"]
TAMANHOS = [100000, 1000000]
VERSOES = ["v1", "v2", "v3", "v4", "v5", "v6", "v7"]
CUTOFFS = [1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 14, 16, 20, 24, 32, 48, 64]


def medir(versao, tipo, n, cutoff, reps):
    cmd = [sys.executable, str(DIR / "cliente.py"), str(n), versao]
    if cutoff is not None:
        cmd += ["--cutoff", str(cutoff)]
    tempos = []
    for _ in range(reps):
        with open(DIR / "input" / tipo / f"{n}.txt") as entrada:
            r = subprocess.run(cmd, stdin=entrada, stdout=subprocess.DEVNULL,
                               stderr=subprocess.PIPE, text=True, check=True)
        # última linha do stderr: "merge sort v1, N = 100000: 0.131566 s"
        tempos.append(float(r.stderr.strip().rsplit(":", 1)[1].split()[0]))
    return statistics.median(tempos)


def fmt(t):
    return f"{t * 1000:.1f} ms" if t < 1 else f"{t:.2f} s"


def tabela_versoes(args):
    for tipo in TIPOS:
        print(f"\n### `{tipo}`\n")
        print("| Versão | " + " | ".join(f"{n // 1000}K" if n < 10**6 else f"{n // 10**6}M"
                                       for n in TAMANHOS) + " |")
        print("|---|" + "---:|" * len(TAMANHOS))
        for v in VERSOES:
            tempos = [medir(v, tipo, n, args.cutoff, args.reps) for n in TAMANHOS]
            print(f"| {v} | " + " | ".join(fmt(t) for t in tempos) + " |", flush=True)


def tabela_cutoff(args):
    print(f"\n### `{args.versao}` em `{args.tipo}`\n")
    print("| cut-off | " + " | ".join(f"N = {n}" for n in TAMANHOS) + " |")
    print("|---:|" + "---:|" * len(TAMANHOS))
    for c in CUTOFFS:
        tempos = [medir(args.versao, args.tipo, n, c, args.reps) for n in TAMANHOS]
        print(f"| {c} | " + " | ".join(fmt(t) for t in tempos) + " |", flush=True)


def main():
    parser = argparse.ArgumentParser(description="Mede o tempo das variantes do merge sort.")
    parser.add_argument("--reps", type=int, default=5, help="execuções por medida (padrão: 5)")
    sub = parser.add_subparsers(dest="experimento", required=True)
    p = sub.add_parser("versoes", help="tempo das 7 versões em todas as entradas")
    p.add_argument("--cutoff", type=int, default=None, help="cut-off das versões v2, v4, v6 e v7")
    p.set_defaults(func=tabela_versoes)
    p = sub.add_parser("cutoff", help="tempo de uma versão variando o cut-off")
    p.add_argument("versao", choices=VERSOES)
    p.add_argument("tipo", choices=TIPOS)
    p.set_defaults(func=tabela_cutoff)
    args = parser.parse_args()
    args.func(args)


main()
