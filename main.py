from utils.db_queries.get_coordinates_by_date import get_coordinates_by_date_range
from utils.clustering import clustering_geografico_kmeans
from utils.distance_matrix import procesar_grupos_y_guardar_matrices
from utils.routing_solver import process_all_matrices
from utils.maps_url_generator import generar_urls_google_maps


if __name__ == "__main__":

    # obtener coordenadas desde la base de datos entre dos fechas y guardar en dataframe y CSV
    df_coords = get_coordinates_by_date_range('2025-05-04', '2025-05-04')
    print(df_coords.head())

    # aplicar clustering KMeans y guardar en archivo TXT
    clustering_geografico_kmeans("data\coordenadas_por_fecha.csv", n_clusters=5)
    print("Clustering KMeans aplicado y grupos guardados en 'data/grupos_kmeans.txt'")

    # procesar grupos y guardar matrices de distancia en json
    procesar_grupos_y_guardar_matrices("data\grupos_kmeans.txt", "-34.641042,-68.339570")
    print("Matrices de distancia procesadas y guardadas en 'data/matrices'")

    # resolver TSP con OR-Tools para todas las matrices y guardar rutas ordenadas en JSON
    process_all_matrices()
    print("Matrices procesadas y rutas ordenadas guardadas en 'output/rutas_ordenadas.json'")

    # generar URLs de Google Maps a partir de las rutas ordenadas
    generar_urls_google_maps("output/rutas_ordenadas.json", "output/urls_google_maps.json")
    print("Proceso completado. URLs generadas.")