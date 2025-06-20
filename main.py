from pathlib import Path

from utils.db_queries.get_coordinates_by_date import get_coordinates_by_date_range
from utils.clustering import clustering_geografico_kmeans
from utils.distance_matrix import procesar_grupos_y_guardar_matrices
from utils.routing_solver import process_all_matrices
from utils.maps_url_generator import generar_urls_google_maps
from utils.helpers import asignar_motivos_a_grupos
from utils.asignar_tiempoyhora_estimado import asignar_tiempos_estimados_a_destinos
from utils.enviar_email_horadellegada import enviar_notificaciones_email
from utils.enviar_urls_wsp import enviar_urls_whatsapp

if __name__ == "__main__":

    # Definir rutas usando Path (compatibles con todos los SO)
    path_coords_csv = Path("data") / "coordenadas_por_fecha.csv"
    path_kmeans_txt = Path("data") / "grupos_kmeans.txt"
    path_rutas_json = Path("output") / "rutas_ordenadas.json"
    path_grupos_motivos_csv = Path("data") / "grupos_con_motivos.csv"
    path_urls_json = Path("output") / "urls_google_maps.json"
    path_resultados_csv = Path("data") / "resultados_con_tiempos.csv"

    # # obtener coordenadas desde la base de datos entre dos fechas y guardar en dataframe y CSV
    # df_coords = get_coordinates_by_date_range('2025-05-04', '2025-05-04', output_path=path_coords_csv)
    # print(df_coords.head())

    # # aplicar clustering KMeans y guardar en archivo TXT
    # clustering_geografico_kmeans(path_coords_csv, n_clusters=5)
    # print(f"Clustering KMeans aplicado y grupos guardados en '{path_kmeans_txt}'")

    # procesar grupos y guardar matrices de distancia en json
    procesar_grupos_y_guardar_matrices(path_kmeans_txt, "-34.641042,-68.339570")
    print("Matrices de distancia procesadas y guardadas en 'data/matrices'")

    # resolver TSP con OR-Tools para todas las matrices y guardar rutas ordenadas en JSON
    process_all_matrices()
    print(f"Matrices procesadas y rutas ordenadas guardadas en '{path_rutas_json}'")

    # asignar motivos a grupos y guardar en CSV
    asignar_motivos_a_grupos(path_rutas_json, path_coords_csv)
    print(f"Motivos asignados a grupos y guardados en '{path_grupos_motivos_csv}'")

    # generar URLs de Google Maps a partir de las rutas ordenadas
    generar_urls_google_maps(path_rutas_json, path_urls_json)
    print("Proceso completado. URLs generadas.")

    # asignar a cada destino un tiempo de llegada estimado y guardar en CSV
    asignar_tiempos_estimados_a_destinos(path_grupos_motivos_csv)
    print(f"Tiempos y hora estimados asignados a destinos y guardados en '{path_resultados_csv}'")

    # Enviar notificaciones por email
    enviar_notificaciones_email(path_resultados_csv)
    print("Notificaciones enviadas por email (si está configurado).")

    # Enviar urls de google maps a los tecnicos por whatsapp
    enviar_urls_whatsapp(path_urls_json)
    print("URLs de Google Maps enviadas por WhatsApp.")
