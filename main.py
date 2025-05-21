from utils.db_queries.get_coordinates_by_date import get_coordinates_by_date_range

if __name__ == "__main__":
    get_coordinates_by_date_range('2025-05-04', '2025-05-04', 'data/coordenadas_por_fecha.csv')
