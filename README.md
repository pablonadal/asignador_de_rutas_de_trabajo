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


