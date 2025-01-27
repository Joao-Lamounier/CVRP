import math
import numpy as np
import re


class CVRP:
    def __init__(self, name, comment, problem_type, dimension, edge_weight_type,
                 vehicle_capacity, node_list, demands, depot, file_solution):

        # Informações Gerais - CVRP
        self.name, self.comment, self.problem_type = name, comment, problem_type
        self.edge_weight_type = edge_weight_type
        self.dimension, self.arcs = dimension, (dimension * dimension - dimension) // 2
        self.max_vehicles, self.vehicle_capacity = int(re.search(r'k(\d+)', name)[1]), vehicle_capacity
        self.node_list, self.demands, self.depot = node_list, demands, depot - 1
        self.optimal_solution, self.optimal_routes = CVRP.load_optimal_solution(file_solution)

        # Preenchimento Distâncias - Grafo
        self.graph = np.zeros((self.dimension, self.dimension))
        for i in range(self.dimension):
            for j in range(self.dimension):
                self.graph[i, j] = CVRP.euclidean_2d_calc(self.node_list[i], self.node_list[j])

    @staticmethod
    def load_graph(file_path):
        node_list, demands = [], {}

        with open(file_path, 'r') as file:
            lines = file.readlines()

            # Controle de seção - leitura do arquivo
            current_section = None

            for line in lines:
                line = line.strip()

                # Ignora linhas vazias
                if not line:
                    continue

                # Processamento - Informações Gerais
                if line.startswith("NAME"):
                    name = line.split(":")[1].strip()
                elif line.startswith("COMMENT"):
                    comment = line.split(":")[1].strip()
                elif line.startswith("TYPE"):
                    problem_type = line.split(":")[1].strip()
                elif line.startswith("DIMENSION"):
                    dimension = int(line.split(":")[1].strip())
                elif line.startswith("EDGE_WEIGHT_TYPE"):
                    edge_weight_type = line.split(":")[1].strip()
                elif line.startswith("CAPACITY"):
                    capacity = int(line.split(":")[1].strip())

                # Controle de seções
                elif line == "NODE_COORD_SECTION":
                    current_section = "coordinates"
                elif line == "DEMAND_SECTION":
                    current_section = "demands"
                elif line == "DEPOT_SECTION":
                    current_section = "depot"
                elif line == "EOF":
                    break

                # Processamento de dados: Conforme a seção atual
                else:
                    parts = line.split()
                    if current_section == "coordinates" and len(parts) == 3:
                        node_id = int(parts[0])
                        x = float(parts[1])
                        y = float(parts[2])
                        node_list.append((node_id, x, y))

                    elif current_section == "demands" and len(parts) == 2:
                        node_id = int(parts[0]) - 1
                        demand = int(parts[1])
                        demands[node_id] = demand

                    elif current_section == "depot" and len(parts) == 1:
                        depot_id = int(parts[0])
                        if depot_id != -1:  # Ignora o marcador de fim da seção
                            depot = depot_id

        return CVRP(name, comment, problem_type, dimension, edge_weight_type, capacity,
                    node_list, demands, depot, '../files/optimal_solutions/' + name + '.sol')

    @staticmethod
    def load_optimal_solution(file_path):
        routes = []
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith("Cost"):
                    cost = float(line.split()[1].strip())
                elif line.startswith("Route"):
                    route = line.split(":")[1].split()
                    new_route = []
                    for i in range(len(route)):
                        new_route.append(int(route[i]))
                    routes.append(new_route)
        return cost, routes

    @staticmethod
    def euclidean_2d_calc(node1, node2):
        x = node1[1] - node2[1]
        y = node1[2] - node2[2]
        return round(math.sqrt(x * x + y * y))
