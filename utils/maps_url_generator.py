import json
import os

def generar_urls_google_maps(path_entrada: str, path_salida: str):
    # Cargar las rutas ordenadas por grupo
    with open(path_entrada, 'r', encoding='utf-8') as f:
        rutas_por_grupo = json.load(f)

    urls_generadas = {}

    for grupo, coordenadas in rutas_por_grupo.items():
        if len(coordenadas) < 2:
            print(f"[ADVERTENCIA] Grupo {grupo} tiene menos de 2 puntos. Se omite.")
            continue
        
        # Generar la URL concatenando las coordenadas como paradas
        url = "https://www.google.com/maps/dir/" + "/".join(coordenadas)
        urls_generadas[grupo] = url

    # Crear la carpeta de salida si no existe
    os.makedirs(os.path.dirname(path_salida), exist_ok=True)

    # Guardar URLs generadas en archivo JSON
    with open(path_salida, 'w', encoding='utf-8') as f:
        json.dump(urls_generadas, f, indent=4, ensure_ascii=False)

    print(f"✅ URLs generadas guardadas en: {path_salida}")

if __name__ == "__main__":
    input_path = "output/rutas_ordenadas.json"
    output_path = "output/urls_google_maps.json"
    
    generar_urls_google_maps(input_path, output_path)
    print("Proceso completado. URLs generadas.")