import math
import numpy as np
import os


class Graph:

    def __init__(self, name, comment, problem_type, dimension, edge_weight_type, capacity, node_list, node_demand):
        self.name = name
        self.comment = comment
        self.problem_type = problem_type
        self.dimension = int(dimension)
        self.edge_weight_type = edge_weight_type
        self.capacity = capacity
        self.node_list = node_list
        self.node_demand = node_demand
        self.depot_node = 0
        self.graph = np.zeros((self.dimension, self.dimension))
        self.arcs = int((dimension * dimension - dimension) / 2)

        for i in range(self.dimension):
            for j in range(self.dimension):
                self.graph[i, j] = Graph.euclidean_2d_calc(self.node_list[i], self.node_list[j])

    def __str__(self):
        s = (f'NAME: {self.name}\nCOMMENT: {self.comment}\nTYPE: {self.problem_type}\nDIMENSION: {self.dimension}'
             f'\nEDGE_WEIGHT_TYPE: {self.edge_weight_type}\nCAPACITY: {self.capacity}\nARCS: {self.arcs}\n')

        s += '\nNODE_COORD_SECTION\n'

        for node in self.node_list:
            s += f'Node {node[0]}: ({node[1]}, {node[2]})\n'

        s += '\nDEMAND_SECTION\n'

        for node in self.node_demand:
            s += f'Node {node[0]}: {node[1]}\n'

        return s

    @staticmethod
    def load_graph(file_path):
        node_list, node_demand = [], []

        with open(file_path, 'r') as f:
            lines = f.readlines()
            read_coord, read_demand = False, False

            for line in lines:
                line = line.strip()  # Remove espaços em branco

                if not read_coord and not read_demand:
                    if line.startswith("NAME"):
                        name = line.split(":")[1].strip()  # Nome do arquivo/problema
                    elif line.startswith("COMMENT"):
                        comment = line.split("COMMENT :")[1].strip()  # Comentário do arquivo/problema
                    elif line.startswith("TYPE"):
                        problem_type = line.split(":")[1].strip()  # Tipo de problema
                    elif line.startswith("DIMENSION"):
                        dimension = int(line.split(":")[1].strip())  # Número de nós (dimensão)
                    elif line.startswith("EDGE_WEIGHT_TYPE"):
                        edge_weight_type = line.split(":")[1].strip()  # Tipo de distância (EUC_2D)
                    elif line.startswith("CAPACITY"):
                        capacity = line.split(":")[1].strip()
                    elif line == "NODE_COORD_SECTION":
                        read_coord = True
                elif line == "DEMAND_SECTION":
                    read_coord, read_demand = False, True
                elif line == "EOF":
                    break  # Fim do arquivo

                if read_coord:
                    # A linha contém as coordenadas (id, x, y)
                    parts = line.split()
                    if len(parts) == 3:
                        node_id = int(parts[0])  # ID do nó
                        x = float(parts[1])  # Coordenada x
                        y = float(parts[2])  # Coordenada y
                        node_list.append((node_id, x, y))  # Armazena o nó

                if read_demand:
                    # A linha contém as demandas de cada nó
                    parts = line.split()
                    if len(parts) == 2:
                        node_id = int(parts[0])
                        demand = int(parts[1])
                        node_demand.append((node_id, demand))

        return Graph(name, comment, problem_type, dimension, edge_weight_type, capacity, node_list, node_demand)

    @staticmethod
    def euclidean_2d_calc(node1, node2):
        # Cálculo da distância euclidiana
        x = node1[1] - node2[1]
        y = node1[2] - node2[2]
        return math.sqrt(x * x + y * y)


if __name__ == '__main__':

    folder = 'files/instances'
    file_list = [os.path.join(folder, file) for file in os.listdir(folder) if file.endswith('.vrp')]

    for arquivo in file_list:
        graph = Graph.load_graph(arquivo)
        print(graph)
