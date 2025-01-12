class LocalSearch:
    def calculate_distance(self, route, distance_matrix):
        total_distance = 0.0
        for i in range(len(route) - 1):
            total_distance += distance_matrix[route[i]][route[i + 1]]
        # Fechando o ciclo ao voltar ao início
        total_distance += distance_matrix[route[-1]][route[0]]
        return total_distance
