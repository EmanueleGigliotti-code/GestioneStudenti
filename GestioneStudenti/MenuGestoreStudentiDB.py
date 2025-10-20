from GestoreStudenteDB import GestoreStudenteDB
from Studente import Studente
#FASE 3 COMPLETA
def menu():
    gestore = GestoreStudenteDB()

    while True:
        print("\n=== MENU STUDENTI (SQLite) ===")
        print("1. Aggiungi studente manualmente")
        print("2. Genera studenti casuali")
        print("3. Visualizza tutti gli studenti")
        print("4. Modifica uno studente")
        print("5. Elimina uno studente")
        print("6. Esporta in studenti.csv")
        print("0. Esci")

        scelta = input("Scegli un'opzione: ")

        if scelta == "1":
            try:
                nome = input("Nome: ").strip()
                cognome = input("Cognome: ").strip()
                eta = int(input("Età (14-20): ").strip())
                genere = input("Genere (M/F): ").strip().upper()
                ore_studio = float(input("Ore di studio (>=0): ").strip())
                assenze = int(input("Assenze (>=0): ").strip())
                media_voti = float(input("Media voti (1-10): ").strip())
                comportamento = input("Comportamento (Ottimo/Buono/Sufficiente/Scarso): ").strip().capitalize()

                s = Studente(None, nome, cognome, eta, genere, ore_studio, assenze, media_voti, comportamento)
                new_id = gestore.inserisci_studente(s)
                print(f"Studente inserito con id {new_id}")
            except ValueError:
                print("Valori numerici non validi.")
            except Exception as e:
                print(f"Errore inserimento: {e}")

        elif scelta == "2":
            try:
                n = int(input("Quanti studenti generare? ").strip())
                gestore.popola_casuali(n)
            except ValueError:
                print("Inserisci un numero intero valido.")

        elif scelta == "3":
            gestore.visualizza_studenti()
            

        elif scelta == "4":
            try:
                id_stud = int(input("ID studente da modificare: ").strip())
                print("Campi modificabili: nome, cognome, eta, genere, ore_studio, assenze, media_voti, comportamento, esito_finale")
                campo = input("Campo: ").strip()
                nuovo_valore = input("Nuovo valore: ").strip()
                modificato = gestore.modifica_studente(id_stud, campo, nuovo_valore)
                if modificato:
                    print("Modifica eseguita.")
            except ValueError:
                print("ID non valido.")

        elif scelta == "5":
            try:
                id_stud = int(input("ID studente da eliminare: ").strip())
                gestore.elimina_studente(id_stud)
                print("Studente eliminato.")
            except ValueError:
                print("ID non valido.")

        elif scelta == "6":
            filename = input("Nome file CSV: ").strip() or "studenti.csv"
            gestore.esporta_csv(filename)

        elif scelta == "0":
            gestore.chiudi()
            print("Uscita dal programma.")
            break

        else:
            print("Opzione non valida. Riprova.")

menu()
