import argparse
import os
from time import perf_counter

from entities.Graph import Graph
from metaheuristics.Grasph import Grasph


def main():
    args = parse_arguments()
    parameters = process_method_parameters(args.method)
    graph = load_graph(args.instance_file)
    output_file = args.instance_file + ".result"

    routes, objective_function, run_time = run_method(graph, parameters)
    write_results(args.instance_file, args.method, graph, routes,
                  objective_function, run_time, output_file)


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


def run_method(graph, parameters):
    begin = perf_counter()
    method_type = parameters['type']

    if method_type == 'GRASP':
        grasp_solver = Grasph(
            graph,
            alpha=parameters['alpha'],
            max_iter=parameters['max_iter'],
            start_node=graph.getDeposito()
        )
        best_routes, best_cost = grasp_solver.run()
        return best_routes, best_cost, perf_counter() - begin


def load_graph(instance_file):
    folder = 'files/instances/'
    return Graph.load_graph(folder + instance_file)


def write_results(instance_file, method, graph, routes, objective_function, run_time, output_file):
    with open(output_file, 'w') as f:
        for i, route in enumerate(routes, 1):
            route_str = ' '.join(str(node) for node in route[1:])
            f.write(f"Route #{i}: {route_str}\n")
        f.write(f"Cost {int(objective_function)}:\n")

    stats_file = output_file + ".stats"
    file_exists = os.path.exists(stats_file)

    with open(stats_file, 'a') as f:
        if not file_exists:
            f.write(
                f"{'INSTANCE': <20}{'METHOD': <15}{'OBJECTIVE': <15}{'RUNTIME': <15}"
                f"{'DIMENSION': <10}{'CAPACITY': <10}\n"
            )
        f.write(
            f"{instance_file: <20}{method: <15}{objective_function: <15.2f}"
            f"{run_time: <15.3f}{graph.dimension: <10}{graph.capacity: <10}\n"
        )


def run_method(graph, parameters):
    begin = perf_counter()
    method_type = parameters['type']

    if method_type == 'GRASP':
        grasp_solver = Grasph(
            graph,
            alpha=parameters['alpha'],
            max_iter=parameters['max_iter'],
            start_node=1  # Depot
        )
        routes, cost = grasp_solver.run()
        run_time = perf_counter() - begin
        return routes, cost, run_time


if __name__ == '__main__':
    main()
