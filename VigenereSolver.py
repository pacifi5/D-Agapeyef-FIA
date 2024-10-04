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
POPULATION_SIZE = 400  # Mantiene la diversità con un costo computazionale ragionevole
GENOME_LENGTH = 26  # Fisso per il problema
MUTATION_RATE = 0.6 # Evita troppi cambiamenti casuali, mantenendo comunque la diversità
MUTATION_RATE2 = 0.2
CROSSOVER_RATE = 0.4  # Combina efficacemente le soluzioni dei genitori
GENERATIONS = 2000
MAX_FITNESS = 0
BEST_TEXT = ""


def fitness(testo: str):
    """
    Valuta il fitness del testo decifrato basandosi sulla frequenza dei trigrammi
    e sulla presenza di parole comuni.
    """
    testo = testo.lower()
    valutazione = 0.0

    # Valutazione basata sulle parole comuni
    for parola in parole_comuni:
        if parola.lower() in testo:
            valutazione += len(parola) / 200.0

    # Valutazione basata sui trigrammi
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
    # Trasforma la stringa in una lista mutabile
    chiave = list(chiave)
    
    # Seleziona un indice casuale della stringa
    indice = random.randint(0, len(chiave) - 1)
    
    # Ottieni la lettera all'indice selezionato
    lettera = chiave[indice]
    
    # Scelta casuale tra incrementare o decrementare
    if random.choice([True, False]):
        # Incrementa la lettera
        if lettera == 'z':
            chiave[indice] = 'a'  # Wrap-around
        else:
            chiave[indice] = chr(ord(lettera) + 1)
    else:
        # Decrementa la lettera
        if lettera == 'a':
            chiave[indice] = 'z'  # Wrap-around
        else:
            chiave[indice] = chr(ord(lettera) - 1)
    
    # Ritorna la nuova stringa mutata
    return ''.join(chiave)



def mutate2(chiave):
    if random.random() < MUTATION_RATE2:
        chiave = list(chiave)
        lettera_casuale = random.choice(string.ascii_lowercase)
        chiave.append(lettera_casuale)
        
        return ''.join(chiave)
    
    return chiave


def crossover(genitore1, genitore2):
    # Scegli un punto di crossover casuale
    punto_crossover = random.randint(1, len(genitore1) - 1)
    
    # Crea i figli mescolando i segmenti dei genitori
    figlio1 = genitore1[:punto_crossover] + genitore2[punto_crossover:]
    figlio2 = genitore2[:punto_crossover] + genitore1[punto_crossover:]
    
    return figlio1, figlio2


def initial_population(kasiskiTestList, POPULATION_SIZE):
    kasiskiTestList = kasiskiTestList[:3]
    templist = []

    # Modifica della lista kasiskiTestList con tuple raddoppiate
    for N, M in kasiskiTestList:
        templist.append((N * 2, M))

    kasiskiTestList.extend(templist)  # Aggiungi le tuple raddoppiate

    popolazione = []

    while len(popolazione) < POPULATION_SIZE:
        # Genera la popolazione in base alla bontà (frequenza M)
        for N, M in kasiskiTestList:
            for _ in range(M):
                # Genera una stringa casuale di lunghezza N
                chiave = ''.join(random.choices(string.ascii_lowercase, k=N))
                popolazione.append(chiave)
                if len(popolazione) >= POPULATION_SIZE:
                    break
            if len(popolazione) >= POPULATION_SIZE:
                break

    # Shuffle finale della popolazione
    random.shuffle(popolazione)

    print(f"Dimensione popolazione finale: {len(popolazione)}")
    return popolazione


def select_parent(population, fitness_values):
    """
    Seleziona un genitore utilizzando la selezione per roulette basata sul fitness.
    """
    total_fitness = sum(fitness_values)
    if total_fitness == 0:
        return random.choice(population)
    selection_probs = [f / total_fitness for f in fitness_values]
    return random.choices(population, weights=selection_probs, k=1)[0]

def decodifica(ciphertext: str):
    print("Tentativo di decodifica Vigenere:\n")
    """
    Decifra il ciphertext utilizzando un algoritmo genetico.
    """
    ciphertext = ciphertext.lower()
    population = initial_population(kasiski.KasiskiTest(ciphertext).attack(),POPULATION_SIZE)

    global MAX_FITNESS, BEST_TEXT
    MAX_FITNESS = 0
    BEST_TEXT = ""
    vig = Vigenere("ABCDEFGHIJKLMNOPQRSTUVWXYZ".lower(), " ", " ")

    for gen in range(1, GENERATIONS + 1):
        # Calcola i valori di fitness per la popolazione corrente
        fitness_values = [fitness(vig.decrypt(ciphertext, genome)) for genome in population]
        # Trova il genoma con il miglior fitness
        max_fitness = max(fitness_values)
        best_genome = population[fitness_values.index(max_fitness)]
        best_plaintext = vig.decrypt(ciphertext, best_genome)

        if(gen == 1):
            best_plaintext = vig.decrypt(ciphertext,best_genome)

        # Stampa il miglior risultato ogni 100 generazioni
        if gen % 100 == 0 or gen == 1:
            print(f"Generazione {gen}: Fitness={max_fitness} Chiave={best_genome}")
            print(best_plaintext)
            print("-" * 50)

        new_population = [best_genome] #elitismo       

        # Genera il resto della nuova popolazione tramite crossover e mutazione
        while len(new_population) < POPULATION_SIZE:
            parent1 = select_parent(population, fitness_values)
            parent2 = select_parent(population, fitness_values)
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1)
            child2 = mutate(child2)
            child1 = mutate2(child1)
            child2 = mutate(child2)
            new_population.extend([child1, child2])

        population = new_population[:POPULATION_SIZE]

    # Dopo tutte le generazioni, trova la migliore soluzione
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
                ciphertext.append(self.unknown_symbol)  # Simbolo sconosciuto
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
                plaintext.append(self.unknown_symbol)  # Simbolo sconosciuto
                continue

            k_index = self._char_to_index(key[i % key_length])
            p_index = (c_index - k_index) % self.alphabet_size
            plaintext.append(self._index_to_char(p_index))

        return ''.join(plaintext)








if __name__ == '__main__':
    decodifica("fntlvsnkekwwgoebrgoenruwuocrnczzcruibdvntatucbptseueasofnbqpjnraadlfrsuifpeaptotiajcpuecbmvieuhrtibnbfciigwioeagyiyywvopcoghvmvioihcpuevbcgsuydvzaadhnjvrfweodvntolxrnpqbrnnqwuidbuhfrghrtkotfeimojaeejvsvjrfdgouergybxhfvrlbpcyiyhkjvvntyulaalrttnngebrlhdxjoaosyulrcushrrsf".lower())