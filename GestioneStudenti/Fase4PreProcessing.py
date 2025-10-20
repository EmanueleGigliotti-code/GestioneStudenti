import pandas as pd
import sqlite3
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

class Preprocessing:
#Legge i dati direttamente dal database studenti.db
    def __init__(self, db_path="studenti.db"):
        conn = sqlite3.connect(db_path)
        self.df = pd.read_sql_query("SELECT * FROM studenti", conn)
        conn.close()
        self.df_original = self.df.copy()
        # print(self.df_original.loc[47])
        # print(self.df_original.loc[106])
        # print(self.df_original.loc[90])
        # print(self.df_original.loc[12])

    def codifica_label(self):
# Utilizzo il get_dummies sulle colonna comportamento in modo tale che mi va a creare le altre colonne con buono, ottimo ecc.. con prefisso comportamento e mi va ad inserire 0 e 1 se è presente o meno
        comportamento_dummies = pd.get_dummies(self.df["comportamento"], prefix="comportamento").astype(int)
# Qui concateno alla tabella le colonne
        self.df = pd.concat([self.df, comportamento_dummies], axis=1)
    
        self.df['genere_num'] = self.df['genere'].map({'M': 1, 'F': 0})
        self.df['esito_finale_num'] = self.df['esito_finale'].map({'Promosso': 1, 'Bocciato': 0})

    def split_train_test(self, test_size=0.2, random_state=42):
#Costruisco la lista delle colonne da usare come input (feature_cols). Dichiaro una variabile col e tramite un ciclo vado a prendere tutte le altre colonne che iniziano con comportamento_ dichiarate dal Onehotencoder
        feature_cols = ["eta", "ore_studio", "assenze", "media_voti", "genere_num"] + \
                       [col for col in self.df.columns if col.startswith("comportamento_")]

        X = self.df[feature_cols] #Colonne input
        y = self.df["esito_finale_num"] #Target

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )

    def normalizza(self):
#Normalizzo le variabili numeriche tra 0 e 1 
        scaler = MinMaxScaler()
#Lista delle colonne numeriche da normalizzare
        num_cols = ["eta", "ore_studio", "assenze", "media_voti"]

        self.X_train[num_cols] = scaler.fit_transform(self.X_train[num_cols])
        self.X_test[num_cols] = scaler.transform(self.X_test[num_cols])

        self.scaler = scaler

    def salva_csv(self, prefix="dataset"):
#Salva i DataFrame in CSV per debug
        self.X_train.to_csv(f"{prefix}_X_train.csv", index=False)
        self.X_test.to_csv(f"{prefix}_X_test.csv", index=False)
        self.y_train.to_csv(f"{prefix}_y_train.csv", index=False)
        self.y_test.to_csv(f"{prefix}_y_test.csv", index=False)
        print(f"CSV salvati")

    def preprocess(self, test_size=0.2, random_state=42, salva=True, prefix="dataset"):
#Esegue tutte le fasi: codifica, split, normalizzazione e salvataggio
        self.codifica_label()
        self.split_train_test(test_size=test_size, random_state=random_state)
        self.normalizza()
        if salva:
            self.salva_csv(prefix=prefix)

prep = Preprocessing("studenti.db")
prep.preprocess()

print(prep.X_train.head())
print(prep.y_train.head())


