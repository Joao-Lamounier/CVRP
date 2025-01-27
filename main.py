import argparse
import os
from time import perf_counter

from entities.CVRP import CVRP
from metaheuristics.Grasp import Grasp


def main():
    # Configuração dos argumentos de linha de comando
    args = parse_arguments()

    # Processa os argumentos do método
    parameters = process_method_parameters(args.method)

    # Carrega o grafo do arquivo de entrada
    graph = load_graph(args.instance_file)


    # Define o arquivo de saída
    output_file = args.instance_file + ".result"

    # Executa o método selecionado
    objective_function, run_time = run_method(graph, parameters)

    # Escreve os resultados no arquivo de saída
    write_results(args.instance_file, args.method, graph, objective_function, run_time, output_file)


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
    method_type = parameters['type']
    best_cost = float('inf')
    if method_type == 'GRASP':
        grasp_solver = Grasp(
            graph,
            alpha=parameters['alpha'],
            max_iter=parameters['max_iter'],
        )
        best_tour, best_cost = grasp_solver.solve_grasp()

    run_time = 0.0
    return best_cost, run_time


def load_graph(instance_file):
    folder = 'files/instances/'
    return CVRP.load_graph(folder + instance_file)


def write_results(instance_file, method, graph, objective_function, run_time, output_file):
    file_exists = os.path.exists(output_file) and os.path.getsize(output_file) > 0

    if not file_exists:
        with open(output_file, 'a') as f:
            f.write(
                f"{'INSTANCE': <20}{'METHOD': <15}{'OBJECTIVE': <15}{'RUNTIME': <15}"
                f"{'DIMENSION': <10}{'CAPACITY': <10}\n"
            )

    with open(output_file, 'a') as f:
        f.write(
            f"{instance_file: <20}{method: <15}{objective_function: <15.2f}"
            f"{run_time: <15.3f}{graph.dimension: <10}{graph.capacity: <10}\n"
        )


if __name__ == '__main__':
    main()