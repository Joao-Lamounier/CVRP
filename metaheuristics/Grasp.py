import random

from local_search.ThreeOpt import ThreeOpt


class Grasp:
    def __init__(self, graph, start_node, alpha=0.5, max_iter=100):
        self.graph = graph
        self.depot = start_node
        self.alpha = alpha
        self.max_iter = max_iter
        self.best_routes = None
        self.best_cost = float('inf')
        self.vehicle_capacity = graph.capacity
        self.demands = graph.demands
        self.max_vehicles = graph.vehicles

    def decode_solution(self, solution):
        routes = []
        route_capacities = {}  # Dicionário para armazenar a capacidade restante de cada rota
        for client in solution:

            demand = self.graph.demands[client]
            inserted = False

            # Tentar inserir o cliente em uma rota existente
            for i, route in enumerate(routes):
                if route_capacities[i] >= demand:
                    route.append(client)
                    route_capacities[i] -= demand  # Atualiza a capacidade restante da rota
                    inserted = True
                    break

            # Se o cliente não puder ser inserido em nenhuma rota existente, cria-se uma nova rota
            if not inserted:
                routes.append([client])
                route_capacities[len(routes) - 1] = self.graph.capacity - demand  # Capacidade da nova rota

        return routes

    def calculate_distance(self, solution):
        routes = self.decode_solution(solution)
        total_distance = 0.0

        for route in routes:
            route_distance = 0.0
            previous = self.graph.depot

            for client in route:
                route_distance += self.graph.graph[previous][client]
                previous = client

            route_distance += self.graph.graph[previous][self.graph.depot]
            total_distance += route_distance

        # Penalização proporcional ao número de veículos ultrapassados
        if len(routes) > self.graph.vehicles:
            penalty = (len(routes) - self.graph.vehicles) ** 2 * 1e5
            total_distance += penalty

        return total_distance

    def greedy_randomized_construction(self):
        unvisited = set(range(1, self.graph.dimension))  # Exclude depot
        solution = [self.depot]
        current_node = self.depot

        while unvisited:
            candidates = []
            for node in unvisited:
                if node not in solution:  # Ensure node hasn't been visited
                    cost = self.graph.graph[current_node, node]
                    candidates.append((node, cost))

            if not candidates:
                break

            candidates.sort(key=lambda x: x[1])
            min_cost = candidates[0][1]
            max_cost = candidates[-1][1]

            rcl = [node for node, cost in candidates
                   if cost <= min_cost + self.alpha * (max_cost - min_cost)]

            selected_node = random.choice(rcl)
            solution.append(selected_node)
            unvisited.remove(selected_node)
            current_node = selected_node

        return solution[1:]

    def local_search(self, solution):
        three_opt = ThreeOpt(self.graph, solution, self.calculate_distance(solution))
        improved_route, improved_distance = three_opt.solve_three_opt()

        return improved_route, improved_distance

    def run(self):
        for _ in range(self.max_iter):
            solution = self.greedy_randomized_construction()
            routes, cost = self.local_search(solution)
            self.best_routes, self.best_cost = self.decode_solution(routes), cost

            print(f'Iteração {_ + 1} Custo: {cost}')

        return self.best_routes, self.best_cost
