import trigrammi
import random
import string 
import utili as UC
import commons
import pandas as pd
import random
import numpy as np
from cipherImplementations.cipher import Cipher, generate_random_list_of_unique_digits
dizionario_valutazione = trigrammi.trigrams
parole_comuni = commons.commons



POPULATION_SIZE = 900   # Mantiene la diversità con un costo computazionale ragionevole
GENOME_LENGTH = 26      # Fisso per il problema
MUTATION_RATE = 0.3  # Evita troppi cambiamenti casuali, mantenendo comunque la diversità
CROSSOVER_RATE = 0.5  # Combina efficacemente le soluzioni dei genitori
GENERATIONS = 1200 
MAX = 0
BEST_TEXT = 0



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
    

def list_to_NDA(lista:list):
    return np.array(lista)







def fitness(testo:str):
    testo = testo.upper()
    valutazione = 0.0
    for elem in parole_comuni:
        if elem in testo:
            valutazione += elem.length()/200.0
    trigrams = [testo[i:i+3] for i in range(len(testo)-1)]
    global MAX
    global BEST_TEXT
    for tri in trigrams:
        if tri in dizionario_valutazione:
            valutazione += dizionario_valutazione[tri]
        if valutazione >= MAX:
            MAX = valutazione
            BEST_TEXT = testo
    return valutazione


def random_genome():
    length = random.randint(3,10)
    available_digits = list(range(length))
    random_list = random.sample(available_digits, length)
    return list_to_NDA(random_list)

def initial_population(populationSize):
    return [random_genome() for _ in range(populationSize)]

def select_parent(population, fitness_values):
    paired_population = list(zip(population, fitness_values))
    paired_population.sort(key=lambda x: x[1], reverse=True)
    sorted_population = [genome for genome, _ in paired_population]
    selected_index = random.choices(range(len(sorted_population)), weights=range(len(sorted_population), 0, -1), k=1)[0]
    return sorted_population[selected_index]


#TODO: aggiustare la mutazione  
def mutate(genome):
    genome = list(genome)
    if random.random() < MUTATION_RATE + 2 * MAX:
        idx1, idx2 = random.sample(range(GENOME_LENGTH), 2)
        genome[idx1], genome[idx2] = genome[idx2], genome[idx1]
    return list_to_NDA(genome)




def decodifica(ciphertext: str):
    alphabet = b'abcdefghijklmnopqrstuvwxyz'  # Alfabeto in bytes
    unknown_symbol = b'?'
    unknown_symbol_number = 26  # Un numero fuori dall'intervallo dell'alfabeto
    cipher = ColumnarTransposition(alphabet, unknown_symbol, unknown_symbol_number, fill_blocks=True)
    # Prepara il ciphertext, convertendolo in una lista di indici dell'alfabeto
    ciphertext = [alphabet.index(bytes([ord(char)])) for char in ciphertext.lower() if char.encode() in alphabet]
    
    # Inizializza la popolazione
    population = initial_population(POPULATION_SIZE)
    

    # Generazioni dell'algoritmo genetico
    for generation in range(GENERATIONS):
        # Calcola il fitness per ogni genome della popolazione
        fitness_values = []
        for genome in population:
            # Decifra il testo con la chiave attuale
            decrypted_indices = cipher.decrypt(ciphertext, list_to_NDA(genome))
            decrypted_text = ''.join(chr(alphabet[i]) for i in decrypted_indices)
            
            # Calcola il fitness del testo decifrato
            fitness_score = fitness(decrypted_text)
            fitness_values.append(fitness_score)
        
        # Trova il genome migliore in base al fitness
        best_genome = population[fitness_values.index(max(fitness_values))]

        # Seleziona una nuova popolazione basata sul fitness
        new_population = [best_genome] * 10  # Mantieni i migliori individui

        # Log del miglior testo dopo ogni 100 generazioni
        if generation % 100 == 0:
            print(f"Miglior soluzione dopo {generation} generazioni:")
            best_decrypted_indices = cipher.decrypt(ciphertext, best_genome)
            best_decrypted_text = ''.join(chr(alphabet[i]) for i in best_decrypted_indices)
            print(best_decrypted_text)

        # Creazione della nuova generazione tramite selezione e mutazione
        while len(new_population) < POPULATION_SIZE:
            parent1 = select_parent(population, fitness_values)
            parent2 = select_parent(population, fitness_values)
            child = mutate(parent1)  # Puoi applicare anche il crossover se lo implementi
            new_population.append(child)

        # Aggiorna la popolazione
        population = new_population[:POPULATION_SIZE]

    # Decodifica il testo usando il miglior genome trovato
    final_best_genome = population[fitness_values.index(max(fitness_values))]
    final_decrypted_indices = cipher.decrypt(ciphertext, final_best_genome)
    final_plaintext = ''.join(chr(alphabet[i]) for i in final_decrypted_indices)

    return final_plaintext






if __name__ == '__main__':

    print(decodifica("FHTOCEEEWFAXETSLELDDALHTNEATSX"))

