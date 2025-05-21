estructura de carpeta y archivos:

asignador_de_rutas_de_trabajo/
│
├── main.py                        # Script principal que ejecuta todo el flujo
├── .env                           # Variables de entorno (DB, API keys)
├── requirements.txt               # Dependencias del proyecto
├── README.md                      # Documentación del proyecto
│
├── 📁data/
│   ├── coordenadas_raw.csv        # Export opcional desde MySQL (para debug)
│   └── matrices/                  # Matrices de distancia por móvil (JSON/CSV)
│
├── 📁config/
│   └── db_config.py               # Configuración de conexión a MySQL
│
├── 📁utils/
│   ├── db_queries/
│   │   ├── __init__.py
│   │   ├── get_coordinates.py         # Trae solo lat/lon
│   │   ├── get_coordinates_by_date.py # Trae coordenadas por fecha 
│   │   └── get_coordinates_with_tecno.py # Trae coordenadas + tecno
│   ├── db_connection.py           # Función para leer coordenadas desde MySQL
│   ├── clustering.py              # Algoritmo KMeans para agrupar domicilios
│   ├── distance_matrix.py         # Lógica para consultar API de distancia
│   ├── routing_solver.py          # OR-Tools: resolver orden óptimo de visitas
│   ├── maps_url_generator.py      # Generar URL de Google Maps con coordenadas ordenadas
│   └── helpers.py                 # Funciones auxiliares generales
│
├── 📁output/
│   ├── rutas_ordenadas.json       # Rutas resultantes por móvil
│   ├── urls_generadas.csv         # URLs para compartir por móvil
│   └── visualizaciones/           # (Opcional) mapas generados o imágenes


GUIA DE LO QUE SE VA A LOGRAR
1_ clustering geografico
2_ obtener la matriz de distancia para cada vehiculo segun los domicilio asignados por zona
3_ pasarle a OR-Tools esas matrices para que me de el orden optimo de las coordenadas a visitar
4_ finalmente crear una url de maps con las coordenadas en orden para que genera la ruta y compartirla con el tecnico que utilice el vehiculo designado