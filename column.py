import pandas as pd
import random
import numpy as np
from cipherImplementations.cipher import Cipher, generate_random_list_of_unique_digits


class ColumnarTransposition(Cipher):
    def __init__(self, alphabet, unknown_symbol, unknown_symbol_number, fill_blocks=True):
        self.alphabet = alphabet
        self.unknown_symbol = unknown_symbol
        self.unknown_symbol_number = unknown_symbol_number
        self.fill_blocks = fill_blocks

    def generate_random_key(self, length):
        return generate_random_list_of_unique_digits(length)

    def encrypt(self, plaintext, key):
        ciphertext = []
        if self.fill_blocks:
            while len(plaintext) % len(key) != 0:
                if not isinstance(plaintext, list):
                    plaintext = list(plaintext)
                plaintext.append(self.alphabet.index(b'x'))
        for start in range(len(key)):
            position = np.where(key == start)[0][0]
            while position < len(plaintext):
                p = plaintext[position]
                if p > len(self.alphabet):
                    ciphertext.append(self.unknown_symbol_number)
                    position += len(key)
                    continue
                ciphertext.append(p)
                position += len(key)
        return np.array(ciphertext)

    def decrypt(self, ciphertext, key):
        plaintext = [b''] * len(ciphertext)
        i = 0
        for start in range(len(key)):
            position = np.where(key == start)[0][0]
            while position < len(plaintext):
                c = ciphertext[i]
                i += 1
                if c > len(self.alphabet):
                    plaintext[position] = self.unknown_symbol_number
                    position += len(key)
                    continue
                plaintext[position] = c
                position += len(key)
        return np.array(plaintext)


# Funzione per calcolare l'Indice di Coincidenza (IC)
def getIOC(text):
    text = text.lower()
    alph = "abcdefghijklmnopqrstuvwxyz"
    letterCounts = [text.count(letter) for letter in alph]

    N = sum(letterCounts)
    total = sum([ni * (ni - 1) for ni in letterCounts])

    return float(total) / (N * (N - 1)) if N > 1 else 0


# Lettura del file di input contenente le frasi
with open('Transinput_sentences.txt', 'r') as file:
    sentences = [line.strip() for line in file.readlines()]

# Inizializzazione dell'oggetto ColumnarTransposition
alphabet = b'abcdefghijklmnopqrstuvwxyz'  # Alfabeto in bytes
unknown_symbol = b'?'
unknown_symbol_number = 26  # Un numero fuori dall'intervallo dell'alfabeto

cipher = ColumnarTransposition(alphabet, unknown_symbol, unknown_symbol_number, fill_blocks=True)

# Lista per raccogliere i dati per il CSV
data = []

# Cifra le frasi e calcola l'IC
for sentence in sentences:
    # Converti il testo in una lista di indici
    plaintext = [alphabet.index(bytes([ord(char)])) for char in sentence.lower() if char.encode() in alphabet]

    # Genera una chiave casuale (lunghezza della chiave variabile tra 5 e 10)
    key_length = random.randint(5, 10)
    key = cipher.generate_random_key(key_length)

    # Cifra il testo
    ciphertext_indices = cipher.encrypt(plaintext, key)

    # Converti gli indici cifrati in caratteri
    ciphertext_str = ''.join([chr(alphabet[i]) for i in ciphertext_indices])

    # Calcola l'IC
    ic_value = getIOC(ciphertext_str)

    # Aggiungi i dati alla lista
    data.append({'Text': ciphertext_str, 'Cipher': 'ColumnarTransposition', 'IC': ic_value})

# Creazione del DataFrame Pandas
df = pd.DataFrame(data)

# Salva il risultato in un file CSV
df.to_csv('encrypted_sentences_columnar.csv', index=False)
