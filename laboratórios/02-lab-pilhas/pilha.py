# TAD de exceção para pilha vazia
class Empty(Exception):
    pass

# TAD de exceção para operador desconhecido
class UnknownOperator(Exception):
    pass

class PilhaLista:

    # Pilha como uma lista

    # Construtor da classe PilhaLista
    def __init__(self):
        self._pilha = [] # lista que conterá a pilha

    # Retorna o tamanho da pilha
    def __len__(self):
        return len(self._pilha)

    # Retorna True se pilha vazia
    def is_empty(self):
        return len(self._pilha) == 0

    # Empilha novo elemento
    def push(self, e):
        self._pilha.append(e)

    # Retorna o elemento do topo da pilha sem retirá-lo com exceção se pilha vazia
    def top(self):
        if self.is_empty():
            raise Empty("Pilha vazia")
        return self._pilha[-1]

    # Desempilha elemento com exceção se pilha vazia
    def pop(self):
        if self.is_empty():
            raise Empty("Pilha vazia")
        return self._pilha.pop()
