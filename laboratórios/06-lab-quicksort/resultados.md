## Quick sort: tempos de ordenação

Ambiente: Apple M4, Python 3.12.3. Cada tempo é uma execução do `cliente.py` e mede
só a ordenação (`time.perf_counter` em volta de `sort(a, 0, N-1)`), sem a leitura da
entrada. Repetindo medições, o ruído fica em torno de ±5% (a v4 na `unif_rand` de 10M
deu 18.74 s, 15.97 s e 15.95 s em três execuções do mesmo script).

Para reproduzir (tudo leva ≈ 12 min):

```
python3 experimentos.py                      # todas as seções abaixo
python3 experimentos.py versoes 3way         # só algumas seções (cutoff, versoes, merge, 3way)
python3 cliente.py 1000000 v4 < input/unif_rand/1000000.txt > /dev/null
```

| Versão | Descrição |
|---|---|
| v1 | top-down recursivo, sem otimizações (pivô `a[lo]`) |
| v2 | top-down + cut-off para insertion sort |
| v3 | top-down + mediana de 3 |
| v4 | top-down + cut-off + mediana de 3 |
| v5 | não-recursivo (pilha explícita numa `list`, slide 25), sem otimizações |
| v6 | não-recursivo + cut-off + mediana de 3 |
| v7 | v4 + embaralhamento (shuffle) da entrada |
| v8 | top-down com particionamento 3-way de Dijkstra |

Nenhuma versão embaralha a entrada, exceto a v7.

Dois detalhes de implementação:

- O `partition` do slide 10 não avança `i` e `j` depois da troca. Com chaves iguais ao
  pivô (`[5, 5, 5]`), os dois scans param no mesmo lugar para sempre. Corrigi
  avançando os índices antes de cada scan, como no Sedgewick.
- A `median_of_3` usa as posições `lo`, meio e `hi` (sem shuffle não há "3 chaves
  aleatórias") e ordena essas 3 chaves no lugar antes de devolver o índice da mediana.
  A primeira versão que fiz só devolvia o índice, sem mexer nas chaves, e era
  quadrática na entrada reversa (v3 com 100K: 59 s, ≈ N/8 comparações por item).
  Depois do 1º particionamento, o sub-array esquerdo vira `[max, 1, 2, …, max-1]` e a
  amostra (máx., meio, 2º máx.) escolhe sempre o 2º maior como pivô. Com as 3 chaves
  ordenadas no lugar, esse padrão some.

### Escolha do cut-off (`unif_rand`)

| cut-off | v2, 100K | v2, 1M | v4, 100K | v4, 1M | v6, 100K | v6, 1M |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 107.5 ms | 1.34 s | 116.1 ms | 1.40 s | 116.6 ms | 1.44 s |
| 2 | 104.9 ms | 1.30 s | 106.2 ms | 1.29 s | 107.0 ms | 1.31 s |
| 4 | 103.2 ms | 1.29 s | 100.6 ms | 1.24 s | 100.9 ms | 1.25 s |
| 6 | 100.9 ms | 1.26 s | 97.6 ms | 1.21 s | 98.0 ms | 1.22 s |
| 8 | 97.0 ms | 1.27 s | 95.4 ms | 1.18 s | 97.0 ms | 1.20 s |
| 10 | 100.5 ms | 1.25 s | 96.1 ms | 1.19 s | 96.3 ms | 1.21 s |
| 12 | 105.7 ms | 1.33 s | 94.9 ms | 1.21 s | 96.3 ms | 1.43 s |
| 16 | 101.3 ms | 1.28 s | 95.6 ms | 1.19 s | 95.9 ms | 1.19 s |
| 20 | 100.5 ms | 1.25 s | 96.9 ms | 1.19 s | 97.3 ms | 1.22 s |
| 24 | 101.7 ms | 1.29 s | 98.0 ms | 1.21 s | 98.7 ms | 1.29 s |
| 32 | 106.8 ms | 1.30 s | 102.0 ms | 1.25 s | 102.3 ms | 1.26 s |
| 48 | 116.3 ms | 1.41 s | 110.3 ms | 1.35 s | 135.2 ms | 1.50 s |
| 64 | 128.0 ms | 1.54 s | 121.5 ms | 1.49 s | 126.0 ms | 1.48 s |

O tempo cai até cut-off ≈ 6, fica num platô entre 8 e 20 (as diferenças ali estão
dentro do ruído) e sobe a partir de ≈ 32, quando o custo quadrático do insertion sort
começa a pesar. O 1.43 s da v6 com cut-off 12 em 1M fica fora da curva e é ruído: com
100K, o mesmo cut-off deu 96.3 ms. Escolhi `CUTOFF = 8` (constante em `sorts.py`, sobrescrita por
`--cutoff`): é o melhor valor da v4 em 1M e fica no platô das três versões. É o mesmo
valor do merge sort e está perto do ≈ 10 do slide 23.

Assim como no merge sort, cut-off = 1 é mais lento que não ter cut-off (v2 com cut-off 1:
1.34 s, v1: 1.24 s). Cada folha da recursão chama `insertion_sort` à toa.

### Tempos

"quadrático" = passou do limite de 20 s já com 100K. Nesses casos o script mede
N = 2500, 5000 e 10000 (início do arquivo de 100K), e o tempo quadruplica cada vez
que N dobra (razões entre 3.8 e 4.2).

N = 10M

| Versão | `unif_rand` | `sorted` | `reverse_sorted` | `nearly_sorted` |
|---|---:|---:|---:|---:|
| v1 | 16.65 s | quadrático | quadrático | quadrático |
| v2 | 16.44 s | quadrático | quadrático | quadrático |
| v3 | 17.46 s | 9.78 s | 10.40 s | 10.35 s |
| v4 | 16.0 – 18.7 s | 8.42 s | 8.76 s | 8.63 s |
| v5 | 18.65 s | quadrático | quadrático | quadrático |
| v6 | 15.96 s | 8.38 s | 8.56 s | 8.69 s |
| v7 | 20.79 s | 12.39 s | 12.67 s | 13.16 s |

Em 10M, v4 e v6 ficam a menos de 3% uma da outra em todas as entradas, ou seja, dentro do
ruído. Na `unif_rand`, v1, v2, v4 e v6 ficam todas entre 16 e 19 s, e uma execução só
não basta para ordená-las.

N = 1M

| Versão | `unif_rand` | `sorted` | `reverse_sorted` | `nearly_sorted` |
|---|---:|---:|---:|---:|
| v1 | 1.24 s | quadrático | quadrático | quadrático |
| v2 | 1.34 s | quadrático | quadrático | quadrático |
| v3 | 1.32 s | 865.4 ms | 856.2 ms | 859.8 ms |
| v4 | 1.17 s | 708.1 ms | 796.3 ms | 736.7 ms |
| v5 | 1.33 s | quadrático | quadrático | quadrático |
| v6 | 1.25 s | 711.6 ms | 741.9 ms | 743.8 ms |
| v7 | 1.51 s | 1.05 s | 1.04 s | 1.03 s |

N = 100K

| Versão | `unif_rand` | `sorted` | `reverse_sorted` | `nearly_sorted` |
|---|---:|---:|---:|---:|
| v1 | 98.9 ms | quadrático | quadrático | quadrático |
| v2 | 98.2 ms | quadrático | quadrático | quadrático |
| v3 | 106.9 ms | 81.7 ms | 84.6 ms | 81.6 ms |
| v4 | 95.5 ms | 62.3 ms | 67.4 ms | 65.4 ms |
| v5 | 106.9 ms | quadrático | quadrático | quadrático |
| v6 | 96.2 ms | 62.8 ms | 64.6 ms | 65.5 ms |
| v7 | 123.1 ms | 92.4 ms | 92.5 ms | 90.6 ms |

Casos quadráticos medidos em N pequeno (`sorted`):

| Versão | N = 2500 | N = 5000 | N = 10000 |
|---|---:|---:|---:|
| v1 | 139.0 ms | 567.6 ms (×4.1) | 2.24 s (×3.9) |
| v2 | 144.6 ms | 575.1 ms (×4.0) | 2.24 s (×3.9) |
| v5 | 94.7 ms | 378.7 ms (×4.0) | 1.53 s (×4.0) |

Extrapolando a v1 (×100 a cada ×10 em N): ≈ 3.7 min com 100K, ≈ 6 h com 1M e
≈ 26 dias com 10M. Contra 8.4 s da v4.

### Comparações e trocas por item (N = 1M)

Chamadas de `less` e `exch` feitas em `sorts.py`. As comparações dentro de `compexch`
(passada de sentinela do insertion sort e mediana de 3) não entram. Para referência,
lg(10⁶) ≈ 19.9 e 1.39 lg N ≈ 27.7.

| Versão | `unif_rand` less | `unif_rand` exch | `sorted` less | `sorted` exch | `few_uniq` less | `few_uniq` exch |
|---|---:|---:|---:|---:|---:|---:|
| v1 | 25.73 | 4.68 | — | — | 21.18 | 7.59 |
| v3 | 22.43 | 5.18 | 19.00 | 1.05 | 19.90 | 8.25 |
| v4 | 21.56 | 4.30 | 17.61 | 0.26 | 18.76 | 6.97 |
| v7 | 21.56 | 5.30 | 17.61 | 1.26 | 18.76 | 7.97 |
| v8 | 37.99 | 24.24 | — | — | 12.20 | 6.95 |

(`few_uniq` aqui = primeiros 1M itens de `10M_const_keys_unif_rand.txt`, chaves de 0 a 99.
As trocas da v7 incluem as N trocas do shuffle.)

## Análise das 7 versões

v1 (sem otimizações). Na entrada aleatória vai bem: 1.24 s em 1M, com 25.7
comparações por item, pouco abaixo de 1.39 N lg N. Nas outras três entradas é
quadrática. Com pivô `a[lo]`, a entrada ordenada (e a reversa, depois do primeiro
passo) põe o pivô sempre no extremo. Cada particionamento tira um único item, a
recursão chega à profundidade N (o cliente precisa aumentar o `recursionlimit` do Python)
e o custo vai para ~½N². A quase ordenada também cai nisso, porque o primeiro item de cada
sub-array quase sempre é um dos menores. É exatamente o caso que o shuffle do slide 11
existe para evitar.

Cut-off (v1 → v2). Sozinho, o ganho é pequeno: na aleatória a v2 empata com a v1
(1.24–1.34 s em 1M, dentro do ruído). Comparado com a mesma versão com cut-off = 1, o
ganho é ≈ 6%. Como no merge sort, o que melhora é tirar as camadas de baixo da recursão,
não fazer menos comparações. O cut-off não resolve o caso quadrático: o problema está
nas partições do topo, não nos sub-arrays pequenos.

Mediana de 3 (v1 → v3). É a otimização que mais muda o resultado. Nas entradas
ordenada, reversa e quase ordenada, a mediana de `lo`, meio e `hi` é a mediana *exata* do
sub-array, e o quick sort entra no melhor caso: partições ao meio e quase nenhuma
troca (1.05 por item na ordenada). Essas entradas ficam mais rápidas que a aleatória
(9.8 s vs 17.5 s em 10M). Na aleatória, a v3 faz 13% menos comparações que a v1
(22.4 vs 25.7 por item, perto dos 14% do slide 24) e 11% mais trocas. Mesmo assim fica
≈ 6% *mais lenta* que a v1 (1.32 s vs 1.24 s em 1M): em Python, as 3 chamadas de
`compexch` por partição custam mais que as comparações economizadas, principalmente nos
milhares de sub-arrays pequenos.

Cut-off + mediana de 3 (v4). As duas otimizações se completam. O cut-off elimina
justamente os sub-arrays pequenos, onde a mediana de 3 mais pesa (v3 → v4: 1.32 s →
1.17 s em 1M, −11%). A mediana de 3 garante partições boas nas entradas com ordem prévia.
A v4 e a v6 (as duas com cut-off e mediana de 3) dividem os melhores tempos em todas
as entradas e tamanhos, com diferenças dentro do ruído.

Recursivo vs não-recursivo (v1–v4 vs v5–v6). Com a pilha numa `list` do Python, a
versão não-recursiva custa pouco mais que a recursiva: v5 vs v1 em 1M = 1.33 s vs 1.24 s
(+7%), e a v6 empata com a v4. A vantagem da pilha é estrutural: empilhando o
sub-array maior e processando o menor primeiro, ela nunca passa de lg N pares, enquanto a
v1 chega à profundidade N nos casos ruins e só funciona porque o cliente aumenta o limite
de recursão. Mas isso não muda a complexidade: a v5 continua quadrática nas mesmas
entradas que a v1. Com mediana de 3, a recursão já fica rasa (≈ 2 lg N), e a pilha não
traz ganho, embora também não atrapalhe.

Shuffle (v4 → v7). O shuffle sozinho custa ≈ 4.1 s em 10M (uma chamada de
`random.randint` e uma troca por item). Na aleatória, a v7 fica 10–30% mais lenta que a
v4 sem nenhum ganho, já que a entrada já era aleatória. Nas entradas ordenadas, perde
≈ 47% (12.4 s vs 8.4 s em 10M): o shuffle destrói justamente a ordem que deixava a
mediana de 3 no melhor caso e transforma o melhor caso em caso médio.

### Há alguma que se destacou? Qual eu escolheria?

As versões sem mediana de 3 (v1, v2, v5) se destacam negativamente: ficam inviáveis
(quadráticas) em 3 dos 4 tipos de entrada, mesmo com só 100K itens. A mediana de 3 é
a otimização que mais importa: transforma o pior caso em melhor caso.

Eu escolheria a Versão 4 (top-down + cut-off + mediana de 3):

- tem o melhor tempo, empatada com a v6, em todas as entradas e tamanhos;
- é O(N lg N) nas 4 entradas, e nas que já têm ordem fica ainda mais rápida que na
  aleatória;
- é in-place e não depende de gerador aleatório;
- entre as duas empatadas, a v4 é a mais simples, e a recursão fica com profundidade
  ≈ 2 lg N nas entradas testadas. A v6 seria a escolha se fosse preciso *garantir* pilha
  O(lg N) mesmo em entradas adversárias, já que ela custa o mesmo.

### Por que a Versão 7 não é usada na prática?

- Custa caro e não traz ganho nas entradas comuns. Gerar N números aleatórios e fazer
  N trocas é uma passada extra inteira sobre o array (≈ 4 s de 16–20 s em 10M). Na
  entrada aleatória, esse custo não compra nada.
- Joga fora a ordem que já existe. Dados reais muitas vezes já vêm ordenados ou quase
  ordenados. Com a mediana de 3, esse é o melhor caso, e o shuffle o converte em caso
  médio (+47% de tempo).
- A mediana de 3 já protege contra os padrões comuns (ordenado, reverso, quase
  ordenado), que são exatamente os que tornam o quick sort ingênuo quadrático. Entradas que
  derrubam a mediana de 3 existem (como o padrão `[max, 1, 2, …]` visto acima), mas são
  construídas e raras.
- Não-determinismo. O tempo varia entre execuções da mesma entrada, o que dificulta
  testes e depuração.
- Quando se quer garantia contra pior caso, existem soluções mais baratas: escolher o pivô
  aleatoriamente só em cada partição (slide 14) ou o *introsort*, que troca para heap
  sort quando a recursão fica funda demais (usado no `std::sort` do C++).

## Quick sort vs. merge sort (N = 10M)

Melhor quick sort (v4, cut-off 8) contra o melhor merge sort do lab anterior (v4: top-down
+ cut-off 8 + merge skip), rodados em sequência pelo mesmo script.

| Entrada | quick sort v4 | merge sort v4 | mais rápido |
|---|---:|---:|---|
| `unif_rand` | 15.97 s | 21.58 s | quick, −26% |
| `sorted` | 8.33 s | 1.39 s | merge, 6.0× |
| `reverse_sorted` | 8.53 s | 13.73 s | quick, −38% |
| `nearly_sorted` | 8.63 s | 2.37 s | merge, 3.6× |

Não dá para eleger um vencedor absoluto. Depende da entrada e do que a aplicação
precisa:

- Em entradas sem ordem prévia (aleatória e reversa), o quick sort ganha com folga,
  mesmo fazendo mais comparações (21.6 vs ≈ 19.5 por item). Ele move bem menos dados: ≈ 4.3
  trocas por item, contra a cópia de todos os itens para `aux` e de volta em cada nível
  do merge sort. É a vantagem citada no slide 21.
- Em entradas ordenadas ou quase ordenadas, o merge sort com merge skip fica quase
  linear (≈ N comparações) e ganha por 4–6×. O quick sort continua fazendo ~N lg N
  comparações para particionar, mesmo sem trocar quase nada.
- Fora o tempo: o merge sort é estável e tem pior caso N lg N garantido, mas usa
  N de memória extra. O quick sort é in-place, mas não é estável e tem pior caso
  quadrático (raro com mediana de 3, mas possível).

Na prática, a escolha segue esses critérios. É por isso que o Java usa dual-pivot quick
sort para tipos primitivos e Tim sort (variante adaptativa do merge sort) para objetos
(slide 42). O `sorted` do próprio Python também é Tim sort.

## Dijkstra 3-way partitioning (Versão 8, N = 10M)

| Entrada | v8 (3-way) | v4 | mais rápido |
|---|---:|---:|---|
| `unif_rand/10000000.txt` | 30.72 s | 15.95 s | v4, 1.9× |
| `few_uniq/10M_const_keys_unif_rand.txt` | 5.77 s | 11.23 s | v8, 1.9× |

Entrada aleatória: a v4 ganha. Com chaves (quase todas) distintas, a faixa de chaves
iguais ao pivô tem um único item, e o 3-way vira um quick sort comum com um laço mais
caro:

- 38 comparações por item contra 21.6 da v4. Cada item maior que o pivô custa dois
  `less` (`a[i] < v` e `v < a[i]`), e a v8 não tem mediana de 3 para melhorar o pivô.
- 24 trocas por item contra 4.3. O esquema de Dijkstra troca *todo* item diferente do
  pivô (os menores com `lt`, os maiores com `gt`). O particionamento de Sedgewick só troca
  pares que estão do lado errado. É o problema que o Bentley-McIlroy 3-way resolve
  (slide 39).
- Também não tem cut-off.

Entrada com poucas chaves distintas (0 a 99): a v8 ganha. Cada particionamento põe
todas as ≈ 100K cópias do pivô na posição final de uma vez, e elas nunca mais são
tocadas. Com só 100 chaves distintas, a recursão termina em ≈ lg 100 ≈ 7 níveis em vez de
lg N ≈ 23. As comparações caem de 37.99 para 12.20 por item, perto do limite inferior
lg(N! / ∏ xᵢ!) ≈ N lg 100 ≈ 6.6 N do slide 37. O custo passa a ser proporcional a
N · lg(nº de chaves distintas), e não a N lg N.

A v4 não fica quadrática nessa entrada: como os scans param em chaves iguais
(slide 31), um sub-array de chaves iguais é dividido ao meio. Ela até fica mais rápida
que na aleatória (11.2 s vs 16.0 s). Mas continua particionando sub-arrays inteiros de
chaves iguais, trocando-as entre si sem necessidade, até o cut-off. Por isso precisa do
dobro do tempo da v8.

Resumo: o 3-way só compensa quando há muitas chaves duplicadas. É por isso que os
system sorts usam variantes que custam pouco quando as chaves são distintas
(Bentley-McIlroy, dual-pivot com fallback para Dijkstra quando p1 = p2, slides 39–40),
para ficar com o melhor dos dois casos.
