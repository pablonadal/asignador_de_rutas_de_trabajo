from fastapi import FastAPI, Query
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

app = FastAPI()

# Rutas estándar
path_coords_csv = Path("data") / "coordenadas_por_fecha.csv"
path_kmeans_txt = Path("data") / "grupos_kmeans.txt"
path_rutas_json = Path("output") / "rutas_ordenadas.json"
path_grupos_motivos_csv = Path("data") / "grupos_con_motivos.csv"
path_urls_json = Path("output") / "urls_google_maps.json"
path_resultados_csv = Path("data") / "resultados_con_tiempos.csv"

def esperar_archivo(path: Path, timeout: int = 10):
    inicio = time.time()
    while not path.exists():
        if time.time() - inicio > timeout:
            raise TimeoutError(f"⛔ Tiempo agotado: el archivo {path} no fue encontrado.")
        print(f"⏳ Esperando archivo: {path}...")
        time.sleep(0.5)

@app.get("/")
def home():
    return {"mensaje": "API de asignación de rutas activa"}

@app.post("/obtener-coordenadas")
def obtener_coordenadas(fecha_inicio: str = Query(...), fecha_fin: str = Query(...)):
    df_coords = get_coordinates_by_date_range(fecha_inicio, fecha_fin, output_path=path_coords_csv)
    if df_coords.empty:
        return {"estado": "⚠️ No se obtuvieron coordenadas desde la base"}
    return {"estado": "✅ Coordenadas obtenidas", "cantidad": len(df_coords)}

@app.post("/clustering")
def clustering(n_clusters: int = 5):
    clustering_geografico_kmeans(path_coords_csv, n_clusters=n_clusters)
    return {"estado": "Clustering realizado"}

@app.post("/procesar-matrices")
def procesar_matrices(origen: str = "-34.641042,-68.339570"):
    esperar_archivo(path_kmeans_txt)
    procesar_grupos_y_guardar_matrices(path_kmeans_txt, origen)
    return {"estado": "Matrices procesadas"}

@app.post("/resolver-rutas")
def resolver_rutas():
    esperar_archivo(Path("data/matrices"))
    process_all_matrices()
    return {"estado": "Rutas optimizadas"}

@app.post("/asignar-motivos")
def asignar_motivos():
    esperar_archivo(path_rutas_json)
    asignar_motivos_a_grupos(path_rutas_json, path_coords_csv)
    return {"estado": "Motivos asignados"}

@app.post("/generar-urls")
def generar_urls():
    esperar_archivo(path_grupos_motivos_csv)
    generar_urls_google_maps(path_rutas_json, path_urls_json)
    return {"estado": "URLs generadas"}

@app.post("/asignar-tiempos")
def asignar_tiempos():
    esperar_archivo(path_urls_json)
    asignar_tiempos_estimados_a_destinos(path_grupos_motivos_csv)
    return {"estado": "Tiempos estimados asignados"}

@app.post("/notificar-email")
def notificar_email():
    esperar_archivo(path_resultados_csv)
    enviar_notificaciones_email(path_resultados_csv)
    return {"estado": "Emails enviados"}

@app.post("/notificar-whatsapp")
def notificar_whatsapp():
    enviar_urls_whatsapp(path_urls_json)
    return {"estado": "WhatsApp enviado"}
