# 🎓 Student Outcome — Preprocessing & ML (SQLite → scikit-learn)

Pipeline end-to-end per predire l’**esito finale** degli studenti (Promosso/Bocciato) da un DB **SQLite**:
- 📥 Lettura dati da `studenti.db` (tabella `studenti`)
- 🧹 Preprocessing: one-hot di `comportamento`, mapping `genere`/`esito_finale`, train/test split con `stratify`, normalizzazione 0–1 su feature numeriche
- 🤖 Confronto modelli: `DecisionTree`, `KNN`, `NaiveBayes`, `SVM (linear)`, `RandomForest`
- 📊 Metriche: **accuracy**, **confusion matrix**, **classification report**
- 💾 Salvataggio modello (es. `randomforest_model.pkl`)
