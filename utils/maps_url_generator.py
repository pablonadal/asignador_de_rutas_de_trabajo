import json
from pathlib import Path

def generar_urls_google_maps(path_entrada: str, path_salida: str):
    # Convertir a Path
    path_entrada = Path(path_entrada)
    path_salida = Path(path_salida)

    # Cargar las rutas ordenadas por grupo
    with path_entrada.open('r', encoding='utf-8') as f:
        rutas_por_grupo = json.load(f)

    urls_generadas = {}

    for grupo, coordenadas in rutas_por_grupo.items():
        if len(coordenadas) < 2:
            print(f"[ADVERTENCIA] Grupo {grupo} tiene menos de 2 puntos. Se omite.")
            continue
        
        url = "https://www.google.com/maps/dir/" + "/".join(coordenadas)
        urls_generadas[grupo] = url

    # Crear la carpeta de salida si no existe
    path_salida.parent.mkdir(parents=True, exist_ok=True)

    # Guardar URLs generadas en archivo JSON
    with path_salida.open('w', encoding='utf-8') as f:
        json.dump(urls_generadas, f, indent=4, ensure_ascii=False)

    print(f"✅ URLs generadas guardadas en: {path_salida}")

if __name__ == "__main__":
    input_path = "output/rutas_ordenadas.json"
    output_path = "output/urls_google_maps.json"
    
    generar_urls_google_maps(input_path, output_path)
    print("Proceso completado. URLs generadas.")
