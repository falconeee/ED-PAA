def merge_conta(C, aux, lo, meio, hi):
    # intercala C[lo..meio] e C[meio+1..hi] (já ordenados) e conta as inversões
    # entre as duas metades: quando um elemento da direita sai antes, ele é
    # menor que todos os que ainda restam na esquerda (meio - i + 1 inversões)
    for k in range(lo, hi + 1):
        aux[k] = C[k]

    i, j = lo, meio + 1
    inversoes = 0
    for k in range(lo, hi + 1):
        if i > meio:
            C[k] = aux[j]
            j += 1
        elif j > hi:
            C[k] = aux[i]
            i += 1
        elif aux[j] < aux[i]:
            C[k] = aux[j]
            j += 1
            inversoes += meio - i + 1
        else:
            C[k] = aux[i]
            i += 1
    return inversoes


def conta_inversoes(C, aux, lo, hi):
    # merge sort modificado: ordena C[lo..hi] e devolve o número de inversões
    if lo >= hi:
        return 0
    meio = (lo + hi) // 2
    inversoes = conta_inversoes(C, aux, lo, meio)
    inversoes += conta_inversoes(C, aux, meio + 1, hi)
    inversoes += merge_conta(C, aux, lo, meio, hi)
    return inversoes


def kendall_tau(A, B):
    # pos[x] = posição do elemento x em B
    pos = {x: i for i, x in enumerate(B)}

    # C indica a ordem dos elementos de A segundo a ordem em B
    C = [pos[x] for x in A]

    # a distância de Kendall é o número de inversões de C
    aux = [0] * len(C)
    return conta_inversoes(C, aux, 0, len(C) - 1)


# EXEMPLO DE USO
A = [3, 1, 2, 4]
B = [1, 2, 3, 4]
print("Kendall τ:", kendall_tau(A, B))

'''
Análise do comportamento pela relação de recorrência:

Construir pos e C custa Θ(n).

Sendo T(n) o tempo para n elementos.
A divisão custa Θ(1), resolvendo as duas metades de tamanho ~n/2 e com a combinação
(merge_conta) percorrendo os n elementos uma vez, contando as inversões "cruzadas"
em Θ(1) por elemento:

    T(1) = Θ(1)
    T(n) = 2·T(n/2) + Θ(n)

Teorema mestre: a = 2, b = 2, f(n) = Θ(n) = Θ(n^(log_2 2)) → caso 2,
T(n) = Θ(n log n).

Total: Θ(n) + Θ(n log n) = Θ(n log n) de tempo e Θ(n) de espaço extra
(pos, C e aux).

'''
