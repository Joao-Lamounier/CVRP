import math
import numpy as np


class Graph:
    def __init__(self, name, comment, problem_type, dimension, edge_weight_type, capacity, node_list, demands, depot):
        self.name = name
        self.comment = comment
        self.problem_type = problem_type
        self.dimension = int(dimension)
        self.edge_weight_type = edge_weight_type
        self.capacity = int(capacity)
        self.node_list = node_list
        self.demands = demands
        self.depot = depot - 1
        self.graph = np.zeros((self.dimension, self.dimension))
        self.arcs = int((dimension * dimension - dimension) / 2)
        self.optimal_solution = 0.0

        # Calcula a matriz de distâncias
        for i in range(self.dimension):
            for j in range(self.dimension):
                self.graph[i, j] = Graph.euclidean_2d_calc(self.node_list[i], self.node_list[j])

    @staticmethod
    def load_graph(file_path):
        node_list = []
        demands = {}
        depot = None
        capacity = 0

        with open(file_path, 'r') as f:
            lines = f.readlines()

            # Estados para controlar a leitura do arquivo
            current_section = None

            for line in lines:
                line = line.strip()

                # Ignora linhas vazias
                if not line:
                    continue

                # Processa cabeçalho
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

                # Processa dados de acordo com a seção atual
                else:
                    parts = line.split()
                    if current_section == "coordinates" and len(parts) == 3:
                        node_id = int(parts[0])
                        x = float(parts[1])
                        y = float(parts[2])
                        node_list.append((node_id, x, y))

                    elif current_section == "demands" and len(parts) == 2:
                        node_id = int(parts[0])
                        demand = int(parts[1])
                        demands[node_id] = demand

                    elif current_section == "depot" and len(parts) == 1:
                        depot_id = int(parts[0])
                        if depot_id != -1:  # Ignora o marcador de fim da seção
                            depot = depot_id

        return Graph(name, comment, problem_type, dimension, edge_weight_type,
                     capacity, node_list, demands, depot)

    @staticmethod
    def euclidean_2d_calc(node1, node2):
        x = node1[1] - node2[1]
        y = node1[2] - node2[2]
        return round(math.sqrt(x * x + y * y))

    def get_demand(self, node_id):
        """Retorna a demanda para um determinado nó"""
        return self.demands.get(node_id, 0)

    def is_depot(self, node_id):
        """Verifica se o nó é o depósito"""
        return node_id == self.depot

    def get_total_demand(self):
        """Calcula a demanda total de todos os nós"""
        return sum(self.demands.values())

    def get_route_demand(self, route):
        """Calcula a demanda total para uma rota específica"""
        return sum(self.demands[node] for node in route if node in self.demands)
