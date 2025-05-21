# utils/db_connection.py
import csv
import os
from config.db_config import get_db_connection

def export_coordinates_to_csv(output_path='data/coordenadas_raw.csv'):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Query para extraer las coordenadas
        query = "SELECT clientecordx AS longitud, clientecordy AS latitud FROM ordenes_filtradas"
        cursor.execute(query)

        rows = cursor.fetchall()

        # Crear carpeta data/ si no existe
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Guardar en CSV
        with open(output_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['longitud', 'latitud'])  # encabezados
            writer.writerows(rows)

        print(f"Coordenadas exportadas a {output_path}")

    except Exception as e:
        print(f"Error al exportar coordenadas: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
