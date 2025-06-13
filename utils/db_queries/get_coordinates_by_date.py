from config.db_config import get_db_connection
import pandas as pd
import os

def get_coordinates_by_date_range(start_date, end_date, output_path='data/coordenadas_por_fecha.csv'):
    query = """
        SELECT clientecordx AS longitud, clientecordy AS latitud, motivoordnombre
        FROM ordenes_filtradas
        WHERE fecha BETWEEN %s AND %s
    """

    df = pd.DataFrame()

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, (start_date, end_date))
        rows = cursor.fetchall()

        # Crear DataFrame con motivo
        df = pd.DataFrame(rows, columns=['longitud', 'latitud', 'motivoordnombre'])

        # Eliminar duplicados que tienen misma coord + mismo motivo
        df = df.drop_duplicates(subset=['longitud', 'latitud', 'motivoordnombre'])

        # Crear carpeta si no existe
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Guardar como CSV
        df.to_csv(output_path, index=False, encoding='utf-8')

        print(f"Coordenadas únicas entre {start_date} y {end_date} guardadas en {output_path}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

    return df
