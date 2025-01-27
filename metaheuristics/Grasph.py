import random
from local_search.ThreeOpt import ThreeOpt


class Grasph:
    def __init__(self, graph, start_node, alpha=0.5, max_iter=100):
        self.graph = graph
        self.start_node = start_node  # Nó inicial fornecido como parâmetro
        self.alpha = alpha  # Parâmetro de aleatoriedade para construção
        self.max_iter = max_iter  # Número máximo de iterações
        self.best_solution = None
        self.best_cost = float('inf')

    def greedy_randomized_construction(self):
        solution = [self.start_node]  # Começa a solução a partir do nó inicial
        candidate_set = set(range(self.graph.dimension))
        candidate_set.remove(self.start_node)  # Remove o nó inicial do conjunto de candidatos

        current_node = self.start_node

        while len(solution) < self.graph.dimension:
            candidate_costs = []
            for node in candidate_set:
                cost = self.graph.graph[current_node, node]  # Cálculo do custo incremental
                candidate_costs.append((node, cost))

            # Ordena candidatos com base no custo
            candidate_costs.sort(key=lambda x: x[1])
            min_cost = candidate_costs[0][1]
            max_cost = candidate_costs[-1][1]

            # Cria a RCL (Lista de Candidatos Restritos)
            rcl = [node for node, cost in candidate_costs if cost <= min_cost + self.alpha * (max_cost - min_cost)]
            selected_node = random.choice(rcl)  # Escolhe aleatoriamente da RCL
            solution.append(selected_node)
            candidate_set.remove(selected_node)
            current_node = selected_node

        # Cálculo do custo da solução construída
        cost = self.calculate_cost(solution)
        return solution

    def local_search(self, solution):
        # Realiza uma busca local usando a técnica de 3-opt
        best_solution = solution[:]
        best_cost = self.calculate_cost(solution)


        # Criação do objeto ThreeOpt
        three_opt_solver = ThreeOpt(self.graph.graph, 100, best_solution, best_cost)

        # Resolve com o 3-opt
        improved_solution, improved_cost = three_opt_solver.solve_three_opt()

        # Verifica se houve melhoria
        if improved_cost < best_cost:
            best_solution = improved_solution
            best_cost = improved_cost

        return best_solution, best_cost

    def calculate_cost(self, solution):
        # Calcula o custo total de uma solução (soma das distâncias entre os nós)
        cost = 0
        for i in range(len(solution) - 1):
            cost += self.graph.graph[solution[i], solution[i + 1]]
        cost += self.graph.graph[solution[-1], solution[0]]  # Retorna ao ponto de partida
        return cost

    def run(self):
        for iteration in range(self.max_iter):
            # Fase Construtiva
            solution = self.greedy_randomized_construction()
            # Fase Busca Local
            solution, cost = self.local_search(solution)

            # Atualiza a melhor solução encontrada
            if cost < self.best_cost:
                self.best_solution = solution
                self.best_cost = cost

        return self.best_solution, self.best_cost
