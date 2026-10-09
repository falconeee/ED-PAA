# Exercício 2 - Cliente dos algoritmos de ordenação

import argparse
import sys
import time

from sorts import insertion_sort, selection_sort, bubble_sort, shaker_sort

SORTS = {
    "selection": selection_sort,
    "insertion": insertion_sort,
    "bubble": bubble_sort,
    "shaker": shaker_sort,
}


def main():
    parser = argparse.ArgumentParser(
        description="Lê N inteiros de stdin, ordena e exibe o array ordenado em stdout "
                    "(o tempo de ordenação vai para stderr).",
        epilog="exemplo: python3 cliente.py 1000 insertion < input/in/unif_rand/1Kunif_rand.txt")
    parser.add_argument("N", type=int, help="número de itens a serem lidos de stdin")
    parser.add_argument("algoritmo", choices=SORTS, help="algoritmo de ordenação")
    args = parser.parse_args()
    if args.N < 0:
        parser.error("N deve ser >= 0")
    N = args.N
    sort = SORTS[args.algoritmo]

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
    print(f"{args.algoritmo} sort, N = {N}: {end - start:.6f} s", file=sys.stderr)

    # libera o array
    del a


main()
