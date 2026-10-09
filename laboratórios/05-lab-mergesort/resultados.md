## Merge sort: tempos de ordenação

Ambiente: Apple M4, Python 3.12.3. Cada tempo é a **mediana de 5 execuções** do
`cliente.py` e mede só a ordenação (`time.perf_counter` em volta de `sort(a, 0, N-1)`),
sem a leitura da entrada. As entradas de 10M citadas no roteiro não estão em
`input/`, por isso medi só 100K e 1M.

Para reproduzir:

```
python3 cliente.py 1000000 v4 < input/unif_rand/1000000.txt > /dev/null
python3 experimentos.py cutoff v2 unif_rand   # varredura do cut-off
python3 experimentos.py versoes               # tabelas abaixo
```

| Versão | Descrição |
|---|---|
| v1 | top-down recursivo, sem otimizações |
| v2 | top-down + cut-off para insertion sort |
| v3 | top-down + merge skip |
| v4 | top-down + cut-off + merge skip |
| v5 | bottom-up, sem otimizações |
| v6 | bottom-up + cut-off (blocos de `CUTOFF` itens ordenados com insertion sort antes das passadas de merge) |
| v7 | bottom-up + cut-off + merge skip |

### Escolha do cut-off (`unif_rand`)

| cut-off | v2, 100K | v2, 1M | v6, 100K | v6, 1M |
|---:|---:|---:|---:|---:|
| 1 | 145.7 ms | 1.85 s | 148.3 ms | 1.81 s |
| 2 | 137.0 ms | 1.67 s | 132.0 ms | 1.62 s |
| 3 | 124.3 ms | 1.58 s | 130.0 ms | 1.62 s |
| 4 | 123.3 ms | 1.51 s | 123.3 ms | 1.54 s |
| 5 | 122.9 ms | 1.51 s | 121.6 ms | 1.56 s |
| 6 | 119.7 ms | 1.51 s | 124.2 ms | 1.56 s |
| 7 | 119.7 ms | 1.50 s | 117.7 ms | 1.59 s |
| **8** | **118.9 ms** | **1.49 s** | **118.7 ms** | **1.50 s** |
| 10 | 118.8 ms | 1.49 s | 118.2 ms | 1.53 s |
| 12 | 117.9 ms | 1.49 s | 123.2 ms | 1.55 s |
| 14 | 119.2 ms | 1.54 s | 117.9 ms | 1.59 s |
| 16 | 120.5 ms | 1.56 s | 121.4 ms | 1.53 s |
| 20 | 120.1 ms | 1.59 s | 122.9 ms | 1.57 s |
| 24 | 131.9 ms | 1.50 s | 128.9 ms | 1.61 s |
| 32 | 125.3 ms | 1.59 s | 132.7 ms | 1.64 s |
| 48 | 127.9 ms | 1.62 s | 151.2 ms | 1.85 s |
| 64 | 147.6 ms | 1.91 s | 163.1 ms | 1.95 s |

O tempo cai rápido até cut-off ≈ 6, fica num platô entre **8 e 12** (as diferenças
ali são menores que o ruído da medição) e volta a subir a partir de ≈ 24, quando o
custo quadrático do insertion sort passa a dominar. Escolhi **`CUTOFF = 8`**
(constante em `sorts.py`, sobrescrita por `--cutoff`): é o melhor valor comum às
versões top-down e bottom-up em 1M, e fica perto do ≈ 10 sugerido no slide 15.

Observação: cut-off = 1 é *mais lento* que a v1 (1.85 s vs 1.62 s), embora ordene do
mesmo jeito. Com cut-off 1, cada folha da recursão chama `insertion_sort` à toa, o que
soma N chamadas de função a mais.

### Tempos, N = 1M

| Versão | `unif_rand` | `sorted` | `reverse_sorted` | `nearly_sorted` |
|---|---:|---:|---:|---:|
| v1 | 1.62 s | 1.23 s | 1.26 s | 1.25 s |
| v2 | **1.48 s** | 1.03 s | **1.20 s** | 1.03 s |
| v3 | 1.59 s | **103.8 ms** | 1.29 s | **197.8 ms** |
| v4 | **1.48 s** | 131.3 ms | **1.20 s** | 215.7 ms |
| v5 | 1.65 s | 1.25 s | 1.26 s | 1.25 s |
| v6 | 1.51 s | 1.04 s | 1.21 s | 1.05 s |
| v7 | 1.50 s | 134.4 ms | 1.22 s | 214.7 ms |

### Tempos, N = 100K

| Versão | `unif_rand` | `sorted` | `reverse_sorted` | `nearly_sorted` |
|---|---:|---:|---:|---:|
| v1 | 132.6 ms | 106.7 ms | 107.9 ms | 107.2 ms |
| v2 | **118.0 ms** | 87.6 ms | **101.0 ms** | 89.2 ms |
| v3 | 128.1 ms | **10.3 ms** | 110.9 ms | **17.6 ms** |
| v4 | 119.1 ms | 13.4 ms | 101.5 ms | 20.0 ms |
| v5 | 133.8 ms | 108.2 ms | 109.4 ms | 108.4 ms |
| v6 | 119.9 ms | 89.6 ms | 104.9 ms | 87.9 ms |
| v7 | 119.4 ms | 12.8 ms | 104.2 ms | 19.4 ms |

### Comparações por item (chamadas de `less` / N, N = 1M, cut-off 8)

Para referência, lg(10⁶) ≈ 19.9.

| Versão | `unif_rand` | `sorted` | `reverse_sorted` | `nearly_sorted` |
|---|---:|---:|---:|---:|
| v1 | 18.67 | 10.07 | 9.89 | 10.13 |
| v2 | 19.38 | 10.15 | 12.53 | 10.23 |
| v3 | 19.32 | 1.00 | 10.88 | 1.88 |
| v4 | 19.51 | 1.74 | 12.66 | 2.53 |
| v5 | 18.72 | 10.10 | 9.89 | 10.17 |
| v6 | 19.47 | 10.22 | 12.63 | 10.30 |
| v7 | 19.59 | 1.75 | 12.76 | 2.55 |

## Análise

**Cut-off (v1 → v2).** Reduz o tempo em todas as entradas: cerca de 9% na
aleatória, 5% na reversa e 16 a 18% na ordenada e na quase ordenada. O ganho *não* vem
de fazer menos comparações. A v2 faz até mais (19.38 contra 18.67 por item na
aleatória, 12.5 contra 9.9 na reversa, onde cada bloco é o pior caso do insertion
sort). O ganho vem de eliminar as camadas de baixo da recursão: são muitas chamadas de
função e muitas cópias para `aux` para mover pouquíssimos itens, e o laço interno do
insertion sort é mais barato por item do que o merge.

**Merge skip (v1 → v3).** É a otimização que mais se destaca, mas só em entradas com
ordem prévia. Na **ordenada**, a v3 faz exatamente N − 1 comparações (1.00 por item):
todo merge é pulado e o algoritmo fica **linear**, 12× mais rápido que a v1 (1.23 s →
104 ms). Na **quase ordenada**, fica 6× mais rápida (1.25 s → 198 ms). Na aleatória o
teste quase nunca dispara e o ganho é desprezível (≈ 2%). Na **reversa** ele nunca
dispara: custa uma comparação extra por merge (9.89 → 10.88 por item) e a v3 fica ≈ 2%
*mais lenta* que a v1. Ou seja, o custo no pior caso é pequeno e o ganho no melhor caso
é grande.

**Cut-off + merge skip (v4).** Junta os dois ganhos onde eles não competem:
empata com a v2 na aleatória e na reversa (melhores tempos) e herda o comportamento
quase linear da v3 nas entradas ordenadas. Há um efeito curioso: na ordenada e na
quase ordenada, a v4 é **mais lenta que a v3** (131 ms vs 104 ms). Com merge skip,
as camadas de baixo da recursão já custam só uma comparação por nó. O cut-off as troca
por um insertion sort que, por causa da passada de sentinela (`compexch` de `hi` até
`lo`), faz ≈ 1.6 comparações por item mesmo em blocos já ordenados (1.74 vs 1.00 por
item no total). Aqui o cut-off adiciona trabalho em vez de remover.

**Top-down vs bottom-up (v1–v4 vs v5–v7).** Na prática, empatam: as diferenças
entre v1/v5, v2/v6 e v4/v7 ficam em até ≈ 2%, dentro do ruído, com uma leve
vantagem do top-down na aleatória (1.62 s vs 1.65 s sem otimizações). As contagens de
comparações também são praticamente iguais. Em CPython, o custo dominante está nas
operações por item dentro do `merge`, que são as mesmas nas duas versões. O overhead
da recursão (≈ 2N chamadas) é pequeno perto das ≈ N lg N operações do merge. Por isso
não aparece aqui a desvantagem do bottom-up mencionada no slide 19. As mesmas
otimizações funcionam igualmente no bottom-up: o cut-off da v6 tem o mesmo platô
ótimo, e a v7 se comporta como a v4.

**Estabilidade.** As 7 versões são estáveis com qualquer cut-off (verificado em
testes com chaves repetidas): o merge pega da metade esquerda em caso de empate, e o
insertion sort do lab anterior só troca com `less` estrito.

### Há alguma que se destacou? Qual eu escolheria?

As versões com **merge skip (v3, v4, v7)** se destacam muito nas entradas ordenadas
e quase ordenadas: são de 6 a 12× mais rápidas, e o custo cai de ~N lg N para ~N. Nas
entradas sem ordem prévia, quem se destaca é o **cut-off**, com ganho modesto mas
consistente de 5 a 9%.

Eu escolheria a **Versão 4** (top-down + cut-off + merge skip):

- tem o melhor tempo (empatado) nas entradas aleatória e reversa, onde o merge skip
  não ajuda e o cut-off faz diferença;
- nas entradas ordenadas e quase ordenadas fica a ≈ 20–30 ms da v3 em 1M, mas ainda
  6 a 9× mais rápida que a v1. Já a v3 perde ≈ 7% para a v4 nos casos aleatório e
  reverso, que são os mais comuns;
- o pior caso continua O(N lg N), e o merge skip custa no máximo uma comparação por
  merge;
- a v7 tem desempenho equivalente, mas a v4 tem código mais simples e corresponde à
  implementação clássica do slide 16. A profundidade da recursão (lg N ≈ 20) não é
  problema, então não há motivo para preferir o bottom-up.

Se a aplicação souber que as entradas são quase sempre ordenadas, a v3 seria melhor. A
ideia de explorar a ordem já existente na entrada leva ao merge sort natural e ao Tim
sort (slides 21–22).
