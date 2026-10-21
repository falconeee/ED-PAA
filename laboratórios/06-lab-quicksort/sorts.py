import random

from item import less, exch, compexch

# Cut-off usado pelas Versões 2, 4, 6 e 7: sub-arrays com até CUTOFF itens são
# ordenados com insertion sort. CUTOFF = 1 desliga a otimização. Pode ser
# alterado aqui ou pela opção --cutoff do cliente.
CUTOFF = 8


# Insertion sort do Laboratório de Métodos Elementares (Exercício 4)
def insertion_sort(a, lo, hi):
    for i in range(hi, lo, -1):
        a[i - 1], a[i] = compexch(a[i - 1], a[i])
    for i in range(lo + 2, hi + 1):
        v = a[i]
        j = i
        while less(v, a[j - 1]):
            a[j] = a[j - 1]
            j -= 1
        a[j] = v


# Particionamento com pivô a[lo] (slide 10). O código do slide não avança i e j
# depois da troca e entra em loop infinito quando a[i] == a[j] == v; aqui os
# índices avançam antes de cada scan, como no Sedgewick. Os dois scans param em
# chaves iguais ao pivô (slide 31).
def partition(a, lo, hi):
    i, j = lo, hi + 1
    v = a[lo]
    while True:
        i += 1
        while less(a[i], v):  # Find on left to swap
            if i == hi:
                break
            i += 1
        j -= 1
        while less(v, a[j]):  # Find on right to swap
            if j == lo:
                break
            j -= 1
        if i >= j:  # Check if pointers cross
            break
        a[i], a[j] = exch(a[i], a[j])
    a[lo], a[j] = exch(a[lo], a[j])
    return j


# Mediana de a[lo], a[mid] e a[hi]. Sem embaralhamento, a amostra é fixa
# (extremos e meio) em vez de 3 chaves aleatórias. As 3 chaves são ordenadas no
# lugar (a[lo] <= a[mid] <= a[hi]) e o índice da mediana (mid) é devolvido.
# Só devolver o índice, sem mexer nas chaves, deixa o quick sort quadrático na
# entrada reversa: depois do 1º particionamento o sub-array vira
# [max, 1, 2, ..., max-1] e a amostra sempre escolhe o 2º maior como pivô.
def median_of_3(a, lo, hi):
    mid = lo + (hi - lo) // 2
    a[lo], a[mid] = compexch(a[lo], a[mid])
    a[mid], a[hi] = compexch(a[mid], a[hi])
    a[lo], a[mid] = compexch(a[lo], a[mid])
    return mid


# Embaralhamento de Fisher-Yates (slide 11)
def shuffle(a, lo, hi):
    for i in range(hi, lo - 1, -1):
        j = random.randint(lo, i)
        a[i], a[j] = exch(a[j], a[i])


# Versão 1 - quick sort top-down recursivo sem otimizações (slides 10 e 11,
# sem o shuffle)
def quick_sort_v1(a, lo, hi):
    if hi <= lo:
        return
    j = partition(a, lo, hi)
    quick_sort_v1(a, lo, j - 1)
    quick_sort_v1(a, j + 1, hi)


# Versão 2 - top-down com cut-off para insertion sort (slide 23)
def quick_sort_v2(a, lo, hi):
    if hi <= lo + CUTOFF - 1:
        insertion_sort(a, lo, hi)
        return
    j = partition(a, lo, hi)
    quick_sort_v2(a, lo, j - 1)
    quick_sort_v2(a, j + 1, hi)


# Versão 3 - top-down com mediana de 3, sem cut-off (slide 24)
def quick_sort_v3(a, lo, hi):
    if hi <= lo:
        return
    median = median_of_3(a, lo, hi)
    a[lo], a[median] = exch(a[lo], a[median])
    j = partition(a, lo, hi)
    quick_sort_v3(a, lo, j - 1)
    quick_sort_v3(a, j + 1, hi)


# Versão 4 - top-down com cut-off e mediana de 3 (Versões 2 + 3, slide 24)
def quick_sort_v4(a, lo, hi):
    if hi <= lo + CUTOFF - 1:
        insertion_sort(a, lo, hi)
        return
    median = median_of_3(a, lo, hi)
    a[lo], a[median] = exch(a[lo], a[median])
    j = partition(a, lo, hi)
    quick_sort_v4(a, lo, j - 1)
    quick_sort_v4(a, j + 1, hi)


# Versão 5 - quick sort não-recursivo (bottom-up) sem otimizações (slide 25).
# A pilha é uma list do Python (append/pop em O(1)). Empilha o sub-array maior
# e ordena o menor primeiro, então a pilha nunca passa de lg N pares (lo, hi).
def quick_sort_v5(a, lo, hi):
    P = [hi, lo]
    while P:
        lo = P.pop()
        hi = P.pop()
        if hi <= lo:
            continue
        i = partition(a, lo, hi)
        if i - lo > hi - i:  # Test the size of sub-arrays
            P.append(i - 1)
            P.append(lo)  # Push the larger one
            P.append(hi)
            P.append(i + 1)  # Sort the smaller one first
        else:
            P.append(hi)
            P.append(i + 1)
            P.append(i - 1)
            P.append(lo)


# Versão 6 - Versão 5 com cut-off e mediana de 3
def quick_sort_v6(a, lo, hi):
    P = [hi, lo]
    while P:
        lo = P.pop()
        hi = P.pop()
        if hi <= lo + CUTOFF - 1:
            insertion_sort(a, lo, hi)
            continue
        median = median_of_3(a, lo, hi)
        a[lo], a[median] = exch(a[lo], a[median])
        i = partition(a, lo, hi)
        if i - lo > hi - i:
            P.append(i - 1)
            P.append(lo)
            P.append(hi)
            P.append(i + 1)
        else:
            P.append(hi)
            P.append(i + 1)
            P.append(i - 1)
            P.append(lo)


# Versão 7 - melhor versão até aqui (Versão 4) com embaralhamento da entrada
# (slide 11)
def quick_sort_v7(a, lo, hi):
    shuffle(a, lo, hi)  # Needed for performance guarantee
    quick_sort_v4(a, lo, hi)


# Versão 8 - top-down com particionamento 3-way de Dijkstra (slide 35)
def quick_sort_v8(a, lo, hi):
    if hi <= lo:
        return
    v = a[lo]
    lt, gt, i = lo, hi, lo
    while i <= gt:
        if less(a[i], v):
            a[lt], a[i] = exch(a[lt], a[i])
            lt += 1
            i += 1
        elif less(v, a[i]):
            a[i], a[gt] = exch(a[i], a[gt])
            gt -= 1
        else:
            i += 1
    quick_sort_v8(a, lo, lt - 1)
    quick_sort_v8(a, gt + 1, hi)
