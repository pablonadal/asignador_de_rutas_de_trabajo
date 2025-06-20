import json
import re
from pathlib import Path
from dotenv import load_dotenv
import requests
import os

def obtener_matriz_completa(origen: str, destinos: list[str]):
    load_dotenv()
    api_key = os.getenv("API_KEY_DM")

    if not api_key:
        raise ValueError("No se encontró la variable API_KEY_DM en el archivo .env")

    ubicaciones = [origen] + destinos
    matriz_resultado = []

    for i, origen_actual in enumerate(ubicaciones):
        destinos_str = "|".join(ubicaciones)

        url = (
            f"https://api.distancematrix.ai/maps/api/distancematrix/json"
            f"?origins={origen_actual}"
            f"&destinations={destinos_str}"
            f"&key={api_key}"
        )

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            fila = []
            for j, element in enumerate(data["rows"][0]["elements"]):
                distancia_texto = element.get("distance", {}).get("text", "0 km")
                fila.append(distancia_texto)

            matriz_resultado.append(fila)

        except Exception as e:
            print(f"❌ Error al obtener distancias desde {origen_actual}: {e}")
            return []

    return {
        "coordenadas": ubicaciones,
        "matriz": matriz_resultado
    }


def limpiar_carpeta(carpeta: Path):
    if carpeta.exists() and carpeta.is_dir():
        for archivo in carpeta.iterdir():
            if archivo.is_file():
                archivo.unlink()


def procesar_grupos_y_guardar_matrices(archivo_txt: str, origen: str, carpeta_salida: str = "data/matrices"):
    carpeta_salida = Path(carpeta_salida)
    carpeta_salida.mkdir(parents=True, exist_ok=True)

    limpiar_carpeta(carpeta_salida)

    archivo_txt = Path(archivo_txt)
    with archivo_txt.open("r", encoding="utf-8") as file:
        contenido = file.read()

    grupos = re.findall(r"(grupo\d+)\s*=\s*\[(.*?)\]", contenido, re.DOTALL)

    for nombre_grupo, coordenadas_raw in grupos:
        coordenadas = re.findall(r'"(.*?)"', coordenadas_raw)
        print(f"🔄 Procesando {nombre_grupo} con {len(coordenadas)} destinos...")

        matriz = obtener_matriz_completa(origen, coordenadas)

        ruta_archivo = carpeta_salida / f"{nombre_grupo}_matriz.json"
        with ruta_archivo.open("w", encoding="utf-8") as f:
            json.dump(matriz, f, indent=2, ensure_ascii=False)

        print(f"✅ {nombre_grupo} guardado en {ruta_archivo}")
