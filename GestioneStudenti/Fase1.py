#Fase 1 
import csv
import random

#Lista nomi maschili, femminili e cognomi
nomi_maschili = ['Luca', 'Marco', 'Andrea', 'Matteo', 'Francesco', 'Giovanni', 'Alessandro', 'Davide', 'Simone', 'Gabriele',
                 'Federico', 'Riccardo', 'Lorenzo', 'Tommaso', 'Emanuele', 'Daniele', 'Nicola', 'Stefano', 'Antonio', 'Fabio',
                 'Paolo', 'Giuseppe', 'Vincenzo', 'Roberto', 'Salvatore', 'Claudio', 'Enrico', 'Michele', 'Alberto', 'Maurizio']

nomi_femminili = ['Giulia', 'Francesca', 'Sara', 'Martina', 'Chiara', 'Alessia', 'Valentina', 'Federica', 'Elena', 'Ilaria',
                  'Laura', 'Simona', 'Angela', 'Anna', 'Maria', 'Sofia', 'Claudia', 'Veronica', 'Camilla', 'Eleonora',
                  'Paola', 'Cristina', 'Silvia', 'Barbara', 'Roberta', 'Alice', 'Marta', 'Beatrice', 'Nicole', 'Elisa']

cognomi = ['Rossi', 'Russo', 'Ferrari', 'Esposito', 'Bianchi', 'Romano', 'Colombo', 'Ricci', 'Marino', 'Greco',
           'Bruno', 'Gallo', 'Conti', 'De Luca', 'Mancini', 'Costa', 'Giordano', 'Rizzo', 'Lombardi', 'Moretti',
           'Barbieri', 'Fontana', 'Santoro', 'Mariani', 'Rinaldi', 'Caruso', 'Ferraro', 'Fabbri', 'Galli', 'Martini',
           'Leone', 'Longo', 'Gentile', 'Martinelli', 'Serra', 'Villa', 'Cattaneo', 'Sala', 'Pellegrini', 'Farina',
           'Orlando', 'Sanna', 'Piras', 'Lopes', 'Grassi', 'De Santis', 'Monti', 'Bellini', 'Marchetti', 'Valentini']

comportamenti = ['Ottimo', 'Buono', 'Sufficiente', 'Scarso']
'''
Generazione studente
-ID univoco
 -Nome (maschile o femminile)
 -Cognome
 -Età (da 14 a 20 anni)
 -Genere (M o F)
 -Ore di studio giornaliere (valore decimale realistico tra 0 e 8)
 -Numero di assenze (intero casuale)
 -Media voti (da 4 a 10, con un decimale)
 -Comportamento (tra: Ottimo, Buono, Sufficiente, Scarso)
 -Esito finale (Promosso o Bocciato), determinato da una logica specifica.
'''
def calcola_esito(media_voti, comportamento, assenze):
    if comportamento =='Scarso' or media_voti <= 5.3 or assenze ==220:
        return 'Bocciato'
    return 'Promosso'

#Creo la funzione per generare un singolo studente casuale
def genera_studente(id):
    genere = random.choice(['M', 'F'])
    nome = random.choice(nomi_maschili if genere =='M' else nomi_femminili)
    cognome = random.choice(cognomi)
    eta = random.randint(14,20) 
    ore_studio = round(random.uniform(0,8),1) #Genero un numero casuale tra 0 e 8 e con 1 vado a specificare che voglio una sola cifra dopo la virgola
    assenze = random.randint(0, 250)
    media_voti = round(random.uniform(5, 10), 1) #Ho modificato la media voti da 5 a 10 altrimenti andava in loop visto che continuava a bocciare
    comportamento = random.choice(comportamenti)
    esito_finale = calcola_esito(media_voti, comportamento, assenze)
    
    return {
        "id": id,
        "nome": nome,
        "cognome": cognome,
        "eta": eta,
        "genere": genere,
        "ore_studio": ore_studio,
        "assenze": assenze,
        "media_voti": media_voti,
        "comportamento": comportamento,
        "esito_finale": esito_finale
    }
'''
Generazione iterativa del dataset:
-Generare studenti in “batch” di dimensione definita (ad esempio 200 studenti per batch).
-Continuare a generare batch e aggiungerli al dataset totale finché la percentuale di studenti promossi non supera il 60% sul totale degli studenti generati finora.
-Stampare a video come promemoria il numero totale di studenti, il numero di promossi e la percentuale di promossi dopo ogni batch generato.
'''
def ds_Studenti(batch=200):
    studenti = []
    id_corrente = 1
    percentuale_promossi = 0
    
    # Continuiamo finché la percentuale non supera il 60%
    while percentuale_promossi <= 60:
        # Genero un lotto di studenti
        for _ in range(batch):
            studenti.append(genera_studente(id_corrente))
            id_corrente += 1
        
        # Calcolo promossi e percentuale
        promossi = sum(1 for s in studenti if s["esito_finale"] == "Promosso")
        percentuale_promossi = (promossi / len(studenti)) * 100
        
        # Stampo lo stato attuale
        print(f"Totale studenti: {len(studenti)} | Promossi: {promossi} | Percentuale: {percentuale_promossi:.2f}%")
    
    return studenti

studenti = ds_Studenti(200)
print(len(studenti))

#Funzione per salvare in CSV
def salva_csv(studenti, filename="Studenti.csv"):
    intestazione = ["id","nome","cognome","eta","genere","ore_studio","assenze","media_voti","comportamento","esito_finale"]
 
    with open(filename, "w", newline="", encoding="utf-8") as f:
# Creo un writer che sa scrivere nel CSV usando dizionari DictWriter.
        writer = csv.DictWriter(f, fieldnames=intestazione)
#writeheader serve per stampare compe prima riga l'intestazione tramite fieldnames
        writer.writeheader()
#writerows mi stampa la lista degli studenti
        writer.writerows(studenti)

    print(f"File salvato correttamente: {filename}")

salva_csv(studenti, "Studenti.csv")

'''
🧭 Fase 2: Refactoring ad oggetti (OOP)
📋 Obiettivo
Convertire il codice in stile OOP con:
-classe Studente
-classe GestoreStudenti

🧱 Struttura consigliata
class Studente:
    def __init__(self, id, nome, cognome, età, genere, ore_studio, assenze, media_voti, comportamento, esito_finale):
        ...

class GestoreStudenti:
    def __init__(self):
        self.studenti = []

    def aggiungi_studente(self, studente):
        ...

    def salva_csv(self, nome_file):
        ...

    def carica_csv(self, nome_file):
        ...
➕ Extra suggeriti
-metodo __str__() nella classe Studente
-menu testuale che richiama i metodi della classe GestoreStudenti
'''