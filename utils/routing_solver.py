import json
from pathlib import Path
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

def parse_kilometers(dist_str):
    dist_str = dist_str.strip()
    if "km" in dist_str:
        return float(dist_str.replace(" km", "").replace(",", "."))
    elif "m" in dist_str:
        return float(dist_str.replace(" m", "").replace(",", ".")) / 1000
    else:
        raise ValueError(f"Formato de distancia no reconocido: {dist_str}")

def create_distance_matrix(matrix_data):
    coordenadas = matrix_data["coordenadas"]
    matriz_texto = matrix_data["matriz"]

    distancia_numerica = [
        [parse_kilometers(valor) for valor in fila]
        for fila in matriz_texto
    ]

    return distancia_numerica, coordenadas

def solve_tsp(distance_matrix):
    manager = pywrapcp.RoutingIndexManager(len(distance_matrix), 1, 0)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        return int(distance_matrix[manager.IndexToNode(from_index)][manager.IndexToNode(to_index)] * 1000)

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

    solution = routing.SolveWithParameters(search_parameters)

    route = []
    if solution:
        index = routing.Start(0)
        while not routing.IsEnd(index):
            route.append(manager.IndexToNode(index))
            index = solution.Value(routing.NextVar(index))
        route.append(manager.IndexToNode(index))
    return route

def process_all_matrices():
    input_dir = Path("data") / "matrices"
    output_path = Path("output") / "rutas_ordenadas.json"
    result = {}

    for filepath in input_dir.glob("*.json"):
        with filepath.open("r", encoding="utf-8") as file:
            data = json.load(file)
            matrix, coords = create_distance_matrix(data)
            route_indices = solve_tsp(matrix)
            ordered_coords = [coords[i] for i in route_indices if coords[i] != 'origen']
            result[filepath.stem] = ordered_coords

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print(f"✅ Rutas ordenadas guardadas en '{output_path}'")
