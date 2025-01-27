from .LocalSearch import LocalSearch


class ThreeOpt(LocalSearch):
    def __init__(self, distance_matrix, path, objective_function):
        self.distance_matrix = distance_matrix
        self.objective_function = objective_function
        self.path = path
        self.dimension = len(path)

    def solve_three_opt(self):
        route, best_distance = self.path[:], self.objective_function
        improved = True

        while improved:
            improved = False
            for i in range(self.dimension - 2):
                for j in range(i + 1, self.dimension - 1):
                    for k in range(j + 1, self.dimension):
                        candidates = [
                            route[:i] + route[i:j][::-1] + route[j:k][::-1] + route[k:],
                            route[:i] + route[j:k][::-1] + route[i:j] + route[k:],
                            route[:i] + route[j:k][::-1] + route[i:j][::-1] + route[k:],
                            route[:i] + route[i:j] + route[j:k][::-1] + route[k:],
                            route[:i] + route[i:j][::-1] + route[k:j:-1] + route[j:],
                            route[:i] + route[k:j:-1] + route[i:j] + route[j:],
                            route[:i] + route[k:j:-1] + route[i:j][::-1] + route[j:],
                            route[:i] + route[i:j] + route[k:j:-1] + route[j:]
                        ]

                        for new_route in candidates:
                            new_distance = self.calculate_distance(new_route, self.distance_matrix)
                            if new_distance < best_distance:
                                route = new_route
                                best_distance = new_distance
                                improved = True
                                break

                        if improved:
                            break

                    if improved:
                        break

                if improved:
                    break

        self.path, self.objective_function = route, best_distance
        return route, best_distance
