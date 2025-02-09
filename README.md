# CVRP Solver

Implementação de meta-heurísticas GRASP e Algoritmo Genético para resolução do Problema de Roteamento de Veículos Capacitados (CVRP).

## Como Executar

### GRASP
```bash
python main.py arquivo_instancia arquivo_saida GRASP-n_iteracoes-alpha
```

Exemplo:
```bash
python main.py P-n16-k8.vrp output.txt GRASP-1000-0.125
```

### Algoritmo Genético
```bash
python main.py arquivo_instancia arquivo_saida GA-taxa_elitismo-taxa_mutacao-n_geracoes
```

Exemplo:
```bash
python main.py P-n16-k8.vrp output.txt GA-0.15-0.05-10
```
