from config.db_config import get_db_connection
import csv
import os

def get_coordinates_by_date_range(start_date, end_date, output_path='data/coordenadas_por_fecha.csv'):
    query = """
        SELECT clientecordx AS longitud, clientecordy AS latitud
        FROM ordenes_filtradas
        WHERE fecha BETWEEN %s AND %s
    """

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, (start_date, end_date))
        rows = cursor.fetchall()

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['longitud', 'latitud'])
            writer.writerows(rows)

        print(f"Coordenadas entre {start_date} y {end_date} guardadas en {output_path}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
