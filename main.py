import joblib
import pandas as pd
import utils as Cipher
import warnings
import numpy as np
from sklearn.exceptions import InconsistentVersionWarning
from sklearn.preprocessing import LabelEncoder
import monosolver as monosolver
import caesarSolver as cesarsolver

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
    top_3_indices = np.argsort(probabilities[0])[::-1][:3]
    top_3_classes_encoded = model.classes_[top_3_indices]
    top_3_probabilities = probabilities[0][top_3_indices]

    # Decodifica le classi predette usando il target encoder
    top_3_classes = target_encoder.inverse_transform(top_3_classes_encoded)

    # Stampa le prime 3 classi con le loro probabilità
    for i in range(3):
        print(f"Classifica #{i + 1}: {top_3_classes[i]} con probabilità {top_3_probabilities[i]:.4f}")
except ValueError as e:
    print(f"Errore durante la predizione: {e}")



if top_3_classes[0] == 'MonoalphabeticSubstitution':
    monosolver.decodifica(cifrario)
elif top_3_classes[0] == 'ceaser':
    print(cesarsolver.giveBestOfAll(cesarsolver.giveAllDecryptions(cifrario)))


    

    
