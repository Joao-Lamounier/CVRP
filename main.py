import argparse
import os
import re
from time import perf_counter

from entities.CVRP import CVRP
from metaheuristics.GeneticAlgorithm import GeneticAlgorithm
from metaheuristics.Grasp import Grasp


def main():
    # Configuração dos argumentos de linha de comando
    args = parse_arguments()

    # Processa os argumentos do método
    parameters = argument_process(args.method)

    # Carrega o CVRP do arquivo de entrada
    cvrp = load_cvrp(args.instance_file)

    # Define o arquivo de saída
    output_file = args.output_file

    # Executa o método selecionado
    objective_function, run_time = run_method(cvrp, parameters)

    # Escreve os resultados no arquivo de saída
    write_results(args.instance_file, args.method, cvrp, objective_function, run_time, output_file)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Solucionador CVRP usando metaheurísticas")
    parser.add_argument("instance_file", type=str, help="Arquivo de instância CVRP")
    parser.add_argument("output_file", type=str, help="Caminho para o arquivo de saída dos resultados")
    parser.add_argument("method", type=str, help="Método a ser utilizado (GRASP ou GA)")
    return parser.parse_args()


def genetic_argument(command_string):
    genetic_pattern = r"GA-([0-1]\.\d+|\d+)-([0-1]\.\d+|\d+)-(\d+)"
    match = re.match(genetic_pattern, command_string)

    if match:
        elitism_rate = float(match.group(1))
        mutate_rate = float(match.group(2))
        num_generation = int(match.group(3))

        if num_generation <= 0:
            print("[!] -> ERRO: O número de gerações deve ser maior que 0!")
            exit(1)

        if not (0.0 <= elitism_rate <= 1.0):
            print("[!] -> ERRO: A taxa de elitismo deve estar entre 0.0 e 1.0!")
            exit(1)

        if not (0.0 <= mutate_rate <= 1.0):
            print("[!] -> ERRO: A taxa de mutação deve estar entre 0.0 e 1.0!")
            exit(1)

    else:
        print("[!] -> ERRO: O formato para Algoritmo Genético está INCORRETO! "
              "Use 'GA-<elitismo>-<mutacao>-<num_geracoes>'")
        exit(1)


def grasp_argument(command_string):
    grasp_pattern = r"GRASP-(\d+)-([0-1]\.\d+|\d+)"
    match = re.match(grasp_pattern, command_string)

    if match:
        grasp_iter = int(match.group(1))
        grasp_alpha = float(match.group(2))

        if grasp_iter <= 0:
            print("[!] -> ERRO: O número de iterações deve ser maior que 0!")
            exit(1)

        if not (0.0 <= grasp_alpha <= 1.0):
            print("[!] -> ERRO: O valor de alpha deve estar entre 0.0 e 1.0!")
            exit(1)
    else:
        print("[!] -> ERRO: O formato para GRASP está INCORRETO! Use 'GRASP-<iteracoes>-<alpha>'")
        exit(1)


def argument_process(command_string):
    # Dividindo o comando em partes com base no separador "-"
    parts = command_string.split('-')

    if parts[0] == "GRASP":
        grasp_argument(command_string)
        return parts[0], int(parts[1]), float(parts[2])
    else:
        genetic_argument(command_string)
        return parts[0], float(parts[1]), float(parts[2]), int(parts[3])


def load_cvrp(instance_file):
    folder = 'files/instances/'
    return CVRP.load_cvrp(folder + instance_file)


def run_genetic_algorithm(cvrp, parameters):
    _, elitism_rate, mutate_rate, num_generation = parameters
    genetic_algorithm = GeneticAlgorithm(cvrp, elitism_rate, mutate_rate, num_generation)
    genetic_algorithm.run_time = measure_execution_time(genetic_algorithm.solve_genetic_algorithm)
    return genetic_algorithm.objective_function, genetic_algorithm.run_time


def run_grasp(cvrp, parameters):
    _, max_iterations, alpha = parameters
    grasp = Grasp(cvrp, max_iterations, alpha)
    grasp.run_time = measure_execution_time(grasp.solve_grasp)
    return grasp.objective_function, grasp.run_time


def run_method(cvrp, parameters):
    if parameters[0] == 'GRASP':
        return run_grasp(cvrp, parameters)
    else:
        return run_genetic_algorithm(cvrp, parameters)


def write_results(instance_file, method, cvrp, objective_function, run_time, output_file):
    file_exists = os.path.exists(output_file) and os.path.getsize(output_file) > 0

    if not file_exists:
        with open(output_file, 'a') as f:
            f.write(
                f"{'INSTANCE': <16}{'METHOD': <22}{'OBJECTIVE': <15}{'OPTIMAL_SOLUTION':<20}"
                f"{'GAP': <24}{'RUNTIME': <24}{'DIMENSION': <12}{'CAPACITY': <10}{'VEHICLES':<10}\n"
            )

    with open(output_file, 'a') as f:
        f.write(
            f"{instance_file: <16}{method: <22}{objective_function: <15}{cvrp.optimal_solution: <20}"
            f"{gap(objective_function, cvrp.optimal_solution): <24}{run_time: <24}{cvrp.dimension: <12}"
            f"{cvrp.vehicle_capacity: <10}{cvrp.max_vehicles: <10}\n"
        )


def gap(objective_function, optimal_solution):
    return 100 * ((objective_function - optimal_solution) / optimal_solution)


def measure_execution_time(func, *args, **kwargs):
    begin = perf_counter()
    func(*args, **kwargs)
    end = perf_counter()
    return end - begin


if __name__ == '__main__':
    main()
