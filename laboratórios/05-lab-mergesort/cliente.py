# (mesmo cliente do Exercício 2 do Laboratório de Métodos Elementares de Ordenação)

import argparse
import sys
import time

import sorts

SORTS = {
    "v1": sorts.merge_sort_v1,
    "v2": sorts.merge_sort_v2,
    "v3": sorts.merge_sort_v3,
    "v4": sorts.merge_sort_v4,
    "v5": sorts.merge_sort_v5,
    "v6": sorts.merge_sort_v6,
    "v7": sorts.merge_sort_v7,
}

# versões que usam o valor de cut-off
COM_CUTOFF = {"v2", "v4", "v6", "v7"}

VERSOES = """versões:
  v1  top-down recursivo, sem otimizações
  v2  top-down + cut-off para insertion sort
  v3  top-down + merge skip
  v4  top-down + cut-off + merge skip
  v5  bottom-up, sem otimizações
  v6  bottom-up + cut-off
  v7  bottom-up + cut-off + merge skip

exemplo: python3 cliente.py 100000 v4 --cutoff 8 < input/unif_rand/100000.txt"""


def main():
    parser = argparse.ArgumentParser(
        description="Lê N inteiros de stdin, ordena e exibe o array ordenado em stdout "
                    "(o tempo de ordenação vai para stderr).",
        epilog=VERSOES,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("N", type=int, help="número de itens a serem lidos de stdin")
    parser.add_argument("versao", choices=SORTS, help="versão do merge sort")
    parser.add_argument("--cutoff", type=int, default=sorts.CUTOFF,
                        help=f"valor de cut-off das versões v2, v4, v6 e v7 (padrão: {sorts.CUTOFF})")
    args = parser.parse_args()
    if args.N < 0:
        parser.error("N deve ser >= 0")
    if args.cutoff < 1:
        parser.error("cutoff deve ser >= 1")
    N = args.N
    sorts.CUTOFF = args.cutoff
    sort = SORTS[args.versao]

    # aloca o array com N posições e lê os N itens de stdin
    a = [0] * N
    for i in range(N):
        linha = sys.stdin.readline()
        a[i] = int(linha)

    # ordena a[0..N-1] medindo o tempo
    start = time.perf_counter()
    sort(a, 0, N - 1)
    end = time.perf_counter()

    sys.stdout.write("\n".join(map(str, a)))
    if N > 0:
        sys.stdout.write("\n")
    cutoff = f", cutoff = {sorts.CUTOFF}" if args.versao in COM_CUTOFF else ""
    print(f"merge sort {args.versao}, N = {N}{cutoff}: {end - start:.6f} s", file=sys.stderr)

    # libera o array
    del a


main()
