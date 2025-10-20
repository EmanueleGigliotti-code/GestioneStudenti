import csv
from Studente import Studente  

class GestoreStudenti:
    def __init__(self):
        self.studenti = [] 

#Converto una lista self.studenti in oggetti
    def aggiungi_studente(self, studente: Studente):
        self.studenti.append(studente)

#Metodo che serve per generare n studenti casuali
    def genera_studenti_casuali(self, n=1):
        for _ in range(n):
#studente variabile locale che vengono assegnati degli studenti creati nella classe Studente e tramite il metodo aggiungi_studente lo inserisco in lista
            studente = Studente.genera_studente()
            self.aggiungi_studente(studente)

    def salva_csv(self, filename="Studenti.csv"):
        intestazione = ["id","nome","cognome","eta","genere","ore_studio","assenze","media_voti","comportamento","esito_finale"]
        with open(filename, "w", newline="", encoding="utf-8") as f:
#DictWriter è un metodo che mi permette di memorizzare dizionari in un csv
            writer = csv.DictWriter(f, fieldnames=intestazione)
            writer.writeheader()
            for s in self.studenti:
                writer.writerow({
                    "id": s.id,
                    "nome": s.nome,
                    "cognome": s.cognome,
                    "eta": s.eta,
                    "genere": s.genere,
                    "ore_studio": s.ore_studio,
                    "assenze": s.assenze,
                    "media_voti": s.media_voti,
                    "comportamento": s.comportamento,
                    "esito_finale": s.esito_finale
                })

    def carica_csv(self, filename):
        self.studenti = []
        with open(filename, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for riga in reader:
                s = Studente(
                    id=None,
                    nome=riga["nome"],
                    cognome=riga["cognome"],
                    eta=int(riga["eta"]),
                    genere=riga["genere"],
                    ore_studio=float(riga["ore_studio"]),
                    assenze=int(riga["assenze"]),
                    media_voti=float(riga["media_voti"]),
                    comportamento=riga["comportamento"]
                )
                s.id = int(riga["id"]) 
                self.studenti.append(s) #Aggiungo gli studenti nella lista interna
            if self.studenti:
                Studente.id_counter = max(s.id for s in self.studenti) + 1   

    def stampa_studenti(self):
        for s in self.studenti:
            print(s)

#----------- MENù TESTUALE -------------
    def menu(self):
            while True:
                print("\n=== MENU STUDENTI ===")
                print("1. Aggiungi studente manualmente")
                print("2. Genera studenti casuali")
                print("3. Stampa tutti gli studenti")
                print("4. Salva studenti su CSV")
                print("5. Carica studenti da CSV")
                print("0. Esci")
                
                scelta = input("Scegli un'opzione: ")
                
                if scelta == "1":
                    nome = input("Nome: ")
                    cognome = input("Cognome: ")
                    eta = int(input("Età: "))
                    genere = input("Genere (M/F): ")
                    ore_studio = float(input("Ore di studio: "))
                    assenze = int(input("Assenze: "))
                    media_voti = float(input("Media voti: "))
                    comportamento = input("Comportamento: ")
                    
                    studente = Studente(
                        id=None,
                        nome=nome,
                        cognome=cognome,
                        eta=eta,
                        genere=genere,
                        ore_studio=ore_studio,
                        assenze=assenze,
                        media_voti=media_voti,
                        comportamento=comportamento
                    )
                    self.aggiungi_studente(studente)
                    print("Studente aggiunto con successo!")
                
                elif scelta == "2":
                    n = int(input("Quanti studenti generare? "))
                    self.genera_studenti_casuali(n)
                    print(f"{n} studenti generati.")
                
                elif scelta == "3":
                    self.stampa_studenti()
                
                elif scelta == "4":
                    nome_file = input("Nome file CSV: ")
                    self.salva_csv(nome_file)
                    print(f"Studenti salvati in {nome_file}.")
                
                elif scelta == "5":
                    nome_file = input("Nome file CSV: ")
                    self.carica_csv(nome_file)
                    print(f"Studenti caricati da {nome_file}.")
                
                elif scelta == "0":
                    print("Uscita dal programma.")
                    break
                
                else:
                    print("Opzione non valida. Riprova.")

gestore = GestoreStudenti()
gestore.menu()
#FINE FASE 2
