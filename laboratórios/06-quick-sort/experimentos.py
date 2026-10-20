import subprocess
import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
CLIENTE_MERGE = DIR.parent / "05-lab-mergesort" / "cliente.py"
TIPOS = ["unif_rand", "sorted", "reverse_sorted", "nearly_sorted"]
TAMANHOS = [100000, 1000000, 10000000]
VERSOES = ["v1", "v2", "v3", "v4", "v5", "v6", "v7"]
COM_CUTOFF = ["v2", "v4", "v6"]  # versões que usam o valor de cut-off (a v7 usa o da v4)
CUTOFFS = [1, 2, 4, 6, 8, 10, 12, 16, 20, 24, 32, 48, 64]  # Valores de cut-off a testar
TAMANHOS_CUTOFF = [100000, 1000000]
MELHOR_QUICK = "v4"  # melhor versão obtida nos experimentos (seção "versoes")
MELHOR_MERGE = "v4"  # melhor versão do Laboratório de Merge Sort (cut-off 8)
LIMITE = 20  # segundos por 100K itens; acima disso interrompi a execução para não demorar demais
TAMANHOS_QUADRATICO = [2500, 5000, 10000]  # usados quando a execução estoura o limite


class Estouro(Exception):
    pass


def medir(versao, arquivo, n, cutoff=None, cliente=DIR / "cliente.py"):
    cmd = [sys.executable, str(cliente), str(n), versao]
    if cutoff is not None:
        cmd += ["--cutoff", str(cutoff)]
    with open(DIR / "input" / arquivo) as entrada:
        try:
            r = subprocess.run(cmd, stdin=entrada, stdout=subprocess.DEVNULL,
                               stderr=subprocess.PIPE, text=True, check=True,
                               timeout=LIMITE * max(n, 100000) / 100000)
        except subprocess.TimeoutExpired:
            raise Estouro
    # última linha do stderr: "quick sort v1, N = 100000: 0.131566 s"
    return float(r.stderr.strip().rsplit(":", 1)[1].split()[0])


def fmt(t):
    return f"{t * 1000:.1f} ms" if t < 1 else f"{t:.2f} s"


def titulo(texto):
    print(f"\n=== {texto} ===", flush=True)


def exp_cutoff():
    titulo("Escolha do cut-off (unif_rand)")
    for v in COM_CUTOFF:
        for c in CUTOFFS:
            for n in TAMANHOS_CUTOFF:
                t = medir(v, f"unif_rand/{n}.txt", n, c)
                print(f"{v} cutoff = {c:>2} N = {n:>8}: {fmt(t):>10}", flush=True)


# Mede N = 2500, 5000 e 10000 (início do arquivo de 100K): se o tempo
# quadruplica quando N dobra, o caso é quadrático
def quadratico(v, tipo):
    anterior = None
    for n in TAMANHOS_QUADRATICO:
        t = medir(v, f"{tipo}/100000.txt", n)
        razao = f"  (x{t / anterior:.1f})" if anterior else ""
        print(f"    {v} {tipo:<14} N = {n:>8}: {fmt(t):>10}{razao}", flush=True)
        anterior = t


def exp_versoes():
    titulo(f"Versões 1 a 7 (limite de {LIMITE} s por 100K itens)")
    for tipo in TIPOS:
        for v in VERSOES:
            for n in TAMANHOS:
                try:
                    t = medir(v, f"{tipo}/{n}.txt", n)
                except Estouro:
                    print(f"{v} {tipo:<14} N = {n:>8}: estourou o limite; "
                          f"N maiores pulados", flush=True)
                    quadratico(v, tipo)
                    break
                print(f"{v} {tipo:<14} N = {n:>8}: {fmt(t):>10}", flush=True)


def exp_merge():
    titulo(f"Quick sort {MELHOR_QUICK} vs. merge sort {MELHOR_MERGE} (N = 10M)")
    n = 10000000
    for tipo in TIPOS:
        tq = medir(MELHOR_QUICK, f"{tipo}/{n}.txt", n)
        tm = medir(MELHOR_MERGE, f"{tipo}/{n}.txt", n, cliente=CLIENTE_MERGE)
        print(f"{tipo:<14} quick {fmt(tq):>10}   merge {fmt(tm):>10}", flush=True)


def exp_3way():
    titulo(f"Versão 8 (3-way de Dijkstra) vs. {MELHOR_QUICK} (N = 10M)")
    n = 10000000
    for arquivo in [f"unif_rand/{n}.txt", "few_uniq/10M_const_keys_unif_rand.txt"]:
        for v in ["v8", MELHOR_QUICK]:
            t = medir(v, arquivo, n)
            print(f"{v} {arquivo:<38}: {fmt(t):>10}", flush=True)


EXPERIMENTOS = {
    "cutoff": exp_cutoff,
    "versoes": exp_versoes,
    "merge": exp_merge,
    "3way": exp_3way,
}

nomes = sys.argv[1:] or list(EXPERIMENTOS)
for nome in nomes:
    if nome not in EXPERIMENTOS:
        sys.exit(f"experimento desconhecido: {nome} (opções: {', '.join(EXPERIMENTOS)})")
for nome in nomes:
    EXPERIMENTOS[nome]()
