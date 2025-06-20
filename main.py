from pathlib import Path
import time
from utils.db_queries.get_coordinates_by_date import get_coordinates_by_date_range
from utils.clustering import clustering_geografico_kmeans
from utils.distance_matrix import procesar_grupos_y_guardar_matrices
from utils.routing_solver import process_all_matrices
from utils.maps_url_generator import generar_urls_google_maps
from utils.helpers import asignar_motivos_a_grupos
from utils.asignar_tiempoyhora_estimado import asignar_tiempos_estimados_a_destinos
from utils.enviar_email_horadellegada import enviar_notificaciones_email
from utils.enviar_urls_wsp import enviar_urls_whatsapp


def esperar_archivo(path: Path, timeout: int = 10):
    """Espera hasta que el archivo exista en disco o se agote el tiempo."""
    inicio = time.time()
    while not path.exists():
        if time.time() - inicio > timeout:
            raise TimeoutError(f"⛔ Tiempo de espera agotado: el archivo {path} no fue encontrado.")
        print(f"⏳ Esperando a que se cree: {path}...")
        time.sleep(0.5)


if __name__ == "__main__":
    # Definir rutas usando Path (compatibles con todos los SO)
    path_coords_csv = Path("data") / "coordenadas_por_fecha.csv"
    path_kmeans_txt = Path("data") / "grupos_kmeans.txt"
    path_rutas_json = Path("output") / "rutas_ordenadas.json"
    path_grupos_motivos_csv = Path("data") / "grupos_con_motivos.csv"
    path_urls_json = Path("output") / "urls_google_maps.json"
    path_resultados_csv = Path("data") / "resultados_con_tiempos.csv"

    # # Obtener coordenadas desde la base de datos entre dos fechas
    # df_coords = get_coordinates_by_date_range('2025-05-04', '2025-05-04', output_path=path_coords_csv)

    # if df_coords.empty:
    #     print("⚠️ No se obtuvieron coordenadas desde la base. Abortando ejecución.")
    #     exit(1)

    # print(df_coords.head())

    # # Asegurar que el archivo existe antes de seguir
    # esperar_archivo(path_coords_csv)

    # # Aplicar clustering KMeans y guardar en archivo TXT
    # clustering_geografico_kmeans(path_coords_csv, n_clusters=5)
    # print(f"Clustering KMeans aplicado y grupos guardados en '{path_kmeans_txt}'")

    # Esperar a que se cree el archivo de grupos KMeans
    esperar_archivo(path_kmeans_txt)
    # Procesar grupos y guardar matrices de distancia
    procesar_grupos_y_guardar_matrices(path_kmeans_txt, "-34.641042,-68.339570")
    print("Matrices de distancia procesadas y guardadas en 'data/matrices'")

    # Esperar a que se creen las matrices de distancia
    esperar_archivo(Path("data/matrices"))
    # Resolver TSP y guardar rutas ordenadas
    process_all_matrices()
    print(f"Matrices procesadas y rutas ordenadas guardadas en '{path_rutas_json}'")

    # Esperar a que se cree el archivo de rutas ordenadas
    # esperar_archivo(path_coords_csv)
    # Asignar motivos por grupo
    esperar_archivo(path_rutas_json)
    asignar_motivos_a_grupos(path_rutas_json, path_coords_csv)
    print(f"Motivos asignados a grupos y guardados en '{path_grupos_motivos_csv}'")

    # Esperar a que se cree el archivo de grupos con motivos
    esperar_archivo(path_grupos_motivos_csv)
    # Generar URLs de Google Maps
    generar_urls_google_maps(path_rutas_json, path_urls_json)
    print("Proceso completado. URLs generadas.")

    # Esperar a que se creen las URLs de Google Maps
    esperar_archivo(path_urls_json)
    # Asignar tiempos estimados y guardar CSV
    asignar_tiempos_estimados_a_destinos(path_grupos_motivos_csv)
    print(f"Tiempos y hora estimados asignados a destinos y guardados en '{path_resultados_csv}'")

    # Esperar a que se cree el archivo de resultados con tiempos
    esperar_archivo(path_resultados_csv)
    # Enviar notificaciones por email
    enviar_notificaciones_email(path_resultados_csv)
    print("Notificaciones enviadas por email (si está configurado).")

    # Enviar URLs por WhatsApp
    enviar_urls_whatsapp(path_urls_json)
    print("URLs de Google Maps enviadas por WhatsApp.")
