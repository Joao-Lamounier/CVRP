import random

from local_search.ThreeOpt import ThreeOpt


class Grasph:
    def __init__(self, graph, start_node, alpha=0.125, max_iter=1000):
        self.graph = graph
        self.depot = start_node
        self.alpha = alpha
        self.max_iter = max_iter
        self.best_routes = None
        self.best_cost = float('inf')
        self.vehicle_capacity = graph.capacity
        self.demands = graph.demands
        self.max_vehicles = graph.vehicles

    def split_into_routes(self, solution):
        routes = []
        current_route = [self.depot]
        current_load = 0

        for node in solution[1:]:
            node_demand = self.demands[node]

            if current_load + node_demand <= self.vehicle_capacity:
                current_route.append(node)
                current_load += node_demand
            else:
                if current_route[-1] != self.depot:
                    current_route.append(self.depot)
                routes.append(current_route)

                # Start new route
                current_route = [self.depot, node]
                current_load = node_demand

        if current_route:
            if current_route[-1] != self.depot:
                current_route.append(self.depot)
            routes.append(current_route)

        cleaned_routes = []
        for route in routes:
            cleaned_route = []
            prev_node = None
            for node in route:
                if node != prev_node or node != self.depot:
                    cleaned_route.append(node)
                prev_node = node

            if cleaned_route[0] != self.depot:
                cleaned_route.insert(0, self.depot)
            if cleaned_route[-1] != self.depot:
                cleaned_route.append(self.depot)

            cleaned_routes.append(cleaned_route)

        return cleaned_routes

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

        return solution

    def calculate_routes_cost(self, routes):
        total_cost = 0
        for route in routes:
            route_cost = 0
            for i in range(len(route) - 1):
                route_cost += self.graph.graph[route[i], route[i + 1]]
            total_cost += route_cost
        return total_cost

    def local_search(self, solution):
        current_routes = self.split_into_routes(solution)
        best_routes = current_routes
        best_cost = self.calculate_routes_cost(current_routes)

        for i in range(len(best_routes)):
            route = best_routes[i]
            three_opt = ThreeOpt(self.graph.graph, 100, route, self.calculate_routes_cost([route]))
            improved_route, _ = three_opt.solve_three_opt()

            if improved_route[0] != self.depot:
                improved_route.insert(0, self.depot)
            if improved_route[-1] != self.depot:
                improved_route.append(self.depot)

            cleaned_route = []
            prev_node = None
            for node in improved_route:
                if node != prev_node or node != self.depot:
                    cleaned_route.append(node)
                prev_node = node

            best_routes[i] = cleaned_route

        return best_routes, self.calculate_routes_cost(best_routes)

    def run(self):
        for _ in range(self.max_iter):
            solution = self.greedy_randomized_construction()
            print(solution)
            routes, cost = self.local_search(solution)

            valid = True
            nodes_used = set()
            for route in routes:
                if route.count(self.depot) > 2:
                    valid = False
                    break

                route_nodes = set(route[1:-1])
                if route_nodes & nodes_used:
                    valid = False
                    break
                nodes_used.update(route_nodes)

            # Penalidade por excesso de veículos
            if len(routes) > self.max_vehicles:
                excess_vehicles = len(routes) - self.max_vehicles
                cost += (excess_vehicles ** 2) * 1e5

            if valid and cost < self.best_cost:
                self.best_routes = routes
                self.best_cost = cost

        return self.best_routes, self.best_cost
