import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import sqlite3
from Fase4PreProcessing import Preprocessing
from GestoreStudenteDB import GestoreStudenteDB
from Studente import Studente

class AppGUI:
    def __init__(self, root):
        try:
            self.scaler = joblib.load("scaler.pkl")
        except:
            self.scaler = None

        self.root = root
        self.root.title("Gestione Studenti E Predizione")
        self.root.geometry("900x650")
        self.root.configure(bg="#f5f6fa")

        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TNotebook", background="#f5f6fa", borderwidth=0)
        style.configure("TNotebook.Tab",
                        font=("Segoe UI", 11, "bold"),
                        padding=[20, 10],
                        background="#dcdde1")
        style.map("TNotebook.Tab",
                  background=[("selected", "#2f3640")],
                  foreground=[("selected", "white")])

        style.configure("TLabel", background="#f5f6fa", font=("Segoe UI", 11))
        style.configure("TButton",
                        font=("Segoe UI", 11, "bold"),
                        padding=6,
                        relief="flat",
                        background="#40739e",
                        foreground="white")
        style.map("TButton",
                  background=[("active", "#273c75")])

        # Connessione DB
        self.gestore = GestoreStudenteDB()

        # Caricamento modello
        try:
            self.model = joblib.load("randomforest_model.pkl")
        except:
            self.model = None

        self.crea_widgets()

    def crea_widgets(self):
        tabControl = ttk.Notebook(self.root)

        self.tab_inserimento = ttk.Frame(tabControl)
        self.tab_predizione = ttk.Frame(tabControl)
        self.tab_statistiche = ttk.Frame(tabControl)

        tabControl.add(self.tab_inserimento, text='Inserimento Studente')
        tabControl.add(self.tab_predizione, text='Predizione Esito')
        tabControl.add(self.tab_statistiche, text='Statistiche')
        tabControl.pack(expand=1, fill="both", padx=10, pady=10)

        self.crea_tab_inserimento()
        self.crea_tab_predizione()
        self.crea_tab_statistiche()

    # --- Tab Inserimento ---
    def crea_tab_inserimento(self):
        frame = ttk.LabelFrame(self.tab_inserimento, text="Dati Studente", padding=20)
        frame.pack(fill="x", padx=30, pady=30)

        labels = ["Nome", "Cognome", "Età", "Genere", "Ore studio", "Assenze", "Media voti", "Comportamento"]
        self.entries = {}
        for i, label in enumerate(labels):
            ttk.Label(frame, text=label).grid(row=i, column=0, padx=10, pady=8, sticky="w")
            entry = ttk.Entry(frame, width=30)
            entry.grid(row=i, column=1, padx=10, pady=8, sticky="w")
            self.entries[label] = entry

        ttk.Button(frame, text="Salva Studente", command=self.salva_studente).grid(
            row=len(labels), column=0, columnspan=2, pady=15
        )

    def salva_studente(self):
        try:
            s = Studente(
                id=None,
                nome=self.entries["Nome"].get(),
                cognome=self.entries["Cognome"].get(),
                eta=int(self.entries["Età"].get()),
                genere=self.entries["Genere"].get().upper(),
                ore_studio=float(self.entries["Ore studio"].get()),
                assenze=int(self.entries["Assenze"].get()),
                media_voti=float(self.entries["Media voti"].get()),
                comportamento=self.entries["Comportamento"].get().capitalize()
            )
            self.gestore.inserisci_studente(s)
            messagebox.showinfo("Successo", f"Studente {s.nome} salvato con ID {s.id}")
            for e in self.entries.values():
                e.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Errore", f"Errore inserimento: {e}")

    # --- Tab Predizione ---
    def crea_tab_predizione(self):
        frame = ttk.LabelFrame(self.tab_predizione, text="Inserisci Dati per Predizione", padding=20)
        frame.pack(fill="x", padx=30, pady=30)

        labels = ["Età", "Ore studio", "Assenze", "Media voti", "Genere", "Comportamento"]
        self.pred_entries = {}
        for i, label in enumerate(labels):
            ttk.Label(frame, text=label).grid(row=i, column=0, padx=10, pady=8, sticky="w")
            entry = ttk.Entry(frame, width=30)
            entry.grid(row=i, column=1, padx=10, pady=8, sticky="w")
            self.pred_entries[label] = entry

        ttk.Button(frame, text="Predici Esito", command=self.predici_esito).grid(
            row=len(labels), column=0, columnspan=2, pady=15
        )
        self.pred_label = ttk.Label(frame, text="", font=("Segoe UI", 13, "bold"), foreground="#192a56")
        self.pred_label.grid(row=len(labels)+1, column=0, columnspan=2, pady=20)
    
    def predici_esito(self):
        try:
            if not self.model:
                messagebox.showerror("Errore", "Modello non caricato!")
                return

            # Recupero dati dall'utente
            eta = int(self.pred_entries["Età"].get())
            ore_studio = float(self.pred_entries["Ore studio"].get())
            assenze = int(self.pred_entries["Assenze"].get())
            media_voti = float(self.pred_entries["Media voti"].get())
            genere = self.pred_entries["Genere"].get().upper()
            comportamento = self.pred_entries["Comportamento"].get().capitalize()

            # Dizionario dati
            dati_input = {
                "eta": eta,
                "ore_studio": ore_studio,
                "assenze": assenze,
                "media_voti": media_voti,
                "genere_num": 1 if genere == "M" else 0,
                "comportamento_Ottimo": int(comportamento == "Ottimo"),
                "comportamento_Buono": int(comportamento == "Buono"),
                "comportamento_Sufficiente": int(comportamento == "Sufficiente"),
                "comportamento_Scarso": int(comportamento == "Scarso"),
            }

            # Creo DataFrame nell'ordine delle feature del modello
            features = list(self.model.feature_names_in_)
            df_input = pd.DataFrame([[dati_input.get(f, 0) for f in features]], columns=features)

            # Applico lo scaler
            if self.scaler:
                num_cols = ["eta", "ore_studio", "assenze", "media_voti"]
                df_input[num_cols] = self.scaler.transform(df_input[num_cols])

            # Predizione
            pred = self.model.predict(df_input)[0]
            esito = "Promosso" if pred == 1 else "Bocciato"
            self.pred_label.config(text=f"Esito previsto: {esito}")

        except Exception as e:
            messagebox.showerror("Errore", f"Errore predizione: {e}")

    # --- Tab Statistiche ---
    def crea_tab_statistiche(self):
        frame = ttk.LabelFrame(self.tab_statistiche, text="Statistiche Studenti", padding=20)
        frame.pack(fill="x", padx=30, pady=30)

        ttk.Button(frame, text="Mostra numero studenti per esito", command=self.visualizza_statistiche).pack(pady=15)
        self.stat_label = ttk.Label(frame, text="", font=("Segoe UI", 12))
        self.stat_label.pack()

        ttk.Button(frame, text="Genera Report PDF", command=self.genera_report_pdf).pack(pady=15)

    def visualizza_statistiche(self):
        self.gestore.cursor.execute("SELECT esito_finale, COUNT(*) FROM studenti GROUP BY esito_finale")
        dati = self.gestore.cursor.fetchall()
        testo = "\n".join([f"{row[0]}: {row[1]}" for row in dati])
        self.stat_label.config(text=testo)


    # --- FASE 8 REPORT PDF---
    def genera_report_pdf(self):
        try:
            # ------------------------
            # 1) Preprocessing e dati reali
            # ------------------------
            prep = Preprocessing("studenti.db")
            prep.preprocess(salva=False)  # Preprocessing senza salvare CSV

            X_test = prep.X_test.copy()
            y_true = prep.y_test.values

            if self.model:
                y_pred = self.model.predict(X_test)
            else:
                raise ValueError("Modello non caricato!")
            
            # ------------------------
            # 2) Matrice di Confusione
            # ------------------------
            cm = confusion_matrix(y_true, y_pred)
            plt.figure(figsize=(5,4))
            sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                        xticklabels=["Bocciato","Promosso"],
                        yticklabels=["Bocciato","Promosso"])
            plt.title("Matrice di Confusione")
            plt.savefig("conf_matrix.png")
            plt.close()

            # ------------------------  
            # 3) Clustering KMeans
            # ------------------------
            conn = sqlite3.connect("studenti.db")
            df = pd.read_sql_query("SELECT nome, esito_finale, media_voti, assenze FROM studenti", conn)
            conn.close()

            X_cluster = df[["media_voti", "assenze"]]
            kmeans = KMeans(n_clusters=2, random_state=0, n_init="auto").fit(X_cluster)
            df["Cluster"] = kmeans.labels_

            plt.scatter(df["media_voti"], df["assenze"], c=df["Cluster"], cmap="viridis")
            plt.xlabel("Media Voti")
            plt.ylabel("Assenze")
            plt.title("Clustering KMeans (Studenti)")
            plt.savefig("kmeans.png")
            plt.close()

            # ------------------------
            # 4) Distribuzione voti/assenze
            # ------------------------
            plt.scatter(df["media_voti"], df["assenze"], c=df["esito_finale"].map({"Promosso":"g","Bocciato":"r"}))
            plt.xlabel("Media Voti")
            plt.ylabel("Assenze")
            plt.title("Distribuzione Voti/Assenze")
            plt.savefig("voti_assenze.png")
            plt.close()

            # ------------------------
            # 5) Metriche modello
            # ------------------------
            acc = accuracy_score(y_true, y_pred)
            prec = precision_score(y_true, y_pred)
            rec = recall_score(y_true, y_pred)
            f1 = f1_score(y_true, y_pred)
            report_text = f"""
            Accuracy: {acc:.2f}
            Precision: {prec:.2f}
            Recall: {rec:.2f}
            F1 Score: {f1:.2f}
            """

            # ------------------------
            # 6) Creazione PDF
            # ------------------------
            doc = SimpleDocTemplate("report_studenti.pdf", pagesize=A4)
            styles = getSampleStyleSheet()
            story = []

            # Titolo
            story.append(Paragraph("<b>Report Studenti & Predizioni</b>", styles["Title"]))
            story.append(Spacer(1, 20))

            # Metadati
            story.append(Paragraph(f"Generato il: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles["Normal"]))
            story.append(Paragraph("Autore: Emanuele", styles["Normal"]))
            story.append(Paragraph("Modello: RandomForest", styles["Normal"]))
            story.append(Spacer(1, 20))

            # Elenco studenti
            conn = sqlite3.connect("studenti.db")
            studenti = pd.read_sql_query("SELECT nome, esito_finale FROM studenti", conn)
            conn.close()
            data = [["Nome", "Esito"]] + studenti.values.tolist()
            t = Table(data, hAlign="LEFT")
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.lightblue),
                ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                ('GRID', (0,0), (-1,-1), 0.5, colors.black),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold')
            ]))
            story.append(Paragraph("Elenco Studenti", styles["Heading2"]))
            story.append(t)
            story.append(Spacer(1, 20))

            # Matrice di Confusione
            story.append(Paragraph("Matrice di Confusione", styles["Heading2"]))
            story.append(Image("conf_matrix.png", width=400, height=300))
            story.append(Spacer(1, 20))

            # KMeans
            story.append(Paragraph("Clustering KMeans", styles["Heading2"]))
            story.append(Image("kmeans.png", width=400, height=300))
            story.append(Spacer(1, 20))

            # Voti/Assenze
            story.append(Paragraph("Distribuzione Voti/Assenze", styles["Heading2"]))
            story.append(Image("voti_assenze.png", width=400, height=300))
            story.append(Spacer(1, 20))

            # Metriche
            story.append(Paragraph("Sommario Metriche", styles["Heading2"]))
            for line in report_text.splitlines():
                story.append(Paragraph(line, styles["Normal"]))
            story.append(Spacer(1, 20))

            doc.build(story)

            messagebox.showinfo("Successo", "Report PDF generato con successo: report_studenti.pdf")

        except Exception as e:
            messagebox.showerror("Errore", f"Errore generazione report: {e}")


# --- Esecuzione GUI ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AppGUI(root)
    root.mainloop()
