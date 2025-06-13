import json
import pandas as pd
import os

def asignar_motivos_a_grupos(json_path, csv_path, output_path="data/grupos_con_motivos.csv"):
    # Cargar JSON
    with open(json_path, "r", encoding="utf-8") as f:
        grupos = json.load(f)

    # Cargar CSV
    df = pd.read_csv(csv_path)

    # Asegurar que las columnas necesarias están presentes
    required_cols = {"longitud", "latitud", "motivoordnombre"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"Faltan columnas necesarias en el CSV: {required_cols - set(df.columns)}")

    # Convertir coordenadas del CSV a string con el mismo formato que el JSON
    df["coord_str"] = df["latitud"].astype(str).str.strip() + "," + df["longitud"].astype(str).str.strip()

    # Preparar datos para salida
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
                # Si no se encuentra, igual se puede guardar como sin motivo
                lat, lon = coord.split(",")
                filas_resultado.append({
                    "grupo": grupo_nombre,
                    "longitud": lon.strip(),
                    "latitud": lat.strip(),
                    "motivoordnombre": "NO ENCONTRADO"
                })

    # Guardar nuevo CSV
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pd.DataFrame(filas_resultado).to_csv(output_path, index=False, encoding="utf-8")

# Si querés que esto se ejecute directo:
if __name__ == "__main__":
    asignar_motivos_a_grupos("output/rutas_ordenadas.json", "data/coordenadas_por_fecha.csv")
