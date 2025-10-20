import sqlite3
import csv
from Studente import Studente, comportamenti

#Creo queste due variabili di tuple in modo tale che sono immutabili e quindi nessuno può modificarli
CHECK_COMPORTAMENTI = tuple(comportamenti) #Gli passo la lista dei comportamenti ['Ottimo', 'Buono', 'Sufficiente', 'Scarso'] e li converto sempre in tupla in modo che siano questi
CHECK_ESITO = ('Promosso', 'Bocciato')

class GestoreStudenteDB:
    def __init__(self, db_name="studenti.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.crea_tabella()

    def crea_tabella(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS studenti (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cognome TEXT NOT NULL,
            eta INTEGER CHECK(eta BETWEEN 14 AND 20),
            genere TEXT CHECK(genere IN ('M','F')),
            ore_studio REAL CHECK(ore_studio >= 0),
            assenze INTEGER CHECK(assenze >= 0),
            media_voti REAL CHECK(media_voti BETWEEN 1 AND 10),
            comportamento TEXT CHECK(comportamento IN ('Ottimo','Buono','Sufficiente','Scarso')),
            esito_finale TEXT CHECK(esito_finale IN ('Promosso','Bocciato'))
        );
        """)
        self.conn.commit()

    # --- CRUD ---
    #Prende come parametro un oggetto studente e faccio un controllo sull'esito. Quindi se lo studente rispetta i requisiti allora tramite la query lo aggiunge nel db
    def inserisci_studente(self, studente: Studente):
        esito = studente.calcola_esito()
        self.cursor.execute("""
            INSERT INTO studenti (nome, cognome, eta, genere, ore_studio, assenze, media_voti, comportamento, esito_finale)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (studente.nome, studente.cognome, studente.eta, studente.genere,
              studente.ore_studio, studente.assenze, studente.media_voti,
              studente.comportamento, esito))
        self.conn.commit()
        studente.id = self.cursor.lastrowid #lastrowid mi serve per prelevare l'id dal db visto che su python è none
        return studente.id

#Metodo che converte una tupla proveniente dal DB in un oggetto Studente
    def _row_to_studente(self, row):
        return Studente(
            id=row[0], nome=row[1], cognome=row[2], eta=row[3], genere=row[4],
            ore_studio=row[5], assenze=row[6], media_voti=row[7], comportamento=row[8]
        )

#Metodo che mi permette di visualizzare tutti gli studenti per id e me li stampa a tuple con il metodo di sopra
    def visualizza_studenti(self):
        self.cursor.execute("SELECT * FROM studenti ORDER BY id")
        rows = self.cursor.fetchall()
        if not rows:
            print("Nessuno studente presente.")
            return
        for r in rows:
            s = self._row_to_studente(r)
            print(s)

#Metodo che mi serve per ricalcolare l'esito finale dello studente con id=id_stud e aggiorna il campo esito_finale nel DB
    def _ricalcola_esito_e_aggiorna(self, id_stud):
        self.cursor.execute("""
            SELECT nome, cognome, eta, genere, ore_studio, assenze, media_voti, comportamento
            FROM studenti WHERE id = ?
        """, (id_stud,))
        row = self.cursor.fetchone()
        if not row:
            return False
        tmp = Studente(
            id=id_stud, nome=row[0], cognome=row[1], eta=row[2], genere=row[3],
            ore_studio=row[4], assenze=row[5], media_voti=row[6], comportamento=row[7]
        )
        esito = tmp.calcola_esito()
        self.cursor.execute("UPDATE studenti SET esito_finale = ? WHERE id = ?", (esito, id_stud))
        self.conn.commit()
        return True

# Permette di modificare un campo specifico di uno studente. 
# Dopo l'aggiornamento richiama _ricalcola_esito_e_aggiorna per aggiornare automaticamente l'esito finale se necessario
    def modifica_studente(self, id_stud, campo, nuovo_valore):
        colonne = {"nome", "cognome", "eta", "genere", "ore_studio", "assenze", "media_voti", "comportamento", "esito_finale"}
        if campo not in colonne:
            print(f"Campo non valido: {campo}")
            return False

        try:
            if campo in ("eta", "assenze"):
                nuovo_valore = int(nuovo_valore)
            elif campo in ("ore_studio", "media_voti"):
                nuovo_valore = float(nuovo_valore)
            elif campo == "genere":
                nuovo_valore = str(nuovo_valore).strip().upper()
                if nuovo_valore not in ("M", "F"):
                    raise ValueError("Genere deve essere 'M' o 'F'")
            elif campo == "comportamento":
                nuovo_valore = str(nuovo_valore).strip().capitalize()
                if nuovo_valore not in CHECK_COMPORTAMENTI:
                    raise ValueError(f"Comportamento deve essere in {CHECK_COMPORTAMENTI}")
            elif campo == "esito_finale":
                nuovo_valore = str(nuovo_valore).strip().capitalize()
                if nuovo_valore not in CHECK_ESITO:
                    raise ValueError(f"Esito finale deve essere in {CHECK_ESITO}")
        except ValueError as e:
            print(f"Valore non valido: {e}")
            return False

        self.cursor.execute(f"UPDATE studenti SET {campo} = ? WHERE id = ?", (nuovo_valore, id_stud))
        self.conn.commit()
        self._ricalcola_esito_e_aggiorna(id_stud)
        return True

    def elimina_studente(self, id_stud):
        self.cursor.execute("DELETE FROM studenti WHERE id = ?", (id_stud,))
        self.conn.commit()
        return True

    def esporta_csv(self, filename="studenti.csv"):
        self.cursor.execute("SELECT * FROM studenti ORDER BY id")
        dati = self.cursor.fetchall()
#con desc[0] vado a prenedere i nomi dei campi del db memorizzati all'interno di self.cursor.description
        intestazione = [desc[0] for desc in self.cursor.description]
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(intestazione)
            writer.writerows(dati)
        print(f"Esportati {len(dati)} record in {filename}")

    def popola_casuali(self, n=150):
        for _ in range(n):
            s = Studente.genera_studente()
            self.inserisci_studente(s)
        print(f"Popolati {n} studenti casuali.")

    def chiudi(self):
        self.conn.close()
