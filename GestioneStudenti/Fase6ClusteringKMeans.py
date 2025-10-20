import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import pandas as pd
from sklearn.preprocessing import StandardScaler

class ClusteringKMeans:
#Passo il db e faccio una copia. Inizializzo self.features che sono le colonne che vado a selezionare per il clustering. self.kmeans oggetto di KMeans addestrato e self.labels cluster per ogni studente
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.features = None
        self.scaler = StandardScaler()
        self.kmeans = None
        self.labels = None

#Vado ad estrarre le colonne che mi servono e le normalizzo
    def seleziona_features(self, colonne):
        self.features = self.df[colonne]
        self.features = self.scaler.fit_transform(self.features)
        print(f"Colonne scalate: {colonne}")

    def esegui(self, n_clusters=3, random_state=42):
        if self.features is None:
            raise ValueError("Selezionare features.")
#Creo l'oggetto kmeans
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init="auto")
        self.labels = self.kmeans.fit_predict(self.features)
        self.df["cluster"] = self.labels
        print(f"Clustering completato con {n_clusters} cluster.")
#Ritorno il df aggiornato
        return self.df

#Gli passo tra i parametri le due colonne
    def grafico_dispersione(self, x_col, y_col, color_col=None):
        if self.labels is None:
            raise ValueError("Bisogna eseguire prima.")
        plt.figure(figsize=(8,6))
        if color_col:
            plt.scatter(
                self.df[x_col], self.df[y_col], c=self.df[color_col],
                cmap="coolwarm", alpha=0.7, s=80
            )
            plt.colorbar(label=color_col)
        else:
            plt.scatter(self.df[x_col], self.df[y_col], c=self.labels, cmap="viridis", alpha=0.6)
            plt.colorbar(label="Cluster")
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.title(f"Clustering KMeans - x:{x_col} y:{y_col}")
        plt.show()

    def grafico_gomito(self, max_k=10):
        if self.features is None:
            raise ValueError("Seleziona features.")
#somma delle distanze quadrate tra i punti e il centroide del loro cluster, più basso è il valore di inertia, più i punti sono vicini al centro del loro cluster.
        inertia = []
#provo diversi numeri di cluster, da 2 fino a max_k.
        for k in range(2, max_k+1):
            km = KMeans(n_clusters=k, random_state=42, n_init=10)
#Addestro il modello sui dati selezionati
            km.fit(self.features)
#valore di inertia del modello appena addestrato, cioè quanto i punti sono vicini ai loro centroidi.
            inertia.append(km.inertia_)
        plt.figure(figsize=(8,6))
        plt.plot(range(2, max_k+1), inertia, marker="o")
        plt.xlabel("Numero cluster (k)")
        plt.ylabel("Inertia")
        plt.title("Metodo del gomito")
        plt.show()
        
from Fase4PreProcessing import Preprocessing  

prep = Preprocessing("studenti.db")
prep.preprocess(salva=False)

clust = ClusteringKMeans(prep.X_train)

# Lista delle feature da aggiungere progressivamente
feature_sequence = [
    ["media_voti", "assenze"],                 # performance e assenze
    ["media_voti", "assenze", "ore_studio"],  #  aggiunta ore studio
    ["media_voti", "assenze", "ore_studio", "eta"],  # aggiunta eta
    ["media_voti", "assenze", "ore_studio", "eta", "genere_num"],  # aggiunta genere
    ["media_voti", "assenze", "ore_studio", "eta", "genere_num"] + 
        [col for col in prep.X_train.columns if col.startswith("comportamento_")]  # passo 5: aggiunta comportamento OneHotEncoder
]

for i, cols in enumerate(feature_sequence, start=1):
    print(f"\n--- Clustering con passo {i}: feature {cols} ---")
    clust.seleziona_features(cols)
    df_cluster = clust.esegui(n_clusters=3)
    # Se c'è una feature nuova rispetto al passo precedente, la usiamo per il colore
    if i == 1:
        clust.grafico_dispersione(cols[0], cols[1])
    else:
        nuova_feat = cols[-1]  # ultima feature aggiunta
        clust.grafico_dispersione(cols[0], cols[1], color_col=nuova_feat)

# Grafico del gomito con le ultime feature selezionate
clust.grafico_gomito(max_k=8)

