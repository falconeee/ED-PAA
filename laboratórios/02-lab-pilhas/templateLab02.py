from pilha import PilhaLista, Empty, UnknownOperator

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
    pass

'''
Função que recebe uma expressão em notação pós-fixa e retorna a sua resolução matemática.

@param posFixa: Lista de strings com a entrada -- expressão na notação pós-fixa
@return resultado: valor final da expressão, após sua resolução.
'''
def solvePosFixa(posFixa):
    pass

     
def main():
    # exemplos de entrada
    inFixa = "12 + ( 13 - 4 * 2 ) * 15" # resultado = 87
    # inFixa = "12 + 13 - 4 * 2 * 15" # resultado = -95

    # transforma a string de entrada em lista de strings

    # chamada da transformação de notações (in-fixa -> pós-fixa)
    posFixa = fromInToPos(inFixa)

    # impressão das notações em formato de string
    print("Notação in-fixa: ", " ".join(inFixa))
    print("Notação pós-fixa: ", " ".join(posFixa))

    # resolução da equação em notação pós-fixa
    print(solvePosFixa(posFixa))

main()