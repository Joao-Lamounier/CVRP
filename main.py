import argparse
import os
from time import perf_counter

from entities.Graph import Graph
from metaheuristics.Grasph import Grasph


def main():
    args = parse_arguments()
    parameters = process_method_parameters(args.method)
    graph = load_graph(args.instance_file)

    # Define o diretório de saída
    output_dir = f"files/results/{args.instance_file}"
    os.makedirs(output_dir, exist_ok=True)
    output_file = f"{output_dir}/result.txt"

    optimal_cost = load_optimal_cost(args.instance_file)

    routes, objective_function, run_time = run_method(graph, parameters)
    write_results(output_dir, args.instance_file, args.method, graph, routes,
                  objective_function, run_time, output_file, optimal_cost)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Solucionador CVRP usando heurísticas e metaheurísticas")
    parser.add_argument("instance_file", type=str, help="Arquivo de instância CVRP")
    parser.add_argument("method", type=str, help="Método a ser utilizado (ex: GRASP-100-0.3)")
    return parser.parse_args()


def process_method_parameters(method_string):
    """
    Processa a string do método para extrair os parâmetros
    Exemplo: 'GRASP-100-0.3' retorna ('GRASP', 100, 0.3)
    """
    parts = method_string.split('-')
    if len(parts) == 3 and parts[0] == 'GRASP':
        return {
            'type': 'GRASP',
            'max_iter': int(parts[1]),
            'alpha': float(parts[2])
        }
    return {
        'type': method_string
    }


def load_graph(instance_file):
    folder = 'files/instances/'
    return Graph.load_graph(folder + instance_file)


def load_optimal_cost(instance_file):
    """
    Carrega o valor ótimo da função a partir do arquivo correspondente.
    """
    instance_name = os.path.splitext(instance_file)[0]  # Remove a extensão .vrp
    optimal_file = f"files/optimal_solutions/{instance_name}.sol"
    if os.path.exists(optimal_file):
        with open(optimal_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("Cost"):
                    return int(line.split()[1])
    return None


def write_results(output_dir, instance_file, method, graph, routes, objective_function, run_time, output_file,
                  optimal_cost):
    with open(output_file, 'w') as f:
        for i, route in enumerate(routes, 1):
            route_str = ' '.join(str(node) for node in route)
            f.write(f"Route #{i}: {route_str}\n")
        f.write(f"Cost {int(objective_function)}:\n")

    stats_file = f"{output_dir}/stats.txt"
    file_exists = os.path.exists(stats_file)

    with open(stats_file, 'a') as f:
        if not file_exists:
            f.write(
                f"{'INSTANCE': <20}{'METHOD': <15}{'OBJECTIVE': <15}{'RUNTIME': <15}"
                f"{'DIMENSION': <10}{'CAPACITY': <10}{'GAP': <10}\n"
            )
        f.write(
            f"{instance_file: <20}{method: <15}{objective_function: <15.2f}"
            f"{run_time: <15.3f}{graph.dimension: <10}{graph.capacity: <10}"
            f"{gap(objective_function, optimal_cost): <20}\n"
        )


def gap(objective_function, optimal_solution):
    return 100 * ((objective_function - optimal_solution) / optimal_solution)


def run_method(graph, parameters):
    begin = perf_counter()
    method_type = parameters['type']

    if method_type == 'GRASP':
        grasp_solver = Grasph(
            graph,
            alpha=parameters['alpha'],
            max_iter=parameters['max_iter'],
            start_node=graph.depot
        )
        routes, cost = grasp_solver.run()
        run_time = perf_counter() - begin
        return routes, cost, run_time


if __name__ == '__main__':
    main()
