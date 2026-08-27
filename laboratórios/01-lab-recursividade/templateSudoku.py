''' 
    Função que busca um espaço vazio no Grid do Sudoku (posição == 0) e returna a posição livre
    Caso não encontre uma posição livre no Grid, retorna False

    @input grid: Grid do sudoku
    @input r: número de linhas do Grid do sudoku
    @input c: número de colunas do Grid do sudoku
    @return row,col: posição válida ainda não preenchida do Grid
'''
def encontraPosicaoValida(grid, r, c):
    pass

'''
    Função que verifica se um número candidato pode ser utilizado na posição do Grid do Sudoku.
    Deve-se verificar a existência do candidato passado na linha, coluna e região (n x n) do Grid.

    @param grid: Grid do sudoku
    @param num: número candidato a ser colocado na posição do Grid
    @param row: linha em que o número será preenchido no Grid
    @param col: coluna em que o número será preenchido no Grid
    @param dim: dimensão do Grid do Sudoku

    @return: True se o candidato pode ser utilizado na posição ou False caso contrário
'''
def verificaCandidatoPosicaoValida(grid, num, row, col, dim):
    # Verificar se a linha inclui o número candidato  
    # Verificar se a coluna inclui o número cadidato
    # Verificar se o número já está incluído no bloco individual do Grid
    pass

'''
    Função de solução do Sudoku. Deve buscar uma nova posição válida, e caso esta não exista, retornar True
    pois todas as células já foram preenchidas no Grid.
    Caso contrário, deve resolver o problema verificando possíveis candidatos para a posição não visitada 
    encontrada (posição válida).

    Para cada possível candidato (permutação de 1, ..., n) deve-se verificar a validade deste para a posição válida.
    Se o número candidato for válido para a posição, deve-se atualizar o conteúdo do Grid com este número e prosseguir
    com a resolução do problema para a próxima posição válida a ser preenchida (de forma recursiva), retornando
    True sempre que um novo candidato pode ser colocado no Grid para esta possível solução (princípio do backtracking).

    Caso contrário (algum possível candidato da solução candidata não atende aos requisitos de preenchimento do Grid)
    a função de solução do Sudoku deve retornar False após reestabelecer o valor 0 para a posição válida do Grid.

    @param grid: Grid do sudoku
    @param dimSudoku: dimensão total do tabuleiro (linhas x colunas) do Sudoku

    @return: True se houver solução e False caso contrário
'''
def resolveSudoku(grid, dimSudoku):
   pass


def main():
    dimSudoku = 9

    # Exemplo de entrada do Grid do Sudoku - entrada 3x3 -> 9x9
    # 0 -> posições não preenchidas

    grid = [[3, 0, 6, 5, 0, 8, 4, 0, 0],
            [5, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 7, 0, 0, 0, 0, 3, 1],
            [0, 0, 3, 0, 1, 0, 0, 8, 0],
            [9, 0, 0, 8, 6, 3, 0, 0, 5],
            [0, 5, 0, 0, 9, 0, 6, 0, 0],
            [1, 3, 0, 0, 0, 0, 2, 5, 0],
            [0, 0, 0, 0, 0, 0, 0, 7, 4],
            [0, 0, 5, 2, 0, 6, 3, 0, 0]]

    '''
    Output
    [3, 1, 6, 5, 7, 8, 4, 9, 2]
    [5, 2, 9, 1, 3, 4, 7, 6, 8]
    [4, 8, 7, 6, 2, 9, 5, 3, 1]
    [2, 6, 3, 4, 1, 5, 9, 8, 7]
    [9, 7, 4, 8, 6, 3, 1, 2, 5]
    [8, 5, 1, 7, 9, 2, 6, 4, 3]
    [1, 3, 8, 9, 4, 7, 2, 5, 6]
    [6, 9, 2, 3, 5, 1, 8, 7, 4]
    [7, 4, 5, 2, 8, 6, 3, 1, 9]

    Exemplo 2:
    [1, 0, 0, 0]
    [0, 0, 3, 4]
    [0, 0, 0, 0]
    [0, 3, 0, 1]
     -> Não existe solução!.
    '''
    
    # Chamada de solução do Sudoku - deve alterar o Grid com a solução
    if (resolveSudoku(grid, dimSudoku)):
        for i in grid:
            print(i)
    else:
        print("Não existe solução!")

main()