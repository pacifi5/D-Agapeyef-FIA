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
import VigenereSolver as Vig

warnings.filterwarnings("ignore", category=InconsistentVersionWarning)

# Carica il modello e i LabelEncoders
loaded_data = joblib.load('Jupyter Notebooks/NuovoModelloMigliorato.joblib')
model = loaded_data['model']
label_encoders = loaded_data['label_encoders']
target_encoder = loaded_data['target_encoder']
dag = False

cifrario = input("Inserisci cifrario\n").lower()

if cifrario == "dagapeyeff":
    colsolver.POPULATION_SIZE = 300
    colsolver.GENERATIONS = 300
    monosolver.POPULATION_SIZE = 300
    monosolver.GENERATIONS = 300
    dag = True
    cifrario = "OPBSMIQIKRPMKIDLLKBDDYLPDNLDQCEKOGCTFBCLLKILBQNKPELCEKSILEPLBLKQOPMMOLNNPDDQGRNKEDKEMBICMIBKINLKGCOGMLNLRBMBQBQPNMMEKDDECCDCIOIEKLPOBPMQOLPICPPMQPLNGPIKMBQIQQKDCLPDODNDLGNOBBIBNDMGKNMPBEENMMBCNGOG"

ic = Cipher.indice_di_coincidenza(cifrario)
top_letters = Cipher.get_top9_chars(cifrario)  
top_bigrams = Cipher.get_top_5_bigrams(cifrario)  
top_bigrams = top_bigrams.split()


new_data = {'Text': [cifrario], 'IC': [ic]}

for i in range(9):
    col_name = f'Letter_{i+1}'
    new_data[col_name] = [top_letters[i].lower()]  

for i in range(5):
    col_name = f'Bigram_{i+1}'
    new_data[col_name] = [top_bigrams[i].lower()]


new_df = pd.DataFrame(new_data)


# Trasforma i nuovi dati usando i LabelEncoder salvati
for column in new_df.columns:
    if new_df[column].dtype == 'object' and column in label_encoders:
        try:
            new_df[column] = label_encoders[column].transform(new_df[column])
        except ValueError:
            new_df[column] = -1  

try:
    probabilities = model.predict_proba(new_df)
    
    top_4_indices = np.argsort(probabilities[0])[::-1][:4]
    top_4_classes_encoded = model.classes_[top_4_indices]
    top_4_probabilities = probabilities[0][top_4_indices]

    # Decodifica le classi predette usando il target encoder
    top_4_classes = target_encoder.inverse_transform(top_4_classes_encoded)

    for i in range(4):
        if not dag:
            print(f"Classifica #{i + 1}: {top_4_classes[i]} con probabilità {top_4_probabilities[i]:.4f}")
except ValueError as e:
    print(f"Errore durante la predizione: {e}")

if dag:
    print("bentornato signor Alexander")
    best = [cifrario, monosolver.fitness(cifrario)]
    while True:
        print(f"\nCIFRARIO ATTUALE:\n{best[0]} \nFitness: {best[1]}\n")
        print("1. Scodifica con colsolver")
        print("2. Decodifica con monosolver")
        print("3. Inserire un nuovo cifrario")
        print("4. Decodifica colsolver")
        print("5. Esci")
        
        scelta = input("Scegli un'opzione: ")
        
        if scelta == "1":
            cifrario = colsolver.scodifica(cifrario.lower())
        elif scelta == "2":
            cifrario = monosolver.decodifica(cifrario.lower())
        elif scelta == "3":
            cifrario = input("Inserisci il nuovo cifrario: ")
        elif scelta == "4":
            cifrario = colsolver.decodifica(cifrario.lower())
        elif scelta == "5":
            print("Uscita dal programma.")
            break
        else:
            print("Scelta non valida, riprova.")
        
        fitness = monosolver.fitness(cifrario.lower())
        if fitness > best[1]:
            best = [cifrario, fitness]
        print(f"Nuovo risultato: {best[0]} con fitness {best[1]}")


if top_4_classes[0] == 'ceaser':
    x = cesarsolver.giveBestOfAll(cesarsolver.giveAllDecryptions(cifrario))
    if x == -1:
        print("Il cifrario non sembra dare nessuna decodifica per Cesare, proviamo la seconda miglior alternativa:\n")
        if top_4_classes[1] == 'ColumnarTransposition':
            colsolver.decodifica(cifrario)
        elif top_4_classes[1] == 'MonoalphabeticSubstitution':
            monosolver.decodifica(cifrario)
        elif top_4_classes[1] == 'Vigenere':
            Vig.decodifica(cifrario.lower())
    else:
        print(x)
elif top_4_classes[0] == 'ColumnarTransposition':
    colsolver.decodifica(cifrario)
elif top_4_classes[0] == 'MonoalphabeticSubstitution':
    monosolver.decodifica(cifrario)
elif top_4_classes[0] == 'Vigenere':
    Vig.decodifica(cifrario.lower())
