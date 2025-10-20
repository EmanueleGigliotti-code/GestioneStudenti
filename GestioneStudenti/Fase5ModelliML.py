from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib

class ModelliML:
#Gli passo al costruttore i dati già processati della classe Preprocessing.
    def __init__(self, X_train, X_test, y_train, y_test):
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
#Creo una lista dizionario di chiave valore con i seguenti modelli
        self.modelli = {
            "DecisionTree": DecisionTreeClassifier(random_state=42),
# n_neighbors=5 per classificare un nuovo punto guarda le 5 istanze più vicine.
            "KNN": KNeighborsClassifier(n_neighbors=5),
            "NaiveBayes": GaussianNB(),
            "SVM": SVC(kernel="linear", probability=True, random_state=42),
            "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42)
        }
        self.risultati = {}

    def allena_valuta(self):    
#Eseguo un ciclo for che mi permette di scorrere tutti i modelli del dizionario. Nome= nome modello, modello= istanza del classificatore
        for nome, modello in self.modelli.items():
            print(f"\nAddestramento modello: {nome}...")
#Gli passo le caratteristiche di X_train e le etichette di y_train (Promosso o bocciato)
            modello.fit(self.X_train, self.y_train)  # allena il modello
            y_pred = modello.predict(self.X_test)    # Qui il modello già addestrato fa previsioni su X_test(Dati nuovi) e produce etichette se è promosso o bocciato

            # Faccio un confronto con le etichette reali e quelle previste dal modello 
            acc = accuracy_score(self.y_test, y_pred) #Percentuale di predizioni corrette
            cm = confusion_matrix(self.y_test, y_pred) # Tabella che mostra errori e corretti per classe.
            report = classification_report(self.y_test, y_pred, zero_division=0)

            # salvo risultati in un dizionario per poi stamparli dopo e per il confronto
            self.risultati[nome] = {
                "accuracy": acc,
                "confusion_matrix": cm,
                "report": report
            }

            print(f"{nome} - Accuratezza: {acc:.2f}")
            print("Matrice di confusione:\n", cm)
            print("Report:\n", report)

#Metodo per salvare il modello
    def salva_modello(self, nome_modello, filename):
        if nome_modello in self.modelli:
            joblib.dump(self.modelli[nome_modello], filename)
            print(f"Modello {nome_modello} salvato in {filename}")
        else:
            print(f"Modello {nome_modello} non trovato!")

#Stampo il nome e l'accuratezza del modello
    def confronto(self):
        print("\nConfronto finale tra modelli:")
        for nome, res in self.risultati.items():
            print(f"{nome}: {res['accuracy']:.2f}")


from Fase4PreProcessing import Preprocessing  

prep = Preprocessing("studenti.db")
prep.preprocess()

ml = ModelliML(prep.X_train, prep.X_test, prep.y_train, prep.y_test)
ml.allena_valuta()
ml.confronto()
ml.salva_modello("RandomForest", "randomforest_model.pkl")
