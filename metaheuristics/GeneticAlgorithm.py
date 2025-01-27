import random


class GeneticAlgorithm:

    def __init__(self, cvrp, elitism_rate, mutation_rate, num_generations):
        self.cvrp = cvrp
        self.objective_function, self.routes = float('inf'), []
        self.run_time = 0.0
        self.population_size = 500 * (self.cvrp.dimension - 1)
        self.elitism_rate = elitism_rate
        self.mutation_rate = mutation_rate
        self.num_generations = num_generations

    def create_individual(self):
        clients = list(range(1, self.cvrp.dimension))
        random.shuffle(clients)
        return clients

    def decode_individual(self, individual):
        routes, route_capacities = [], {}

        for client in individual:
            demand = self.cvrp.demands[client]
            inserted = False

            # Tentativa: Inserir o cliente numa rota existente
            for i, route in enumerate(routes):
                if route_capacities[i] >= demand:
                    route.append(client)
                    route_capacities[i] -= demand  # Atualiza a capacidade restante da rota
                    inserted = True
                    break

            # Criação nova rota: Se o cliente não puder ser inserido em nenhuma rota existente
            if not inserted:
                routes.append([client])
                route_capacities[len(routes) - 1] = self.cvrp.vehicle_capacity - demand  # Capacidade da nova rota

        return routes

    def calculate_fitness(self, individual):
        routes = self.decode_individual(individual)
        total_distance = 0.0

        for route in routes:
            route_distance = 0.0
            previous = self.cvrp.depot

            for client in route:
                route_distance += self.cvrp.graph[previous][client]
                previous = client

            route_distance += self.cvrp.graph[previous][self.cvrp.depot]
            total_distance += route_distance

        # Penalização: Número de veículos ultrapassados
        if len(routes) > self.cvrp.max_vehicles:
            penalty = (len(routes) - self.cvrp.max_vehicles) ** 2 * 1e5
            total_distance += penalty

        return total_distance

    @staticmethod
    def crossover(parent_1, parent_2):
        # Operador PMX - Partially Mapped Crossover
        cut = random.randint(1, len(parent_1) - 1)
        child = parent_1[:cut] + [c for c in parent_2 if c not in parent_1[:cut]]
        return child

    def mutate(self, individual):
        # Operador Reverse
        if random.random() < self.mutation_rate:
            idx1, idx2 = random.sample(range(len(individual)), 2)
            individual[idx1:idx2 + 1] = individual[idx1:idx2 + 1][::-1]

    def solve_genetic_algorithm(self):
        # Inicialização da população
        population = [self.create_individual() for _ in range(self.population_size)]
        fitness_scores = []

        for generation in range(self.num_generations):
            # Avaliação da população
            fitness_scores = [(self.calculate_fitness(ind), ind) for ind in population]

            # Ordenação da população por aptidão
            fitness_scores.sort(key=lambda x: x[0])
            population = [ind for _, ind in fitness_scores]

            # Elitismo
            num_elite = int(self.elitism_rate * self.population_size)
            new_population = population[:num_elite]

            # Seleção Crossover: 50% dos melhores indivíduos
            population = [ind for _, ind in fitness_scores[:self.population_size // 2]]

            # Geração da nova população
            while len(new_population) < self.population_size:
                parent_1, parent_2 = random.sample(population, 2)
                child = GeneticAlgorithm.crossover(parent_1, parent_2)
                self.mutate(child)
                new_population.append(child)

            # Nova população
            population = new_population

        # Melhor indivíduo
        self.objective_function, best_individual = fitness_scores[0]
        self.routes = self.decode_individual(best_individual)
