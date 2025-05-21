from utils.db_queries.get_coordinates_by_date import get_coordinates_by_date_range
from utils.clustering import clustering_geografico_kmeans


if __name__ == "__main__":

    # obtener coordenadas entre dos fechas y guardar en dataframe y CSV
    df_coords = get_coordinates_by_date_range('2025-05-04', '2025-05-04')
    print(df_coords.head())

    clustering_geografico_kmeans(df_coords, n_clusters=5)