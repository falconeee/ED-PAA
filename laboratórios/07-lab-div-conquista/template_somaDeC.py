def soma_divisao_e_conquista(A, inicio, fim):
    # vetor vazio
    if inicio > fim:
        return 0
    # caso base: um único elemento
    if inicio == fim:
        return A[inicio]

    # divisão: quebra o vetor ao meio
    meio = (inicio + fim) // 2

    # conquista: resolve cada metade recursivamente
    soma_esq = soma_divisao_e_conquista(A, inicio, meio)
    soma_dir = soma_divisao_e_conquista(A, meio + 1, fim)

    # combinação: uma única soma
    return soma_esq + soma_dir

# Função para chamar a soma
def soma_vetor(A):
    return soma_divisao_e_conquista(A, 0, len(A) - 1)

# EXEMPLO DE USO
A = [5, 2, 8, 3, 7]

resultado = soma_vetor(A)
print("Vetor:", A)
print("Soma calculada por divisão e conquista:", resultado)

'''
Análise do comportamento pela relação de recorrência:

Se T(n) é o tempo para somar n = fim - inicio + 1 elementos. A divisão e a combinação (soma_esq + soma_dir) custam Θ(1), 
e são resolvidas duas instâncias de tamanho ⌈n/2⌉ e ⌊n/2⌋:

    T(1) = Θ(1)
    T(n) = T(⌈n/2⌉) + T(⌊n/2⌋) + Θ(1)
    T(n) = 2T(n/2) + Θ(1)

Pelo teorema mestre (a = 2, b = 2, f(n) = Θ(1)): n^(log_b a) = n^1 e f(n) = O(n^(1-ε)) com ε = 1, logo cai no caso 1 e T(n) = Θ(n).

Contando apenas as adições, S(n) = S(⌈n/2⌉) + S(⌊n/2⌋) + 1 com S(1) = 0, que a solução exata é S(n) = n - 1.

Comparação com o algoritmo trivial (percorrer o vetor acumulando a soma):
    T_trivial(n) = T_trivial(n-1) + Θ(1) = Θ(n), também com n - 1 adições.

Assim a divisão e conquista não melhora a complexidade assintótica e os dois são Θ(n) e fazem o mesmo número de adições.
'''
