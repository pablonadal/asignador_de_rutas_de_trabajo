import json
import pandas as pd
from pathlib import Path

def asignar_motivos_a_grupos(json_path, csv_path, output_path="data/grupos_con_motivos.csv"):
    # Convertir a objetos Path
    json_path = Path(json_path)
    csv_path = Path(csv_path)
    output_path = Path(output_path)

    # Cargar JSON
    with json_path.open("r", encoding="utf-8") as f:
        grupos = json.load(f)

    # Cargar CSV
    df = pd.read_csv(csv_path)

    # Verificar columnas necesarias
    required_cols = {"longitud", "latitud", "motivoordnombre"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"Faltan columnas necesarias en el CSV: {required_cols - set(df.columns)}")

    # Crear columna de coordenadas unificadas como string
    df["coord_str"] = df["latitud"].astype(str).str.strip() + "," + df["longitud"].astype(str).str.strip()

    filas_resultado = []

    for grupo_nombre, coordenadas in grupos.items():
        for coord in coordenadas:
            filas = df[df["coord_str"] == coord]
            if not filas.empty:
                for _, row in filas.iterrows():
                    filas_resultado.append({
                        "grupo": grupo_nombre,
                        "longitud": row["longitud"],
                        "latitud": row["latitud"],
                        "motivoordnombre": row["motivoordnombre"]
                    })
            else:
                lat, lon = coord.split(",")
                filas_resultado.append({
                    "grupo": grupo_nombre,
                    "longitud": lon.strip(),
                    "latitud": lat.strip(),
                    "motivoordnombre": "NO ENCONTRADO"
                })

    # Asegurar que la carpeta existe
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Guardar resultado
    pd.DataFrame(filas_resultado).to_csv(output_path, index=False, encoding="utf-8")
    print(f"✅ Resultado guardado en '{output_path}'")

# Si querés que se ejecute directo:
if __name__ == "__main__":
    asignar_motivos_a_grupos("output/rutas_ordenadas.json", "data/coordenadas_por_fecha.csv")
