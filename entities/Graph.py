import math
import numpy as np
import os
import re
from time import perf_counter

from metaheuristics.GeneticAlgorithm import GeneticAlgorithm


class Graph:
    def __init__(self, name, comment, problem_type, dimension, edge_weight_type, capacity, node_list, demands,
                 depot, file_solution):
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
        self.vehicles = int(re.search(r'k(\d+)', name)[1])
        self.optimal_solution, self.optimal_routes = Graph.load_optimal_solution(file_solution)

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
                        node_id = int(parts[0]) - 1
                        demand = int(parts[1])
                        demands[node_id] = demand

                    elif current_section == "depot" and len(parts) == 1:
                        depot_id = int(parts[0])
                        if depot_id != -1:  # Ignora o marcador de fim da seção
                            depot = depot_id

        return Graph(name, comment, problem_type, dimension, edge_weight_type,
                     capacity, node_list, demands, depot, '../files/optimal_solutions/' + name + '.sol')

    @staticmethod
    def load_optimal_solution(file_path):
        routes = []
        with open(file_path, 'r') as f:
            lines = f.readlines()
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

    def calculate_fitness(self, routes):
        total_distance = 0.0

        for route in routes:
            route_distance = 0.0
            previous = self.depot

            for client in route:
                route_distance += self.graph[previous][client]
                previous = client

            route_distance += self.graph[previous][self.depot]
            total_distance += route_distance

        return total_distance

    def calculate_distance(self):
        total_distance = 0.0

        for i in range(len(self.optimal_routes)):
            route = self.optimal_routes[i]
            total_distance += self.graph[self.depot][route[0]]
            for j in range(len(self.optimal_routes[i]) - 1):
                total_distance += self.graph[route[j]][route[j + 1]]
            total_distance += self.graph[route[-1]][self.depot]

        return float(total_distance)

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

    def get_deposito(self):
        """Retorna as coordenadas do nó depósito"""
        for node in self.node_list:
            if node[0] == self.depot:
                return node[1], node[2]  # Retorna as coordenadas x, y do depósito
        return None


if __name__ == '__main__':

    folder = '../files/instances/'
    file_list = [os.path.join(folder, file) for file in os.listdir(folder) if file.endswith('.vrp')]

    artigo_instancia = ['P-n16-k8', 'P-n19-k2', 'P-n20-k2', 'P-n22-k8', 'M-n101-k10', 'P-n40-k5', 'P-n51-k10']

    nomes = [
        "A-n32-k5", "A-n39-k5", "A-n55-k9", "A-n80-k10", "B-n44-k7", "B-n63-k10",
        "M-n121-k7", "P-n40-k5", "P-n60-k10", "X-n115-k10", "A-n33-k5", "A-n39-k6",
        "A-n60-k9", "B-n31-k5", "B-n45-k5", "B-n64-k9", "M-n151-k12", "P-n45-k5",
        "P-n60-k15", "X-n120-k6", "A-n33-k6", "A-n44-k6", "A-n62-k8", "B-n34-k5",
        "B-n45-k6", "B-n66-k9", "P-n101-k4", "P-n50-k10", "P-n65-k10", "X-n129-k18",
        "A-n34-k5", "A-n45-k7", "A-n63-k10", "B-n35-k5", "B-n50-k7", "B-n67-k10",
        "P-n16-k8", "P-n50-k7", "P-n70-k10", "X-n134-k13", "A-n36-k5", "A-n46-k7",
        "A-n63-k9", "B-n38-k6", "B-n51-k7", "B-n68-k9", "P-n19-k2", "P-n51-k10",
        "P-n76-k4", "X-n139-k10", "A-n37-k5", "A-n48-k7", "A-n64-k9", "B-n39-k5",
        "B-n52-k7", "B-n78-k10", "P-n20-k2", "P-n55-k10", "P-n76-k5", "X-n143-k7",
        "A-n37-k6", "A-n53-k7", "A-n65-k9", "B-n41-k6", "B-n56-k7", "F-n72-k4",
        "P-n21-k2", "P-n55-k7", "X-n106-k14", "A-n38-k5", "A-n54-k7", "A-n69-k9",
        "B-n43-k6", "B-n57-k9", "M-n101-k10", "P-n22-k2", "P-n55-k8", "X-n110-k13"
    ]

    route_teste = [[1, 10, 8, 16, 17, 3, 12, 14, 11, 4], [6, 2, 7, 9, 15, 13, 5, 18]]

    for file in file_list:
        graph = Graph.load_graph(file)
        GA = GeneticAlgorithm(graph)

        if graph.name in nomes: # graph.optimal_solution == graph.calculate_fitness(graph.optimal_routes) and graph.name not in ['P-n55-k15', 'X-n101-k25', 'X-n125-k30', 'X-n148-k46'] and graph.name in artigo_instancia and graph.name == 'M-n101-k10':

            begin = perf_counter()
            GA.genetic_algorithm()
            end = perf_counter()

            print(f'NAME: {graph.name} OPTIMAL_SOLUTION: {graph.optimal_solution} '
                  f' OBJECTIVE FUNCTION: {GA.objetive_function} '
                  f' GAP: {100*((GA.objetive_function - graph.optimal_solution)/graph.optimal_solution)} '
                  f' ROUTES: {len(GA.routes)} '
                  f' RUN_TIME: {end - begin}'
                  f'Routes {GA.routes}')
