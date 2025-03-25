import pandas as pd


def process_cipher_dataset(input_file, output_file):
    # Carica il dataset
    df = pd.read_csv(input_file)

    # Funzione per espandere lettere e bigrammi
    def expand_features(row):
        letters = list(row['Top9Letters']) + [''] * (9 - len(row['Top9Letters']))
        bigrams = row['Top5Bigrams'].split() + [''] * (5 - len(row['Top5Bigrams'].split()))

        # Crea un dizionario con le nuove colonne
        features = {f'Letter_{i + 1}': letters[i] for i in range(9)}
        features.update({f'Bigram_{i + 1}': bigrams[i] for i in range(5)})
        return pd.Series(features)

    # Espandi e concatena le nuove colonne
    expanded_features = df.apply(expand_features, axis=1)
    new_df = pd.concat([df, expanded_features], axis=1)

    # Rimuove le colonne originali Top9Letters e Top5Bigrams
    new_df.drop(['Top9Letters', 'Top5Bigrams'], axis=1, inplace=True)

    # Salva il nuovo dataset
    new_df.to_csv(output_file, index=False)

    print(f"Nuovo dataset salvato in: {output_file}")



import os
print(os.listdir())

# Usa la funzione con i tuoi file di input e output
process_cipher_dataset("Jupyter Notebooks\DataSets\\NewDataSet4.csv", 'output_dataset_colonne_divise.csv')
