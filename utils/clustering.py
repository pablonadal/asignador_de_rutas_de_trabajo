import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def clustering_geografico_kmeans(data, n_clusters=3, plot=True):
    if isinstance(data, str):
        df = pd.read_csv(data)
    elif isinstance(data, pd.DataFrame):
        df = data
    else:
        raise TypeError("El parámetro debe ser un DataFrame o la ruta a un archivo CSV.")

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

    with open("data/grupos_kmeans.txt", "w") as f:
        for cluster_id in sorted(df_clean['cluster'].unique()):
            grupo = df_clean[df_clean['cluster'] == cluster_id]
            f.write(f"grupo{cluster_id + 1} = [\n")
            for _, row in grupo.iterrows():
                f.write(f'    "{row["latitud"]:.6f},{row["longitud"]:.6f}",\n')
            f.write("]\n\n")

    print("Grupos guardados en 'data/grupos_kmeans.txt'")
    return df_clean
