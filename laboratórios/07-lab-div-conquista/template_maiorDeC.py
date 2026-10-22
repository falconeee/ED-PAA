def max_divisao_e_conquista(A, p, r):
    # caso base: um único elemento é o próprio máximo (0 comparações)
    if p == r:
        return A[p]

    # divisão: quebra A[p..r] em A[p..q] e A[q+1..r]
    q = (p + r) // 2

    # conquista: máximo de cada metade
    max_esq = max_divisao_e_conquista(A, p, q)
    max_dir = max_divisao_e_conquista(A, q + 1, r)

    # combinação: 1 comparação entre elementos do vetor
    if max_esq >= max_dir:
        return max_esq
    return max_dir

# EXEMPLO DE USO
A = [7, 3, 12, 1, 9, 15, 4]

resultado = max_divisao_e_conquista(A, 0, len(A) - 1)

print("Vetor:", A)
print("Máximo encontrado por divisão e conquista:", resultado)

'''
Análise do comportamento pela relação de recorrência:

Seja n = r - p + 1 e C(n) o número de comparações entre elementos do vetor.
No caso base (n = 1) nenhuma comparação é feita; Se for maior que 1 o vetor é
dividido em duas metades de tamanhos ⌈n/2⌉ e ⌊n/2⌋ e é feita uma comparação para combinar os resultados:

    C(1) = 0
    C(n) = C(⌈n/2⌉) + C(⌊n/2⌋) + 1,   com o n ≥ 2

Teorema mestre: C(n) = a·C(n/b) + f(n) com a = 2, b = 2 e f(n) = 1.
    n^(log_b a) = n^(log_2 2) = n
    f(n) = 1 = O(n^(1-ε)) para ε = 1  →  caso 1
    Logo C(n) = Θ(n^(log_b a)) = Θ(n).

Solução exata (por indução): C(n) = n - 1.
    C(1) = 0 = 1 - 1;
    C(n) = (⌈n/2⌉ - 1) + (⌊n/2⌋ - 1) + 1 = n - 1.

Por exemplo no exemplo do vetor A = [7, 3, 12, 1, 9, 15, 4] (n = 7) são feitas 6 comparações.

Esse é o mesmo número de comparações da busca linear e é o ótimo. Todo elemento
diferente do máximo precisa "perder" pelo menos uma comparação, então qualquer
algoritmo baseado em comparações faz no mínimo n - 1 delas.
'''