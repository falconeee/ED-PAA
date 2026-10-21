# ED-PAA — Estruturas de Dados e Projeto e Análise de Algoritmos

Material da disciplina de Estruturas de Dados e Projeto e Análise de Algoritmos:
slides das aulas e as soluções dos laboratórios, todas em Python.

## Estrutura do repositório

```
ED-PAA/
├── aulas/            # slides das aulas (PDF)
└── laboratórios/     # um diretório por laboratório: roteiro (PDF) + solução
    ├── 01-lab-recursividade/
    ├── 02-lab-pilhas/
    ├── 03-lab-abb/
    ├── 04-lab-ordenacao/
    ├── 05-lab-mergesort/
    └── 06-lab-quicksort/
```

### Aulas

| Aula | Tema |
|---:|---|
| 01 | Revisão de gestão de memória, tipos de dados (abstrato, opaco, estruturas genéricas) |
| 02 | Tipos Abstratos de Dados |
| 03 | Recursividade |
| 05 | Pilhas |
| 06 | Filas |
| 08 | Listas Encadeadas |
| 09 | Árvores e Tabela Hash |
| 11 | Introdução à Análise de Algoritmos (partes 1 e 2) |
| 12 | Algoritmos de Busca |
| 14 | Métodos elementares de ordenação |
| 15 | Merge Sort |
| 16 | Quick Sort |
| 19 | Introdução a Paradigmas de Projeto de Algoritmos |

### Laboratórios

| Lab | Tema | Arquivos principais |
|---|---|---|
| [01](laboratórios/01-lab-recursividade) | Recursividade: resolvedor de Sudoku por backtracking | `solucaoUnicaSudoku.py` (solução), `templateSudoku.py` (modelo fornecido) |
| [02](laboratórios/02-lab-pilhas) | Pilhas: conversão de expressões infixas para pós-fixas e avaliação | `pilha.py` (TAD pilha), `Lab02.py` (solução), `templateLab02.py` (modelo fornecido) |
| [03](laboratórios/03-lab-abb) | Árvore Binária de Busca: inserção, busca, altura e caminhamentos recursivos e iterativos | `ABB.py` (TAD), `cliente.py`, `pilhaListaEncadeada.py`, `filaListaEncadeada.py` |
| [04](laboratórios/04-lab-ordenacao) | Ordenação elementar: selection, insertion, bubble e shaker sort | `sorts.py`, `item.py`, `cliente.py`, `resultados.md` |
| [05](laboratórios/05-lab-mergesort) | Merge sort: 7 versões (top-down, bottom-up, cut-off, merge skip) | `sorts.py`, `cliente.py`, `experimentos.py`, `resultados.md` |
| [06](laboratórios/06-lab-quicksort) | Quick sort: 8 versões (cut-off, mediana de 3, não-recursivo, shuffle, 3-way) | `sorts.py`, `cliente.py`, `experimentos.py`, `resultados.md`, `respostas.md` |

Cada laboratório traz o roteiro em PDF. Nos labs de ordenação, `resultados.md` tem as
tabelas de tempo medidas e `respostas.md` (lab 06) responde às perguntas do roteiro.

## Como executar

Requisito: Python 3.12 (não há dependências externas). Execute os scripts de dentro do
diretório do laboratório, já que os módulos se importam pelo nome do arquivo:

```bash
cd laboratórios/03-lab-abb
python3 cliente.py 20                # insere 20 chaves aleatórias na ABB
```

Os clientes dos labs de ordenação leem `N` inteiros da entrada padrão, escrevem o array
ordenado na saída padrão e o tempo de ordenação na saída de erro:

```bash
cd laboratórios/04-lab-ordenacao
python3 cliente.py 1000 insertion < input/in/unif_rand/1Kunif_rand.txt > /dev/null

cd laboratórios/06-lab-quicksort
python3 cliente.py 100000 v4 --cutoff 8 < input/unif_rand/100000.txt > /dev/null
python3 cliente.py --help            # lista as versões disponíveis
python3 experimentos.py              # roda todos os experimentos de resultados.md
```

### Arquivos de entrada

Os arquivos de entrada (`*.txt`) **não são versionados**: são grandes (só os do lab 06
somam ~500 MB) e são fornecidos junto com cada roteiro. Para rodar os clientes e os
experimentos, coloque-os em `input/` dentro do laboratório, seguindo a organização
por tipo de entrada:

```
input/
├── unif_rand/        # chaves aleatórias
├── sorted/           # chaves ordenadas
├── reverse_sorted/   # chaves em ordem decrescente
├── nearly_sorted/    # chaves quase ordenadas
└── few_uniq/         # poucas chaves distintas (lab 06)
```

No lab 04 os arquivos ficam em `input/in/<tipo>/` e se chamam `1K<tipo>.txt`,
`10K<tipo>.txt` e `100K<tipo>.txt`; nos labs 05 e 06, em `input/<tipo>/<N>.txt`.
