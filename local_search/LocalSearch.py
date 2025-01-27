class LocalSearch:

    def decode_solution(self, cvrp, solution):
        routes = []
        route_capacities = {}  # Dicionário para armazenar a capacidade restante de cada rota

        for client in solution:
            demand = cvrp.demands[client]
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
                route_capacities[len(routes) - 1] = cvrp.capacity - demand  # Capacidade da nova rota

        return routes

    def calculate_distance(self, cvrp, solution):
        routes = self.decode_solution(cvrp, solution)
        total_distance = 0.0

        for route in routes:
            route_distance = 0.0
            previous = cvrp.depot

            for client in route:
                route_distance += cvrp.graph[previous][client]
                previous = client

            route_distance += cvrp.graph[previous][cvrp.depot]
            total_distance += route_distance

        # Penalização proporcional ao número de veículos ultrapassados
        if len(routes) > cvrp.vehicles:
            penalty = (len(routes) - cvrp.vehicles) ** 2 * 1e5
            total_distance += penalty

        return total_distance
