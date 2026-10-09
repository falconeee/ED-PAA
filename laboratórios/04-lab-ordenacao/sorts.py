from item import less, exch, compexch

# Exercício 3 - Selection sort
def selection_sort(a, lo, hi):
    for i in range(lo, hi):
        menor = i
        for j in range(i + 1, hi + 1):
            if less(a[j], a[menor]):
                menor = j
        if menor != i:
            a[i], a[menor] = exch(a[i], a[menor])


# Exercício 4 - Insertion sort
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


# Exercício 5 - Bubble sort
def bubble_sort(a, lo, hi):
    fim = hi
    while fim > lo:
        ultima_troca = lo
        for j in range(lo, fim):
            if less(a[j + 1], a[j]):
                a[j], a[j + 1] = exch(a[j], a[j + 1])
                ultima_troca = j
        fim = ultima_troca


# Exercício 6 - Shaker sort (bubble sort bidirecional)
def shaker_sort(a, lo, hi):
    esq, dir = lo, hi
    while esq < dir:
        ultima_troca = esq
        for j in range(esq, dir):
            if less(a[j + 1], a[j]):
                a[j], a[j + 1] = exch(a[j], a[j + 1])
                ultima_troca = j
        dir = ultima_troca

        ultima_troca = dir
        for j in range(dir, esq, -1):
            if less(a[j], a[j - 1]):
                a[j - 1], a[j] = exch(a[j - 1], a[j])
                ultima_troca = j
        esq = ultima_troca
