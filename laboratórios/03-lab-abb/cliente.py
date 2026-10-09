# Exercício 2 - Cliente do TAD ABB
#
# Uso: python3 cliente.py N
#   N = número de chaves aleatórias (inteiros em [0, 1000]) a inserir na ABB.
#
# O programa cria a ABB, insere as chaves, exibe a altura final e os
# caminhamentos (recursivos e não-recursivos), e verifica que a inserção de
# chaves repetidas não altera a estrutura.

import sys

from ABB import ABB, criaABB, busca, conta, contaNos, altura
from ABB import insereElementoABB, insereElementoABBIterativo
from ABB import ImprimeABBinLevel, ImprimeABBinOrder, ImprimeABBpreOrder, ImprimeABBpostOrder
from ABB import ImprimeABBinOrderIterativo, ImprimeABBpreOrderIterativo, ImprimeABBpostOrderIterativo
from ABB import preOrder, inOrder, postOrder, levelOrder
from ABB import preOrderIterativo, inOrderIterativo, postOrderIterativo
from random import randint

n_args = len(sys.argv)

# devolve a lista de chaves produzida por um caminhamento
def coleta(caminhamento, h):
    chaves = []
    caminhamento(h, chaves.append)
    return chaves

def main():
    print("Total arguments passed:", n_args)
    for i in range(n_args):
        # verificação de cada argumento de sys.argv
        print(sys.argv[i])

    if n_args < 2 or not sys.argv[1].isdigit() or int(sys.argv[1]) < 1:
        print("Uso: python3 cliente.py N   (N >= 1)")
        return
    N = int(sys.argv[1])

    # geração de N valores aleatórios no intervalo [0-1000]
    chaves = [randint(0, 1000) for _ in range(N)]
    print("\nChaves geradas:", chaves)

    # a árvore é criada com a primeira chave; as demais são inseridas
    # alternando as versões recursiva e iterativa da inserção
    h = criaABB(chaves[0])
    for i in range(1, N):
        if i % 2 == 1:
            h = insereElementoABB(h, chaves[i])
        else:
            h = insereElementoABBIterativo(h, chaves[i])

    distintas = len(set(chaves))
    print("\nChaves geradas:", N, "| distintas:", distintas,
          "| nós na ABB:", contaNos(h))
    print("Altura da ABB:", altura(h))
    print("Altura de uma ABB degenerada com", distintas, "nós seria:", distintas - 1)

    # caminhamentos
    print("\npre-order  (rec):", end=' '); ImprimeABBpreOrder(h); print()
    print("pre-order  (it): ", end=' '); ImprimeABBpreOrderIterativo(h); print()
    print("in-order   (rec):", end=' '); ImprimeABBinOrder(h); print()
    print("in-order   (it): ", end=' '); ImprimeABBinOrderIterativo(h); print()
    print("post-order (rec):", end=' '); ImprimeABBpostOrder(h); print()
    print("post-order (it): ", end=' '); ImprimeABBpostOrderIterativo(h); print()
    print("level-order:     ", end=' '); ImprimeABBinLevel(h); print()

    # verificações
    print("\nVerificações:")
    print("  in-order ordenado e sem repetição:",
          coleta(inOrder, h) == sorted(set(chaves)))
    print("  pre-order  rec == it:", coleta(preOrder, h) == coleta(preOrderIterativo, h))
    print("  in-order   rec == it:", coleta(inOrder, h) == coleta(inOrderIterativo, h))
    print("  post-order rec == it:", coleta(postOrder, h) == coleta(postOrderIterativo, h))
    print("  busca/conta de todas as chaves geradas:",
          all(busca(h, k) is not None and conta(h, k) == 1 for k in chaves))

    # inserção de chaves repetidas deve terminar sem modificar a estrutura
    antes = (coleta(preOrder, h), contaNos(h), altura(h))
    for k in chaves:
        h = insereElementoABB(h, k)
        h = insereElementoABBIterativo(h, k)
    depois = (coleta(preOrder, h), contaNos(h), altura(h))
    print("  reinserção de chaves existentes não altera a ABB:", antes == depois)

main()
