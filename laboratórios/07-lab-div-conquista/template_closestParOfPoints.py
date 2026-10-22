import math
import sys

def dist(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def forca_bruta(pontos):
    melhor = math.inf
    for i in range(len(pontos)):
        for j in range(i + 1, len(pontos)):
            melhor = min(melhor, dist(pontos[i], pontos[j]))
    return melhor

def closest_pair_rec(px, py):
    # px: pontos ordenados por x; py: os mesmos pontos ordenados por y.
    # Cada ponto é (x, y, indice); o índice desempata pontos repetidos.
    n = len(px)
    if n <= 3:
        return forca_bruta(px)

    # divisão: a reta vertical que passa por px[meio] separa as metades
    meio = n // 2
    divisor = px[meio]
    esq_x, dir_x = px[:meio], px[meio:]

    # separa py mantendo a ordenação por y, em Θ(n)
    esq_y = [p for p in py if p < divisor]
    dir_y = [p for p in py if p >= divisor]

    # conquista
    d = min(closest_pair_rec(esq_x, esq_y), closest_pair_rec(dir_x, dir_y))

    # combinação: só interessam pontos a menos de d da reta divisória
    faixa = [p for p in py if abs(p[0] - divisor[0]) < d]
    for i in range(len(faixa)):
        # na faixa ordenada por y, cada ponto tem no máximo 7 vizinhos a menos de d
        j = i + 1
        while j < len(faixa) and faixa[j][1] - faixa[i][1] < d:
            d = min(d, dist(faixa[i], faixa[j]))
            j += 1
    return d


def closest_pair(points):
    if len(points) < 2:
        return math.inf
    pontos = [(x, y, i) for i, (x, y) in enumerate(points)]
    px = sorted(pontos)
    py = sorted(pontos, key=lambda p: (p[1], p[0], p[2]))
    return closest_pair_rec(px, py)


'''
--------------------------
    LEITURA DA ENTRADA
--------------------------
'''
def main():
    for linha in sys.stdin:
        N = int(linha.strip())
        if N == 0:
            break

        pontos = []
        for _ in range(N):
            x, y = map(int, sys.stdin.readline().split())
            pontos.append((x, y))

        resposta = closest_pair(pontos)

        if resposta >= 10000:
            print("INFINITY")
        else:
            print(f"{resposta:.4f}")


if __name__ == "__main__":
    main()


'''
Análise do comportamento pela relação de recorrência:

Pré-processamento (closest_pair): ordenar os pontos por x e por y custa
Θ(n log n), feito uma única vez.

Seja T(n) o tempo de closest_pair_rec para n pontos:
  - divisão: fatiar px e separar py em esq_y/dir_y preservando a ordem por y
    custa Θ(n) (por isso mantemos py pré-ordenado em vez de reordenar a cada
    chamada);
  - conquista: duas chamadas com ⌈n/2⌉ e ⌊n/2⌋ pontos;
  - combinação: montar a faixa custa Θ(n) e, como dentro de um retângulo
    d × 2d cabem no máximo 8 pontos com distância mútua ≥ d, cada ponto da
    faixa é comparado com no máximo 7 seguintes, ou seja, Θ(n) no total.

    T(n) = Θ(1),                      n ≤ 3
    T(n) = 2·T(n/2) + Θ(n),           n > 3

Teorema mestre: a = 2, b = 2, f(n) = Θ(n) = Θ(n^(log_2 2)) → caso 2,
logo T(n) = Θ(n log n).

Total: Θ(n log n) + Θ(n log n) = Θ(n log n), contra Θ(n²) da força bruta
(n(n-1)/2 pares). Para N = 10000 isso é ~1.3·10^5 operações contra ~5·10^7.

Observação: se a ordenação por y fosse refeita em cada chamada, a recorrência
seria T(n) = 2·T(n/2) + Θ(n log n) = Θ(n log² n).
'''
