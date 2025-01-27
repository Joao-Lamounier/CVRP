import random
from local_search.ThreeOpt import ThreeOpt


class Grasp:
    def __init__(self, cvrp, alpha=0.125, max_iter=1000):
        self.cvrp = cvrp
        self.objective_function, self.routes = float('inf'), []
        self.alpha = alpha
        self.max_iter = max_iter

    def split_into_routes(self, solution):
        routes = []
        current_route = [self.cvrp.depot]
        current_load = 0

        for node in solution[1:]:
            node_demand = self.cvrp.demands[node]

            if current_load + node_demand <= self.cvrp.vehicle_capacity:
                current_route.append(node)
                current_load += node_demand
            else:
                if current_route[-1] != self.cvrp.depot:
                    current_route.append(self.cvrp.depot)
                routes.append(current_route)

                # Inicia uma nova rota
                current_route = [self.cvrp.depot, node]
                current_load = node_demand

        if current_route:
            if current_route[-1] != self.cvrp.depot:
                current_route.append(self.cvrp.depot)
            routes.append(current_route)

        cleaned_routes = []
        for route in routes:
            cleaned_route = []
            prev_node = None
            for node in route:
                if node != prev_node or node != self.cvrp.depot:
                    cleaned_route.append(node)
                prev_node = node

            if cleaned_route[0] != self.cvrp.depot:
                cleaned_route.insert(0, self.cvrp.depot)
            if cleaned_route[-1] != self.cvrp.depot:
                cleaned_route.append(self.cvrp.depot)

            cleaned_routes.append(cleaned_route)

        return cleaned_routes

    def greedy_randomized_construction(self):
        unvisited = set(range(1, self.cvrp.dimension))  # Desconsidera o depósito (0)
        solution = [self.cvrp.depot]
        current_node = self.cvrp.depot

        while unvisited:
            candidates = []
            for node in unvisited:
                if node not in solution:
                    cost = self.cvrp.graph[current_node, node]
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

        return solution

    def calculate_routes_cost(self, routes):
        total_cost = 0
        for route in routes:
            route_cost = 0
            for i in range(len(route) - 1):
                route_cost += self.cvrp.graph[route[i], route[i + 1]]
            total_cost += route_cost
        return total_cost

    def local_search(self, solution):
        current_routes = self.split_into_routes(solution)
        best_routes = current_routes

        for i in range(len(best_routes)):
            route = best_routes[i]
            three_opt = ThreeOpt(self.cvrp.graph, route, self.calculate_routes_cost([route]))
            improved_route, _ = three_opt.solve_three_opt()

            if improved_route[0] != self.cvrp.depot:
                improved_route.insert(0, self.cvrp.depot)
            if improved_route[-1] != self.cvrp.depot:
                improved_route.append(self.cvrp.depot)

            cleaned_route = []
            prev_node = None
            for node in improved_route:
                if node != prev_node or node != self.cvrp.depot:
                    cleaned_route.append(node)
                prev_node = node

            best_routes[i] = cleaned_route

        return best_routes, self.calculate_routes_cost(best_routes)

    def solve_grasp(self):
        for _ in range(self.max_iter):
            solution = self.greedy_randomized_construction()
            routes, cost = self.local_search(solution)

            valid = True
            nodes_used = set()
            for route in routes:
                if route.count(self.cvrp.depot) > 2:
                    valid = False
                    break

                route_nodes = set(route[1:-1])
                if route_nodes & nodes_used:
                    valid = False
                    break
                nodes_used.update(route_nodes)

            # Penalização: Número de veículos ultrapassados
            if len(routes) > self.cvrp.max_vehicles:
                excess_vehicles = len(routes) - self.cvrp.max_vehicles
                cost += (excess_vehicles ** 2) * 1e5

            if valid and cost < self.objective_function:
                self.routes = routes
                self.objective_function = cost

        return self.routes, self.objective_function
