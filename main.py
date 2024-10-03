import joblib
import pandas as pd
import utili as Cipher
import warnings
import numpy as np
from sklearn.exceptions import InconsistentVersionWarning
from sklearn.preprocessing import LabelEncoder
import monosolver as monosolver
import caesarSolver as cesarsolver
import TranspositionSolver as colsolver

warnings.filterwarnings("ignore", category=InconsistentVersionWarning)

# Carica il modello e i LabelEncoders
loaded_data = joblib.load('Jupyter Notebooks/test_model_and_encoders.joblib')
model = loaded_data['model']
label_encoders = loaded_data['label_encoders']
target_encoder = loaded_data['target_encoder']

cifrario = input("Inserisci cifrario\n").lower()

# Crea un dizionario con le nuove caratteristiche
new_data = {
    'Text': [cifrario],
    'IC': [Cipher.indice_di_coincidenza(cifrario)],
    'Top9Letters': [''.join(Cipher.get_top9_chars(cifrario)).lower()],
    'Top5Bigrams': [''.join(Cipher.get_top_5_bigrams(cifrario)).lower()],
    
}

# Converti i nuovi dati in un DataFrame
new_df = pd.DataFrame(new_data)

# Trasforma i nuovi dati usando i LabelEncoder salvati
for column in new_df.columns:
    if new_df[column].dtype == 'object' and column in label_encoders:
        try:
            new_df[column] = label_encoders[column].fit_transform(new_df[column])
        except ValueError as e:
            print(f"Errore: {e}")
            print(f"La colonna '{column}' contiene valori non visti durante l'addestramento.")
            new_df[column] = -1  # Oppure gestisci diversamente, ad esempio impostando valori di default

# Predici le probabilità per ogni classe
try:
    probabilities = model.predict_proba(new_df)
    
    # Ordina le classi per probabilità decrescente e prendi le prime 3
    top_4_indices = np.argsort(probabilities[0])[::-1][:4]
    top_4_classes_encoded = model.classes_[top_4_indices]
    top_4_probabilities = probabilities[0][top_4_indices]

    # Decodifica le classi predette usando il target encoder
    top_4_classes = target_encoder.inverse_transform(top_4_classes_encoded)

    # Stampa le prime 3 classi con le loro probabilità
    for i in range(4):
        print(f"Classifica #{i + 1}: {top_4_classes[i]} con probabilità {top_4_probabilities[i]:.4f}")
except ValueError as e:
    print(f"Errore durante la predizione: {e}")


if top_4_classes[0] == 'ceaser':
    x=(cesarsolver.giveBestOfAll(cesarsolver.giveAllDecryptions(cifrario)))
    if x==-1:
        if top_4_classes[1] == 'ColumnarTransposition':
            colsolver.decodifica(cifrario)
        elif top_4_classes[1]=='MonoalphabeticSubstitution':
            monosolver.decodifica(cifrario)
        elif top_4_classes[1]=='Vigenere':
            print("io vigenere ancora non lo so fare")
    else:
        print(x)





    

    
