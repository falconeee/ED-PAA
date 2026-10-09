## Tempos de ordenação

### Chaves aleatórias (`in/unif_rand`)

| Algoritmo | 1K | 10K | 100K |
|---|---:|---:|---:|
| selection sort | 14.89 ms | 1.51 s | 196.80 s |
| insertion sort | 11.73 ms | 1.22 s | 158.91 s |
| bubble sort | 31.01 ms | 3.39 s | 463.41 s |
| shaker sort | 27.00 ms | 2.77 s | 394.12 s |

### Chaves ordenadas (`in/sorted`)

| Algoritmo | 1K | 10K | 100K |
|---|---:|---:|---:|
| selection sort | 13.65 ms | 1.42 s | 188.50 s |
| insertion sort | 0.11 ms | 1.18 ms | 15.87 ms |
| bubble sort | 0.03 ms | 0.35 ms | 4.87 ms |
| shaker sort | 0.03 ms | 0.35 ms | 4.84 ms |

### Chaves ordenadas ao contrário (`in/reverse_sorted`)

| Algoritmo | 1K | 10K | 100K |
|---|---:|---:|---:|
| selection sort | 14.30 ms | 1.52 s | 208.47 s |
| insertion sort | 21.18 ms | 2.60 s | 355.93 s |
| bubble sort | 41.85 ms | 4.69 s | 647.96 s |
| shaker sort | 44.89 ms | 4.69 s | 627.61 s |

### Chaves quase ordenadas (`in/nearly_sorted`)

| Algoritmo | 1K | 10K | 100K |
|---|---:|---:|---:|
| selection sort | 13.69 ms | 1.42 s | 201.24 s |
| insertion sort | 0.12 ms | 1.26 ms | 18.19 ms |
| bubble sort | 0.10 ms | 1.45 ms | 30.96 ms |
| shaker sort | 0.06 ms | 0.73 ms | 10.92 ms |
