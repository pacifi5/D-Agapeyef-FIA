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



POPULATION_SIZE = 900                      
MUTATION_RATE = 0.7  
MUTATION_RATE2 = 0.2  
CROSSOVER_RATE = 0.5  
GENERATIONS = 1200 
MAX = 0
BEST_TEXT = 0
ogtx = ""



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
        if elem.upper() in testo:
            valutazione += len(elem)/200.0
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
    length = random.randint(3,15)
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


def mutate_add_or_remove(genome):
    genome = list(genome)
    if random.random() > MUTATION_RATE2:
        return list_to_NDA(genome)
    
  
    if random.random() < 0.5:  
        # Rimuovere l'elemento più grande
        if len(genome) > 3:
            genome.remove(max(genome))
    else:
        
        max_value = max(genome)
        next_value = max_value + 1
        genome.append(next_value)
    
    return list_to_NDA(genome)



#TODO: aggiustare la mutazione  
def mutate(genome):
    genome = list(genome)
    if random.random() < MUTATION_RATE:
        idx1, idx2 = random.sample(range(len(genome)), 2)
        genome[idx1], genome[idx2] = genome[idx2], genome[idx1]
    return list_to_NDA(genome)




def decodifica(ciphertext: str):
    print("Tentativo di decodifica Trasposizione Colonnare:\n")
    alphabet = b'abcdefghijklmnopqrstuvwxyz'  
    unknown_symbol = b'?'
    unknown_symbol_number = 26  
    cipher = ColumnarTransposition(alphabet, unknown_symbol, unknown_symbol_number, fill_blocks=True)
    # Prepara il ciphertext, convertendolo in una lista di indici dell'alfabeto
    global ogtx
    ogtx = ciphertext
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
        
       
        best_genome = population[fitness_values.index(max(fitness_values))]

        # Seleziona una nuova popolazione basata sul fitness
        new_population = [best_genome] * round(generation / 100 * 10)  # Mantieni i migliori individui
        
    
        if generation % 100 == 0 or generation == 0:
            print(f"Miglior soluzione dopo {generation} generazioni:")
            best_decrypted_indices = cipher.decrypt(ciphertext, best_genome)
            best_decrypted_text = ''.join(chr(alphabet[i]) for i in best_decrypted_indices)
            if(fitness(best_decrypted_text) <= fitness(str(ogtx))):
                 print(ogtx)
                 print("con fitness:" + str(fitness(ogtx)))
            else:
                print(best_decrypted_text)
                print("con fitness:" + str(fitness(best_decrypted_text)))

        # Creazione della nuova generazione tramite selezione e mutazione
        while len(new_population) < POPULATION_SIZE:
            parent1 = select_parent(population, fitness_values)
            parent2 = select_parent(population, fitness_values)
    
            if random.random() < CROSSOVER_RATE:
                child = crossover(parent1, parent2)
            else:
                child = mutate(parent1)
            child = mutate_add_or_remove(child)
            

            new_population.append(child)

        
        population = new_population[:POPULATION_SIZE]

    
    final_best_genome = population[fitness_values.index(max(fitness_values))]
    final_decrypted_indices = cipher.decrypt(ciphertext, final_best_genome)
    final_plaintext = ''.join(chr(alphabet[i]) for i in final_decrypted_indices)

    if(fitness(final_plaintext)< fitness(ogtx)):
        return ogtx
    return final_plaintext



def scodifica(ciphertext: str):
    """funzione atta solo a testare il cifrario dagapeyeff"""
    print("Tentativo di scodifica Trasposizione Colonnare:\n")
    alphabet = b'abcdefghijklmnopqrstuvwxyz'  
    unknown_symbol = b'?'
    unknown_symbol_number = 26  
    cipher = ColumnarTransposition(alphabet, unknown_symbol, unknown_symbol_number, fill_blocks=False)
    ciphertext = ciphertext.lower()
    global ogtx
    ogtx = ciphertext
    ciphertext = [alphabet.index(bytes([ord(char)])) for char in ciphertext.lower() if char.encode() in alphabet]
    population = initial_population(POPULATION_SIZE)
    for generation in range(GENERATIONS):
        fitness_values = []
        for genome in population:
            decrypted_indices = cipher.encrypt(ciphertext, list_to_NDA(genome))
            decrypted_text = ''.join(chr(alphabet[i]) for i in decrypted_indices)
            fitness_score = fitness(decrypted_text)
            fitness_values.append(fitness_score)
        best_genome = population[fitness_values.index(max(fitness_values))]
        new_population = [best_genome] * round(generation / 100 * 10)  
        if generation % 100 == 0 or generation == 0:
            print(f"Miglior soluzione dopo {generation} generazioni:")
            best_decrypted_indices = cipher.encrypt(ciphertext, best_genome)
            best_decrypted_text = ''.join(chr(alphabet[i]) for i in best_decrypted_indices)
            if(fitness(best_decrypted_text) <= fitness(str(ogtx))):
                 print(ogtx)
                 print("con fitness:" + str(fitness(ogtx)))
            else:
                print(best_decrypted_text)
                print("con fitness:" + str(fitness(best_decrypted_text)))
        while len(new_population) < POPULATION_SIZE:
            parent1 = select_parent(population, fitness_values)
            parent2 = select_parent(population, fitness_values)
            if random.random() < CROSSOVER_RATE:
                child = crossover(parent1, parent2)
            else:
                child = mutate(parent1)
            child = mutate_add_or_remove(child)
            new_population.append(child)

        population = new_population[:POPULATION_SIZE]
    final_best_genome = population[fitness_values.index(max(fitness_values))]
    final_decrypted_indices = cipher.encrypt(ciphertext, final_best_genome)
    final_plaintext = ''.join(chr(alphabet[i]) for i in final_decrypted_indices)
    if(fitness(final_plaintext)< fitness(ogtx)):
        return ogtx
    return final_plaintext



def crossover(parent1, parent2):
    """
    Esegue il crossover tra due genitori garantendo che il figlio
    sia una lista strettamente crescente di numeri unici.

    :param parent1: Primo genitore (numpy array o lista strettamente crescente)
    :param parent2: Secondo genitore (numpy array o lista strettamente crescente)
    :return: Figlio risultante dal crossover (numpy array)
    """
    # Converte i genitori in set per ottenere unione e intersezione
    set1, set2 = set(parent1), set(parent2)

    # Prende l'intersezione come base per il figlio
    common_elements = sorted(set1 & set2)

    # Prende elementi unici da ciascun genitore per completare il figlio
    unique_elements1 = sorted(set1 - set2)
    unique_elements2 = sorted(set2 - set1)

    # Combina in modo casuale per mantenere il risultato crescente
    child = common_elements + unique_elements1[:len(unique_elements1)//2] + unique_elements2[:len(unique_elements2)//2]
    child = sorted(child)

    # Assicurati che il figlio abbia una lunghezza valida (almeno 3 elementi)
    while len(child) < 3:
        possible_values = set(range(max(child) + 1)) - set(child)
        if possible_values:
            child.append(min(possible_values))
        child = sorted(child)

    return list_to_NDA(child)





if __name__ == '__main__':

    print(fitness("TOOONAWTWONFBSEEUOVIBOAYETHEIAOFBUTNUNTENDONTHEEHWARFSTANNIOTHESDFIHTHENORWFDAHWSITHEATHEDAETIOSBWCATEODDIAFDIDSUATODOEDASUNGUIRISENWIFESISDNINONEATFSDBDSSHEOUTNFAFFUNDWNBWBEBDSBDDWGOFTSUUAEUHWIUA"))