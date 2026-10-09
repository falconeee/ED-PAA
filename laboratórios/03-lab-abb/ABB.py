# TAD ABB - Árvore de Busca Binária com chaves inteiras
#
# O nó da ABB é uma estrutura opaca: os campos (_info, _eprox, _dprox) são
# privados e o cliente só manipula a árvore através das funções deste módulo.
# Uma ABB vazia é representada por None.

from pilhaListaEncadeada import PilhaListaEncadeada
from filaListaEncadeada import FilaListaEncadeada


class ABB:
    
    __slots__ = '_info', '_eprox', '_dprox'

    def __init__ (self, raiz):
        # cria uma nova ABB com o info raiz e sem filhos
        self._info = raiz
        self._eprox = None
        self._dprox = None
    

# ---------------------------------------------------------------------------
# Exercício 1 - criação e inserção
# ---------------------------------------------------------------------------

# Cria uma ABB com um único elemento (a raiz)
def criaABB(raiz):
    return ABB(raiz)

# Insere elemento na ABB h - versão recursiva.
# Retorna a raiz da (sub)árvore resultante, o que permite tratar de forma
# uniforme a inserção em uma árvore vazia (None).
# Chaves repetidas são ignoradas silenciosamente (ABB não admite repetição).
def insereElementoABB(h, elemento):
    if h is None:
        return ABB(elemento)
    if elemento < h._info:
        h._eprox = insereElementoABB(h._eprox, elemento)
    elif elemento > h._info:
        h._dprox = insereElementoABB(h._dprox, elemento)
    # elemento == h._info: já existe, nada a fazer
    return h

# Insere elemento na ABB h - versão iterativa.
# Mesma interface e mesmo comportamento da versão recursiva.
def insereElementoABBIterativo(h, elemento):
    if h is None:
        return ABB(elemento)
    atual = h
    while True:
        if elemento < atual._info:
            if atual._eprox is None:
                atual._eprox = ABB(elemento)
                break
            atual = atual._eprox
        elif elemento > atual._info:
            if atual._dprox is None:
                atual._dprox = ABB(elemento)
                break
            atual = atual._dprox
        else:
            break   # chave já existe: termina sem modificar a árvore
    return h


# ---------------------------------------------------------------------------
# Consultas
# ---------------------------------------------------------------------------

# Procura elemento com info igual a v na ABB h
# Versão recursiva - retorna o nó encontrado ou None
def busca(h, v):
    if h is None or h._info == v:
        return h
    if v < h._info:
        return busca(h._eprox, v)
    return busca(h._dprox, v)

# conta elementos com info igual a v na ABB h
# (em uma ABB sem repetição o resultado é sempre 0 ou 1)
def conta(h, v):
    if h is None:
        return 0
    if v < h._info:
        return conta(h._eprox, v)
    if v > h._info:
        return conta(h._dprox, v)
    return 1 + conta(h._dprox, v)

# número total de nós da ABB h
def contaNos(h):
    if h is None:
        return 0
    return 1 + contaNos(h._eprox) + contaNos(h._dprox)

# altura de uma ABB - raíz é altura 0, árvore vazia é altura -1
def altura(h):
    if h is None:
        return -1
    return 1 + max(altura(h._eprox), altura(h._dprox))


# ---------------------------------------------------------------------------
# Exercício 3 - caminhamentos recursivos
# Cada caminhamento recebe uma função 'visita' aplicada a cada chave.
# ---------------------------------------------------------------------------

def preOrder(h, visita):
    if h is None:
        return
    visita(h._info)
    preOrder(h._eprox, visita)
    preOrder(h._dprox, visita)

def inOrder(h, visita):
    if h is None:
        return
    inOrder(h._eprox, visita)
    visita(h._info)
    inOrder(h._dprox, visita)

def postOrder(h, visita):
    if h is None:
        return
    postOrder(h._eprox, visita)
    postOrder(h._dprox, visita)
    visita(h._info)


# ---------------------------------------------------------------------------
# Exercício 5 - caminhamentos não-recursivos usando a pilha (exercício 4)
# ---------------------------------------------------------------------------

def preOrderIterativo(h, visita):
    if h is None:
        return
    P = PilhaListaEncadeada()
    P.push(h)
    while not P.is_empty():
        no = P.pop()
        visita(no._info)
        # o filho da direita entra antes para que o da esquerda saia primeiro
        if no._dprox is not None:
            P.push(no._dprox)
        if no._eprox is not None:
            P.push(no._eprox)

def inOrderIterativo(h, visita):
    P = PilhaListaEncadeada()
    no = h
    while no is not None or not P.is_empty():
        # desce até o nó mais à esquerda, empilhando o caminho
        while no is not None:
            P.push(no)
            no = no._eprox
        no = P.pop()
        visita(no._info)
        no = no._dprox

def postOrderIterativo(h, visita):
    P = PilhaListaEncadeada()
    no = h
    ultimoVisitado = None
    while no is not None or not P.is_empty():
        if no is not None:
            P.push(no)
            no = no._eprox
        else:
            topo = P.top()
            # se existe filho da direita ainda não visitado, desce por ele
            if topo._dprox is not None and ultimoVisitado is not topo._dprox:
                no = topo._dprox
            else:
                visita(topo._info)
                ultimoVisitado = P.pop()


# ---------------------------------------------------------------------------
# Exercício 7 - caminhamento em níveis usando a fila (exercício 6)
# ---------------------------------------------------------------------------

def levelOrder(h, visita):
    if h is None:
        return
    F = FilaListaEncadeada()
    F.enqueue(h)
    while not F.is_empty():
        no = F.dequeue()
        visita(no._info)
        if no._eprox is not None:
            F.enqueue(no._eprox)
        if no._dprox is not None:
            F.enqueue(no._dprox)


# ---------------------------------------------------------------------------
# Funções de impressão (interface esperada pelo cliente)
# ---------------------------------------------------------------------------

def _imprime(v):
    print(v, end=' ')

def ImprimeABBinOrder(h):
    inOrder(h, _imprime)

def ImprimeABBpreOrder(h):
    preOrder(h, _imprime)

def ImprimeABBpostOrder(h):
    postOrder(h, _imprime)

def ImprimeABBinOrderIterativo(h):
    inOrderIterativo(h, _imprime)

def ImprimeABBpreOrderIterativo(h):
    preOrderIterativo(h, _imprime)

def ImprimeABBpostOrderIterativo(h):
    postOrderIterativo(h, _imprime)

def ImprimeABBinLevel(h):
    levelOrder(h, _imprime)


# Monta uma ABB a partir de uma lista 
# Elementos repetidos são ignorados (uma ABB não admite chaves repetidas)
def montaABB(a, a_len):
    if a_len == 0:
        return None
    h = criaABB(a[0])
    for i in range(1, a_len):
        h = insereElementoABB(h, a[i])
    return h


if __name__ == '__main__':
    # Testes

    lista = [0, 1, 2, 3, 4, 5, 6]
    outralista = [10, 4, 2, 30, 7, 15, 40, 27, 60, 6]
    mabb = montaABB(lista, len(lista))
    moabb = montaABB(outralista, len(outralista))

    print("alturas:", altura(mabb), altura(moabb))

    print("in-order (recursivo / iterativo)")
    ImprimeABBinOrder(mabb); print()
    ImprimeABBinOrderIterativo(mabb); print()
    ImprimeABBinOrder(moabb); print()
    ImprimeABBinOrderIterativo(moabb); print()

    print("pre-order (recursivo / iterativo)")
    ImprimeABBpreOrder(mabb); print()
    ImprimeABBpreOrderIterativo(mabb); print()
    ImprimeABBpreOrder(moabb); print()
    ImprimeABBpreOrderIterativo(moabb); print()

    print("post-order (recursivo / iterativo)")
    ImprimeABBpostOrder(mabb); print()
    ImprimeABBpostOrderIterativo(mabb); print()
    ImprimeABBpostOrder(moabb); print()
    ImprimeABBpostOrderIterativo(moabb); print()

    print("level-order")
    ImprimeABBinLevel(mabb); print()
    ImprimeABBinLevel(moabb); print()
