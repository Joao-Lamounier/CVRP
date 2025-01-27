import random


class GeneticAlgorithm:

    def __init__(self, graph, mutation_rate=0.05, elitism_rate=0.15, num_generations=400):
        self.graph = graph
        self.objetive_function = 0.0
        self.routes = []
        self.mutation_rate = mutation_rate
        self.population_size = 500 * (self.graph.dimension - 1)
        self.num_generations = num_generations
        self.elitism_rate = elitism_rate

    def create_individual(self):
        clients = list(range(1, self.graph.dimension))
        random.shuffle(clients)
        return clients

    def decode_individual(self, individual):
        routes = []
        route_capacities = {}  # Dicionário para armazenar a capacidade restante de cada rota

        for client in individual:
            demand = self.graph.demands[client]
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
                route_capacities[len(routes) - 1] = self.graph.capacity - demand  # Capacidade da nova rota

        return routes

    def calculate_fitness(self, individual):
        routes = self.decode_individual(individual)
        total_distance = 0.0

        for route in routes:
            route_distance = 0.0
            previous = self.graph.depot

            for client in route:
                route_distance += self.graph.graph[previous][client]
                previous = client

            route_distance += self.graph.graph[previous][self.graph.depot]
            total_distance += route_distance

        # Penalização proporcional ao número de veículos ultrapassados
        if len(routes) > self.graph.vehicles:
            penalty = (len(routes) - self.graph.vehicles) ** 2 * 1e5
            total_distance += penalty

        return total_distance

    def crossover(self, parent_1, parent_2):
        cut = random.randint(1, len(parent_1) - 1)
        child = parent_1[:cut] + [c for c in parent_2 if c not in parent_1[:cut]]
        return child

    def mutate(self, individual):
        if random.random() < self.mutation_rate:
            idx1, idx2 = random.sample(range(len(individual)), 2)
            individual[idx1:idx2 + 1] = individual[idx1:idx2 + 1][::-1]

    def genetic_algorithm(self):
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

            # Seleção dos indivíduos para o Crossover
            population = [ind for _, ind in fitness_scores[:self.population_size // 2]]

            # Geração da nova população
            while len(new_population) < self.population_size:
                parent_1, parent_2 = random.sample(population, 2)
                child = self.crossover(parent_1, parent_2)
                self.mutate(child)
                new_population.append(child)

            # print(f'\nGeração: {generation + 1} Melhor Aptidão: {fitness_scores[0][0]}')

            # Nova população
            population = new_population

        # Melhor indivíduo
        self.objetive_function, best_individual = fitness_scores[0]
        self.routes = self.decode_individual(best_individual)
