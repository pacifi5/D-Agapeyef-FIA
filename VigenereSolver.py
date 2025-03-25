import numpy as np
from cipherImplementations.cipher import Cipher, generate_random_keyword
import kasiski
import trigrammi
import random
import string
import utili as UC
import commons

# Dati per la valutazione del fitness
dizionario_valutazione = trigrammi.trigrams
parole_comuni = commons.commons

# Parametri dell'algoritmo genetico
POPULATION_SIZE = 6000
MUTATION_RATE = 0.8  
MUTATION_RATE2 = 0.3 
CROSSOVER_RATE = 0.7  
GENERATIONS = 2000
TOURNAMENT_SIZE = 10 
MAX_FITNESS = 0
BEST_TEXT = ""

def fitness(testo: str):
    """
    Valuta il fitness del testo decifrato basandosi sulla frequenza dei trigrammi
    e sulla presenza di parole comuni.
    """
    testo = testo.lower()
    valutazione = 0.0

    for parola in parole_comuni:
        if parola.lower() in testo:
            valutazione += len(parola) / 200.0

    trigrams = [testo[i:i + 3] for i in range(len(testo) - 2)]
    global MAX_FITNESS, BEST_TEXT
    for tri in trigrams:
        if tri in dizionario_valutazione:
            valutazione += dizionario_valutazione[tri]
        if valutazione > MAX_FITNESS:
            MAX_FITNESS = valutazione
            BEST_TEXT = testo
    return valutazione

def mutate(chiave):
    if random.random() > MUTATION_RATE:
        return chiave
   
    chiave = list(chiave)
    indice = random.randint(0, len(chiave) - 1)
    lettera = chiave[indice]
    if random.choice([True, False]):
        if lettera == 'z':
            chiave[indice] = 'a'  
        else:
            chiave[indice] = chr(ord(lettera) + 1)
    else:
        if lettera == 'a':
            chiave[indice] = 'z'  
        else:
            chiave[indice] = chr(ord(lettera) - 1)
    return ''.join(chiave)

def mutate2(chiave):
    if random.random() < MUTATION_RATE2:
        chiave = list(chiave)
        if random.choice([True, False]):
            lettera_casuale = random.choice(string.ascii_lowercase)
            random_index = random.randint(0, len(chiave) - 1)
            chiave.insert(random_index, lettera_casuale)
            return ''.join(chiave)
        else:
            if len(chiave) > 3:
                random_index = random.randint(0, len(chiave) - 1)
                chiave.pop(random_index)
            return ''.join(chiave)
    return chiave

def crossover(genitore1, genitore2):
    if random.random() > CROSSOVER_RATE:
        return genitore1, genitore2
    # Scegli un punto di crossover casuale
    punto_crossover = random.randint(1, min(len(genitore1), len(genitore2)) - 1)
    # Crea i figli mescolando i segmenti dei genitori
    figlio1 = genitore1[:punto_crossover] + genitore2[punto_crossover:]
    figlio2 = genitore2[:punto_crossover] + genitore1[punto_crossover:]
    return figlio1, figlio2


def initial_population(kasiskiTestList, POPULATION_SIZE, ciphertext):
    if kasiskiTestList == -1:
        popolazione = [''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 14))) for _ in range(POPULATION_SIZE)]
    else:
        kasiskiTestList = kasiskiTestList[:3]
        templist = [(N * 2, int(M / 2)) for N, M in kasiskiTestList[:2]]
        kasiskiTestList.extend(templist)  
        popolazione = []
        while len(popolazione) < POPULATION_SIZE:
            for N, M in kasiskiTestList:
                for _ in range(M):
                    chiave = ''.join(random.choices(string.ascii_lowercase, k=N))
                    popolazione.append(chiave)
                    if len(popolazione) >= POPULATION_SIZE:
                        break
                if len(popolazione) >= POPULATION_SIZE:
                    break

    # Ordinamento basato sul fitness della decifratura
    vig = Vigenere("abcdefghijklmnopqrstuvwxyz", " ", "-")
    popolazione.sort(key=lambda key: fitness(vig.decrypt(ciphertext, key)), reverse=True)
    return popolazione



def select_parent(population, fitness_values, tournament_size=TOURNAMENT_SIZE):
    """
    Seleziona un genitore utilizzando la selezione a torneo.
    """
    tournament = random.sample(list(zip(population, fitness_values)), tournament_size)
    tournament = sorted(tournament, key=lambda x: x[1], reverse=True)
    return tournament[0][0]


def decodifica(ciphertext: str):
    print("Tentativo di decodifica Vigenere:\n")
    """
    Decifra il ciphertext utilizzando un algoritmo genetico.
    """
    ciphertext = ciphertext.lower()
    ciphertext = ciphertext.replace(" ", "")
    global POPULATION_SIZE
    population = initial_population(kasiski.KasiskiTest(ciphertext).attack(), POPULATION_SIZE,ciphertext)
    POPULATION_SIZE=500
    global MAX_FITNESS, BEST_TEXT
    
    MAX_FITNESS = 0
    BEST_TEXT = ""
    vig = Vigenere("abcdefghijklmnopqrstuvwxyz", " ", "-")
    for gen in range(1, GENERATIONS + 1):
        fitness_values = [fitness(vig.decrypt(ciphertext, genome)) for genome in population]
        sorted_population = [genome for _, genome in sorted(zip(fitness_values, population), key=lambda x: x[0], reverse=True)]
        sorted_fitness = sorted(fitness_values, reverse=True)
        if gen % 20 == 0 or gen == 1:
            best_genome = sorted_population[0]
            best_fitness = sorted_fitness[0]
            best_plaintext = vig.decrypt(ciphertext, best_genome)
            print(f"Generazione {gen}: Fitness={best_fitness} Chiave={best_genome}")
            print(best_plaintext)
            print("-" * 50)
        new_population = [best_genome] 
        # Genera la nuova popolazione tramite crossover e mutazione
        while len(new_population) < POPULATION_SIZE:
            parent1 = select_parent(sorted_population, sorted_fitness)
            parent2 = select_parent(sorted_population, sorted_fitness)
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1)
            child2 = mutate2(child2)
            new_population.extend([child1, child2])
        population = new_population[:POPULATION_SIZE]
    fitness_values = [fitness(vig.decrypt(ciphertext, genome)) for genome in population]
    best_genome = population[fitness_values.index(max(fitness_values))]
    plaintext = vig.decrypt(ciphertext, best_genome)
    print("Miglior soluzione finale:")
    print(plaintext)
    return plaintext

class Vigenere(Cipher):
    def __init__(self, alphabet, unknown_symbol=None, unknown_symbol_number=-1):
        self.alphabet = alphabet
        self.unknown_symbol = unknown_symbol if unknown_symbol else '?'
        self.unknown_symbol_number = unknown_symbol_number
        self.alphabet_size = len(alphabet)

    def generate_random_key(self, length):
        return generate_random_keyword(self.alphabet, length)

    def _char_to_index(self, char):
        """Converte un carattere nel suo indice corrispondente nell'alfabeto."""
        if char in self.alphabet:
            return self.alphabet.index(char)
        return self.unknown_symbol_number

    def _index_to_char(self, index):
        """Converte un indice nel carattere corrispondente nell'alfabeto."""
        if index >= 0 and index < self.alphabet_size:
            return self.alphabet[index]
        return self.unknown_symbol

    def encrypt(self, plaintext, key):
        """Cifra il plaintext usando la chiave e l'alfabeto."""
        ciphertext = []
        key_length = len(key)

        for i, char in enumerate(plaintext):
            p_index = self._char_to_index(char)
            if p_index == self.unknown_symbol_number:
                ciphertext.append(self.unknown_symbol)  
                continue

            k_index = self._char_to_index(key[i % key_length])
            c_index = (p_index + k_index) % self.alphabet_size
            ciphertext.append(self._index_to_char(c_index))
        return ''.join(ciphertext)


    def decrypt(self, ciphertext, key):
        """Decifra il ciphertext usando la chiave e l'alfabeto."""
        plaintext = []
        key_length = len(key)
        for i, char in enumerate(ciphertext):
            c_index = self._char_to_index(char)
            if c_index == self.unknown_symbol_number:
                plaintext.append(self.unknown_symbol)  
                continue
            k_index = self._char_to_index(key[i % key_length])
            p_index = (c_index - k_index) % self.alphabet_size
            plaintext.append(self._index_to_char(p_index))
        return ''.join(plaintext)


if __name__ == '__main__':
    cif = "YPVWHMAFAJIGSMSOFZRQXMMYMYKWFAKLRVMSLXIASPDZLWGKIIBYVBTKMBYIGQIJAKLRBSQWIWBEXMMJOLAPJVUIQHRFAFJGFVFLZIASSKXZRXZRIWIEAFIGQIHFEPJERGENWXBYIUNVNHFRGGINZNMAFWHCKXVMKYPISHFLYPVEVQANBYKEZGJIWIRKMSOFJPZPRAVXGKIIWMIESLJTRRQZRINFVNLSRMEXRUIWGKLVMKKMCXFSMQTRRQSMRMCIFRXMMUELVEXNRHVMKFVURVFLYERWBMMYANELAYYNFVANAYPVVRVEXWEPLOIFKVEACUZQVX"
    decodifica(cif)