from config.db_config import get_db_connection
import pandas as pd
import os

def get_coordinates_by_date_range(start_date, end_date, output_path='data/coordenadas_por_fecha.csv'):
    query = """
        SELECT clientecordx AS longitud, clientecordy AS latitud, motivoordnombre
        FROM ordenes
        WHERE fecha BETWEEN %s AND %s
    """

    df = pd.DataFrame()

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, (start_date, end_date))
        rows = cursor.fetchall()

        df = pd.DataFrame(rows, columns=['longitud', 'latitud', 'motivoordnombre'])
        df = df.drop_duplicates(subset=['longitud', 'latitud', 'motivoordnombre'])

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False, encoding='utf-8')

        print(f"Coordenadas únicas entre {start_date} y {end_date} guardadas en {output_path}")

    except Exception as e:
        print(f"❌ Error al obtener coordenadas: {e}")

    finally:
        if conn:
            cursor.close()
            conn.close()

    return df
