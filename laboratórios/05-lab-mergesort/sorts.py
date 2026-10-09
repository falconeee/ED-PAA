from item import less, compexch

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


# Merge dos sub-arrays ordenados a[lo..mid] e a[mid+1..hi] (slide 7)
def merge(a, aux, lo, mid, hi):
    for k in range(lo, hi + 1):
        aux[k] = a[k]
    i, j = lo, mid + 1
    for k in range(lo, hi + 1):
        if i > mid:
            a[k] = aux[j]
            j += 1
        elif j > hi:
            a[k] = aux[i]
            i += 1
        elif less(aux[j], aux[i]):
            a[k] = aux[j]
            j += 1
        else:
            a[k] = aux[i]
            i += 1


# Versão 1 - merge sort top-down recursivo sem otimizações (slides 7 e 8)
def _top_down(a, aux, lo, hi):
    if hi <= lo:
        return
    mid = lo + (hi - lo) // 2
    _top_down(a, aux, lo, mid)
    _top_down(a, aux, mid + 1, hi)
    merge(a, aux, lo, mid, hi)


def merge_sort_v1(a, lo, hi):
    aux = [None] * len(a)
    _top_down(a, aux, lo, hi)


# Versão 2 - top-down com cut-off para insertion sort (slide 15)
def _top_down_cutoff(a, aux, lo, hi):
    if hi <= lo + CUTOFF - 1:
        insertion_sort(a, lo, hi)
        return
    mid = lo + (hi - lo) // 2
    _top_down_cutoff(a, aux, lo, mid)
    _top_down_cutoff(a, aux, mid + 1, hi)
    merge(a, aux, lo, mid, hi)


def merge_sort_v2(a, lo, hi):
    aux = [None] * len(a)
    _top_down_cutoff(a, aux, lo, hi)


# Versão 3 - top-down com merge skip, sem cut-off (slide 16)
def _top_down_skip(a, aux, lo, hi):
    if hi <= lo:
        return
    mid = lo + (hi - lo) // 2
    _top_down_skip(a, aux, lo, mid)
    _top_down_skip(a, aux, mid + 1, hi)
    if not less(a[mid + 1], a[mid]):
        return
    merge(a, aux, lo, mid, hi)


def merge_sort_v3(a, lo, hi):
    aux = [None] * len(a)
    _top_down_skip(a, aux, lo, hi)


# Versão 4 - top-down com cut-off e merge skip (Versões 2 + 3)
def _top_down_cutoff_skip(a, aux, lo, hi):
    if hi <= lo + CUTOFF - 1:
        insertion_sort(a, lo, hi)
        return
    mid = lo + (hi - lo) // 2
    _top_down_cutoff_skip(a, aux, lo, mid)
    _top_down_cutoff_skip(a, aux, mid + 1, hi)
    if not less(a[mid + 1], a[mid]):
        return
    merge(a, aux, lo, mid, hi)


def merge_sort_v4(a, lo, hi):
    aux = [None] * len(a)
    _top_down_cutoff_skip(a, aux, lo, hi)


# Versão 5 - merge sort bottom-up sem otimizações (slide 19)
def merge_sort_v5(a, lo, hi):
    aux = [None] * len(a)
    sz = 1
    while sz <= hi - lo:
        for i in range(lo, hi - sz + 1, 2 * sz):
            merge(a, aux, i, i + sz - 1, min(i + 2 * sz - 1, hi))
        sz = 2 * sz


# Versão 6 - bottom-up com "cut-off": ordena blocos de CUTOFF itens com
# insertion sort e começa as passadas de merge com sub-arrays desse tamanho
def merge_sort_v6(a, lo, hi):
    aux = [None] * len(a)
    for i in range(lo, hi + 1, CUTOFF):
        insertion_sort(a, i, min(i + CUTOFF - 1, hi))
    sz = CUTOFF
    while sz <= hi - lo:
        for i in range(lo, hi - sz + 1, 2 * sz):
            merge(a, aux, i, i + sz - 1, min(i + 2 * sz - 1, hi))
        sz = 2 * sz


# Versão 7 - Versão 6 com merge skip
def merge_sort_v7(a, lo, hi):
    aux = [None] * len(a)
    for i in range(lo, hi + 1, CUTOFF):
        insertion_sort(a, i, min(i + CUTOFF - 1, hi))
    sz = CUTOFF
    while sz <= hi - lo:
        for i in range(lo, hi - sz + 1, 2 * sz):
            mid = i + sz - 1
            if less(a[mid + 1], a[mid]):
                merge(a, aux, i, mid, min(i + 2 * sz - 1, hi))
        sz = 2 * sz
