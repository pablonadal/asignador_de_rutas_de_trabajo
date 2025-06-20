estructura de carpeta y archivos:

a tener en cuenta:
tokens y url de distintas apis actualizadas para usar las versiones gratuitas



asignador_de_rutas_de_trabajo/
## 📁 Estructura del Proyecto

```plaintext
.
├── 🛠️ config/
│   └── 📄 db_config.py              # Configuración de conexión a la base de datos
│
├── 📂 data/
│   ├── 📁 matrices/
│   │   ├── 📄 grupo1_matriz.json    # Matriz de distancias del grupo 1
│   │   ├── 📄 grupo2_matriz.json    # Matriz de distancias del grupo 2
│   ├── 📄 coordenadas_por_fecha.csv # Coordenadas extraídas por rango de fechas
│   ├── 📄 coordenadas_raw.csv       # Coordenadas originales sin procesar
│   ├── 📄 grupos_con_motivos.csv    # Datos agrupados con motivo asignado
│   ├── 📄 grupos_kmeans.txt         # Resultados del clustering KMeans
│   ├── 🌐 mapa.html                 # Visualización interactiva de las rutas
│   └── 📄 resultados_con_tiempos.csv # Dataset final con tiempos estimados
│
├── 📤 output/
│   ├── 📁 visualizaciones/
│   │   └── 🖼️ Figure_1.png          # Imagen generada del análisis
│   ├── 📄 rutas_ordenadas.csv       # Rutas en orden óptimo
│   ├── 📄 rutas_ordenadas.json      # Rutas ordenadas en formato JSON
│   ├── 📄 urls_generadas.csv        # URLs generadas para seguimiento
│   └── 📄 urls_google_maps.json     # URLs en formato Google Maps
│
├── ⚙️ utils/
│   ├── 🧩 db_queries/
│   │   ├── 📄 get_coordinates_by_date.py       # Consulta coordenadas por fecha
│   │   ├── 📄 get_coordinates.py               # Obtiene coordenadas generales
│   │   └── 📄 asignar_tiempoyhora_estimado.py  # Asigna tiempos estimados por orden
│   ├── 📄 clustering.py               # Lógica para clustering de coordenadas
│   ├── 📄 distance_matrix.py         # Cálculo de matrices de distancia
│   ├── 📄 enviar_email_horadellegada.py # Envía emails con hora de llegada
│   ├── 📄 enviar_urls_whsp.py        # Envía URLs por WhatsApp
│   ├── 📄 helpers.py                 # Funciones auxiliares
│   ├── 📄 maps_url_generator.py      # Generador de enlaces de mapas
│   └── 📄 routing_solver.py          # Solver del problema de ruteo (TSP)
│
├── 🔐 .env                 # Variables de entorno (API keys, config)
├── 📄 .gitignore           # Archivos y carpetas a ignorar por Git
├── 🚀 main.py              # Script principal del proyecto
├── 📘 README.md            # Documentación general del proyecto
└── 📦 requirements.txt     # Dependencias necesarias (pip)
