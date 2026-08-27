from pilha import PilhaLista, Empty, UnknownOperator

# Função que retorna a prioridade de um operador. Quanto maior o valor, maior a prioridade.
def prioridade(x):
    if x == '+': return 1
    elif x == '-': return 1
    elif x == '*': return 2
    elif x == '/': return 2
    elif x == '^': return 3
    elif x == '(': return 4 # caso particular
    elif x == ')': return 5 # caso particular
    else: return 0          # não é operador


# Transformação de in-fixa para pós-fixa
'''
Função que recebe uma expressão em notação in-fixa e retorna sua correspondente em notação 
pós-fixa. As expressões de entrada e saída são descritas como uma lista de strings.

@param inFixa: Lista de strings com a entrada -- expressão na notação in-fixa
@return posFixa: Lista de strings com a saída em notação pós-fixa
'''
def fromInToPos(inFixa):
    pilha = PilhaLista() # Cria pilha vazia para armazenar operadores
    posFixa = [] # Cria lista vazia para armazenar a expressão pós-fixa

    for p in inFixa: # percorre cada elemento da expressão in-fixa
        # se p é operando: coloca direto na pós-fixa
        if prioridade(p) == 0:
            posFixa.append(p)

        # se p é abre parêntesis: empilha
        elif p == '(':
            pilha.push(p)

        # se p é fecha parêntesis: desempilha os operadores até o primeiro abre
        elif p == ')':
            while pilha.top() != '(':
                posFixa.append(pilha.pop())
            pilha.pop() # descarta o '(' correspondente

        # se p é operador: tira da pilha os de prioridade maior ou igual e empilha p
        else:
            while (not pilha.is_empty() and pilha.top() != '(' and prioridade(pilha.top()) >= prioridade(p)):
                posFixa.append(pilha.pop())
            pilha.push(p)

    # desempilha os operadores que ainda estão na pilha
    while not pilha.is_empty():
        posFixa.append(pilha.pop())

    return posFixa

'''
Função que recebe uma expressão em notação pós-fixa e retorna a sua resolução matemática.

@param posFixa: Lista de strings com a entrada -- expressão na notação pós-fixa
@return resultado: valor final da expressão, após sua resolução.
'''
def solvePosFixa(posFixa):
    pilha = PilhaLista() # Cria pilha vazia para armazenar operandos

    for p in posFixa: # percorre cada elemento da expressão pós-fixa
        # se p é operando: empilha seu valor numérico
        if prioridade(p) == 0:
            pilha.push(float(p) if '.' in p else int(p))

        # se p é operador binário: opera os 2 elementos do topo
        else:
            b = pilha.pop()
            a = pilha.pop()
            if p == '+': pilha.push(a + b)
            elif p == '-': pilha.push(a - b)
            elif p == '*': pilha.push(a * b)
            elif p == '/': pilha.push(a / b)
            elif p == '^': pilha.push(a ** b)
            else: raise UnknownOperator("Operador desconhecido: " + p)

    resultado = pilha.pop()

    # a pilha deve estar vazia ao final de uma expressão bem formada
    if not pilha.is_empty():
        raise UnknownOperator("Expressão pós-fixa mal formada")

    return resultado

     
def main():
    # Exemplos de entrada
    inFixa = "12 + ( 13 - 4 * 2 ) * 15" # resultado = 87
    inFixa = "12 + 13 - 4 * 2 * 15" # resultado = -95
    inFixa = "3 + 4 * 2 / ( 1 - 5 ) ^ 2 ^ 3" # resultado = 3.0001220703125
    inFixa = "5 + 3 * ( 12 / ( 3 + 1 ) - 1 )" # resultado = 11
    inFixa = "1 * ( 2 + 3 * ( 4 + 5 ) )" # resultado = 29

    # transforma a string de entrada em lista de strings
    inFixa = inFixa.split()

    # chamada da transformação de notações (in-fixa -> pós-fixa)
    posFixa = fromInToPos(inFixa)

    # impressão das notações em formato de string
    print("Notação in-fixa: ", " ".join(inFixa))
    print("Notação pós-fixa: ", " ".join(posFixa))

    # resolução da equação em notação pós-fixa
    print(solvePosFixa(posFixa))

main()
