from utils.db_queries.get_coordinates_by_date import get_coordinates_by_date_range
from utils.clustering import clustering_geografico_kmeans
from utils.distance_matrix import procesar_grupos_y_guardar_matrices


if __name__ == "__main__":

    # obtener coordenadas entre dos fechas y guardar en dataframe y CSV
    df_coords = get_coordinates_by_date_range('2025-05-04', '2025-05-04')
    print(df_coords.head())

    # aplicar clustering KMeans y guardar en archivo TXT
    clustering_geografico_kmeans(df_coords, n_clusters=5)
    print("Clustering KMeans aplicado y grupos guardados en 'data/grupos_kmeans.txt'")

    # procesar grupos y guardar matrices de distancia
    procesar_grupos_y_guardar_matrices("data\grupos_kmeans.txt", "-34.641042,-68.339570")
    print("Matrices de distancia procesadas y guardadas en 'data/matrices'")