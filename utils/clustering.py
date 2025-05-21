import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def clustering_geografico_kmeans(df, n_clusters=3, plot=True):
    """
    Aplica clustering K-Means sobre coordenadas geográficas.
    
    Parámetros:
    - df: DataFrame con columnas 'longitud' y 'latitud'
    - n_clusters: número de clusters deseados (default: 3)
    - plot: si True, muestra un gráfico de los clusters

    Devuelve:
    - df_clean: DataFrame sin valores nulos con una columna 'cluster'
    """
    if not {'longitud', 'latitud'}.issubset(df.columns):
        raise ValueError("El DataFrame debe contener las columnas 'longitud' y 'latitud'.")

    df_clean = df[['longitud', 'latitud']].dropna().copy()

    scaler = StandardScaler()
    coords_scaled = scaler.fit_transform(df_clean)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df_clean['cluster'] = kmeans.fit_predict(coords_scaled)

    if plot:
        plt.figure(figsize=(10, 6))
        plt.scatter(df_clean['longitud'], df_clean['latitud'], c=df_clean['cluster'], cmap='viridis', s=50)
        plt.xlabel('Longitud')
        plt.ylabel('Latitud')
        plt.title(f'Clustering geográfico con K-Means ({n_clusters} clusters)')
        plt.grid(True)
        plt.show()
        # Guardar los grupos en un archivo TXT
    # Guardar los grupos en un archivo TXT
    with open("data\\grupos_kmeans.txt", "w") as f:
        for cluster_id in sorted(df_clean['cluster'].unique()):
            f.write(f"Grupo {cluster_id}:\n")
            grupo = df_clean[df_clean['cluster'] == cluster_id]
            for _, row in grupo.iterrows():
                f.write(f"  - Longitud: {row['longitud']}, Latitud: {row['latitud']}\n")
            f.write("\n")
    
    
    print("Grupos guardados en 'data\\grupos_kmeans.txt'")
    return df_clean
