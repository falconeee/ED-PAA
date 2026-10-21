# Exercício 1 - Item

def less(A, B):
    return A < B

def exch(A, B):
    C = A
    A = B
    B = C
    return (A, B)

def compexch(A, B):
    if less(B, A):
        A, B = exch(A, B)
    return A, B
