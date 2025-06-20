import pandas as pd
import numpy as np
import requests
import time
from datetime import datetime, timedelta
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY_DM")

def asignar_tiempos_estimados_a_destinos(
    csv_path,
    output_path="data/resultados_con_tiempos.csv",
    api_key=API_KEY
):
    # Convertir a objetos Path (por si se pasan como string)
    csv_path = Path(csv_path)
    output_path = Path(output_path)

    # Leer el CSV
    df = pd.read_csv(csv_path)

    # Tiempos por motivo
    tiempos_por_motivo = {
        "MUDANZA": 25,
        "NO ENCONTRADO": 20,
        "motivo_desconocido": 20
    }

    # Asignar entre 15 y 35 mins a motivos nuevos
    for motivo in df['motivoordnombre'].dropna().unique():
        if motivo not in tiempos_por_motivo:
            tiempos_por_motivo[motivo] = np.random.randint(15, 36)

    df["tiempo_estimado_llegada"] = 0

    for grupo in df["grupo"].unique():
        sub = df[df["grupo"] == grupo]
        tiempo_acum = 0
        for i in range(len(sub)):
            idx = sub.index[i]
            if i == 0:
                df.at[idx, "tiempo_estimado_llegada"] = 0
                continue

            o = f"{sub.iloc[i-1]['latitud']},{sub.iloc[i-1]['longitud']}"
            d = f"{sub.iloc[i]['latitud']},{sub.iloc[i]['longitud']}"

            if api_key:
                url = (
                    f"https://api.distancematrix.ai/maps/api/distancematrix/json"
                    f"?origins={o}&destinations={d}&key={api_key}"
                )
                try:
                    rsp = requests.get(url)
                    data = rsp.json()
                    print(data)
                    elem = data["rows"][0]["elements"][0]
                    if elem.get("status") == "OK":
                        dur_seg = elem["duration"]["value"]
                        tiempo_viaje = dur_seg / 60
                    else:
                        print(f"⚠️ Ruta no encontrada: {elem.get('status')}. Simulo tiempo.")
                        tiempo_viaje = np.random.randint(5, 16)
                except Exception as e:
                    print(f"❌ Error API: {e}. Simulo tiempo.")
                    tiempo_viaje = np.random.randint(5, 16)

                time.sleep(1)
            else:
                tiempo_viaje = np.random.randint(5, 16)
                print(f"⚠️ API_KEY no configurada. Simulo tiempo de {tiempo_viaje} mins.")

            motivo = sub.iloc[i]["motivoordnombre"]
            t_mot = tiempos_por_motivo.get(motivo, tiempos_por_motivo["motivo_desconocido"])
            tiempo_acum += tiempo_viaje + t_mot
            df.at[idx, "tiempo_estimado_llegada"] = int(tiempo_acum)

    # Hora partida 09:00
    inicio = datetime.strptime("09:00", "%H:%M")
    df["hora_estimada_llegada"] = df["tiempo_estimado_llegada"].apply(
        lambda m: (inicio + timedelta(minutes=m)).strftime("%H:%M")
    )

    # Crear carpeta de salida si no existe
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Guardar el archivo
    df.to_csv(output_path, index=False)
    print(f"✅ Resultado guardado en {output_path}")
    return df
