## Versão 2: qual o valor ideal de cut-off?

8. Variando o cut-off de 1 a 64 na entrada aleatória (100K e 1M), o tempo cai até
≈ 6, fica num platô entre 8 e 20 (diferenças dentro do ruído) e volta a subir a partir
de ≈ 32, quando o custo quadrático do insertion sort passa a pesar. 8 foi o melhor valor da
v4 em 1M (1.18 s, contra 1.40 s com cut-off 1) e está no platô das versões v2, v4 e v6.

## Seção 3: há alguma versão que se destacou?

Sim, nos dois sentidos.

- Negativamente: v1, v2 e v5, as versões sem mediana de 3. São quadráticas nas
  entradas ordenada, reversa e quase ordenada: o tempo quadruplica cada vez que N dobra.
  Com 10K itens ordenados, a v1 já leva 2.24 s. Extrapolando, seriam ≈ 6 h com 1M e
  ≈ 26 dias com 10M. O pivô `a[lo]` é sempre um extremo nessas entradas, então cada
  particionamento separa um único item e a recursão chega à profundidade N. O cut-off
  (v2) não ajuda, porque o problema está nas partições do topo, não nos sub-arrays
  pequenos.
- Positivamente: a mediana de 3 (v3, v4, v6). Ela transforma o pior caso em melhor
  caso: nas entradas com ordem prévia, a mediana de `lo`, meio e `hi` é a mediana exata
  do sub-array, e essas entradas ficam mais rápidas que a aleatória (8.4 s contra
  16–18 s em 10M). Na aleatória, a mediana de 3 reduz as comparações em 13% (25.7 → 22.4
  por item, perto dos 14% do slide 24).

## Seção 3: qual versão você escolheria e por quê?

A Versão 4 (top-down + cut-off + mediana de 3):

- tem o melhor tempo em todas as entradas e tamanhos, empatada com a v6 (diferenças
  abaixo de 3% em 10M, dentro do ruído);
- é O(N lg N) nos quatro tipos de entrada, e nas entradas com ordem prévia fica ainda
  mais rápida;
- as duas otimizações se completam. A mediana de 3 garante bons pivôs, mas custa 3
  `compexch` por partição. O cut-off elimina justamente os milhares de sub-arrays
  pequenos onde esse custo mais pesa (v3 → v4: 1.32 s → 1.17 s em 1M);
- é in-place e determinística. Entre as duas empatadas, é a mais simples: com a mediana de
  3, a recursão já fica rasa (≈ 2 lg N), e a pilha explícita da v6 não traz ganho. A v6
  seria a escolha se fosse preciso garantir pilha O(lg N).

## Seção 3: por que a Versão 7 não é utilizada na prática?

- Custa caro e não ganha nada nas entradas comuns. O shuffle sozinho leva ≈ 4 s em 10M
  (N chamadas de `random.randint` mais N trocas). Na entrada aleatória a v7 fica 10–30%
  mais lenta que a v4 sem nenhum benefício, porque a entrada já era aleatória.
- Destrói a ordem que já existe. Dados reais muitas vezes chegam ordenados ou quase
  ordenados. Com a mediana de 3, esse é o melhor caso, e o shuffle o transforma em caso
  médio: na entrada ordenada de 10M, 12.4 s contra 8.4 s (+47%).
- A mediana de 3 já protege contra os padrões que derrubam o quick sort ingênuo
  (ordenado, reverso, quase ordenado). As entradas que ainda derrubam a mediana de 3 são
  construídas de propósito e raras aqui.
- Não-determinismo. O tempo muda de uma execução para outra com a mesma entrada, o que
  atrapalha testes e depuração.

## Seção 4: quick sort vs. merge sort com 10M. É possível eleger o melhor?

| Entrada | quick sort v4 | merge sort v4 (lab 05) | mais rápido |
|---|---:|---:|---|
| `unif_rand` | 15.97 s | 21.58 s | quick, −26% |
| `sorted` | 8.33 s | 1.39 s | merge, 6.0× |
| `reverse_sorted` | 8.53 s | 13.73 s | quick, −38% |
| `nearly_sorted` | 8.63 s | 2.37 s | merge, 3.6× |

Não é possível eleger um melhor absoluto. O vencedor depende da entrada e dos
requisitos da aplicação:

- Sem ordem prévia (aleatória, reversa): o quick sort ganha. Ele faz mais comparações
  (21.6 contra ≈ 19.5 por item), mas move muito menos dados: ≈ 4.3 trocas por item, contra
  copiar o array inteiro para `aux` e de volta em cada nível do merge sort.
- Com ordem prévia (ordenada, quase ordenada): o merge sort ganha por 4–6×. Com merge
  skip, ele fica quase linear (≈ N comparações). O quick sort continua fazendo ~N lg N
  comparações para particionar, mesmo trocando quase nada.
- Além do tempo: o merge sort é estável, tem pior caso N lg N garantido e usa
  N de memória extra. O quick sort é in-place, não é estável e tem pior caso
  quadrático (raro com mediana de 3, mas possível).

A escolha depende dos requisitos.

## Seção 5: Versão 8 vs. melhor versão na entrada aleatória com 10M

| Entrada | v8 (3-way de Dijkstra) | v4 |
|---|---:|---:|
| `unif_rand/10000000.txt` | 30.72 s | 15.95 s |

A v4 foi melhor, ≈ 1.9× mais rápida. Com chaves praticamente todas distintas, a faixa
de chaves iguais ao pivô tem um único item, e o 3-way não tem nada a agrupar. Sobra só o
custo extra do laço:

- 38 comparações por item contra 21.6 da v4. Todo item maior que o pivô custa dois
  `less` (`a[i] < v` e depois `v < a[i]`), e a v8 não tem mediana de 3 para escolher um
  pivô melhor.
- 24 trocas por item contra 4.3. O esquema de Dijkstra troca *todo* item diferente do
  pivô, enquanto o particionamento da v4 só troca os pares que estão do lado errado. É o
  defeito que o Bentley-McIlroy 3-way corrige (slide 39).
- A v8 também não tem cut-off para os sub-arrays pequenos.

## Seção 5: e na entrada `few_uniq/10M_const_keys_unif_rand.txt`? O que mudou?

| Entrada | v8 (3-way de Dijkstra) | v4 |
|---|---:|---:|
| `few_uniq/10M_const_keys_unif_rand.txt` | 5.77 s | 11.23 s |

A situação se inverteu: a v8 ficou ≈ 1.9× mais rápida. O que mudou foi o número de
chaves distintas, só 100 (0 a 99), cada uma repetida ≈ 100K vezes:

- Cada particionamento 3-way coloca todas as ≈ 100K cópias do pivô na posição final de
  uma vez, e elas não são tocadas. A recursão só continua nas chaves menores e
  maiores e termina em ≈ lg 100 ≈ 7 níveis, em vez de lg N ≈ 23.
- As comparações caem de 38 para 12.2 por item. O custo passa a ser proporcional a
  N · lg(nº de chaves distintas), e não a N lg N.
- A v4 não fica quadrática, porque os scans param em chaves iguais e um
  sub-array de chaves iguais é dividido ao meio. Ela até fica mais rápida que na
  aleatória. Mas continua particionando, e trocando entre si, sub-arrays inteiros de chaves iguais até o cut-off, 
  por isso leva o dobro do tempo da v8.

O 3-way só compensa com muitas chaves duplicadas.