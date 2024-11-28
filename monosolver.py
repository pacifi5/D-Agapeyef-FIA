import trigrammi
import random
import string
import utili as UC
import commons


# Dati per la valutazione del fitness
dizionario_valutazione = trigrammi.trigrams
parole_comuni = commons.commons


POPULATION_SIZE = 800  
GENOME_LENGTH = 26  
MUTATION_RATE = 0.6 
CROSSOVER_RATE = 0.4 
GENERATIONS = 1200
MAX_FITNESS = 0
BEST_TEXT = ""


def inject_init_population(ciphertext):
    """
    Crea una chiave iniziale mappando le lettere più comuni in inglese
    alle lettere più comuni nel ciphertext.
    """
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']
    most_commons = ['e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd', 'l', 'c', 'u', 'm', 'w', 'f', 'g', 'y', 'p', 'b',
                    'v', 'k', 'j', 'x', 'q', 'z']
    cipher_most_commons = list(UC.all_piu_usati(ciphertext).lower())

    mapping = {}
    used_chars = set()

    # Mappa le lettere più comuni in inglese alle lettere più comuni nel ciphertext
    for mc, cmc in zip(most_commons, cipher_most_commons):
        if cmc not in used_chars:
            mapping[mc] = cmc
            used_chars.add(cmc)

    # Aggiungi le lettere rimanenti in modo casuale
    remaining_letters = [char for char in alphabet if char not in used_chars]
    random.shuffle(remaining_letters)

    key = []
    for char in alphabet:
        if char in mapping:
            key.append(mapping[char])
        else:
            key.append(remaining_letters.pop())

    
    return ''.join(key)


def convert(ciphertext, testkey):
    """
    Decodifica il ciphertext utilizzando la chiave fornita.
    """
    ciphertext = ciphertext.upper()
    testkey = testkey.upper()
    plaintext = []

    # Crea una mappa dalla chiave alla lettere in chiaro
    translation_map = {testkey[i]: chr(65 + i) for i in range(GENOME_LENGTH)}

    # Traduci il ciphertext utilizzando la mappa
    for char in ciphertext:
        if char in translation_map:
            plaintext.append(translation_map[char].lower())
        else:
            plaintext.append(char)  # Mantiene caratteri non alfabetici invariati

    return ''.join(plaintext).upper()


def fitness(testo: str):
    """
    Valuta il fitness del testo decifrato basandosi sulla frequenza dei trigrammi
    e sulla presenza di parole comuni.
    """
    testo = testo.upper()
    valutazione = 0.0

    # Valutazione basata sulle parole comuni
    for parola in parole_comuni:
        if parola.upper() in testo:
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


def random_genome():
    
    alfabeto = list(string.ascii_lowercase)
    random.shuffle(alfabeto)
    return ''.join(alfabeto)


def initial_population(pop_size):
    
    return [random_genome() for _ in range(pop_size)]


def select_parent(population, fitness_values):
   
    total_fitness = sum(fitness_values)
    if total_fitness == 0:
        return random.choice(population)
    selection_probs = [f / total_fitness for f in fitness_values]
    return random.choices(population, weights=selection_probs, k=1)[0]


def crossover(parent1, parent2):
 
    if random.random() > CROSSOVER_RATE:
        return parent1, parent2

    crossover_point = random.randint(1, GENOME_LENGTH - 2)
    child1 = parent1[:crossover_point]
    child2 = parent2[:crossover_point]

    # Aggiungi le lettere rimanenti preservando l'unicità
    def complete_child(child, parent):
        for gene in parent:
            if gene not in child:
                child += gene
                if len(child) == GENOME_LENGTH:
                    break
        return child

    child1 = complete_child(child1, parent2)
    child2 = complete_child(child2, parent1)

    return child1, child2


def mutate(genome):
    
    if random.random() < MUTATION_RATE:
        genome = list(genome)
        idx1, idx2 = random.sample(range(GENOME_LENGTH), 2)
        genome[idx1], genome[idx2] = genome[idx2], genome[idx1]
        return ''.join(genome)
    return genome

def forcemutate(genome):
 
    if True:
        genome = list(genome)
        idx1, idx2 = random.sample(range(GENOME_LENGTH), 2)
        genome[idx1], genome[idx2] = genome[idx2], genome[idx1]
        return ''.join(genome)
    return genome


def decodifica(ciphertext: str):
    print("Tentativo di decodifica sostituzione monoalfabetica:\n")
   

    # Inizializza la popolazione con soluzioni casuali e soluzioni basate su frequenza
    population = initial_population(POPULATION_SIZE - 20)

    for _ in range(20):
        population.append(inject_init_population(ciphertext))

    global MAX_FITNESS, BEST_TEXT
    MAX_FITNESS = 0
    BEST_TEXT = ""

    for gen in range(1, GENERATIONS + 1):
        # Calcola i valori di fitness per la popolazione corrente
        fitness_values = [fitness(convert(ciphertext, genome)) for genome in population]
       
        max_fitness = max(fitness_values)
        best_genome = population[fitness_values.index(max_fitness)]
        best_plaintext = convert(ciphertext, best_genome)

        if(gen == 1):
            best_genome = inject_init_population(ciphertext)
            best_plaintext = convert(ciphertext,best_genome)

       
        if gen % 100 == 0 or gen == 1:
            print(f"Generazione {gen}: Fitness={max_fitness}")
            print(best_plaintext)
            print("-" * 50)

        
        new_population = [best_genome] * 5  
        if(gen > 1000 ):
            new_population.append(best_genome)

        # Genera il resto della nuova popolazione tramite crossover e mutazione
        while len(new_population) < POPULATION_SIZE:
            parent1 = select_parent(population, fitness_values)
            parent2 = select_parent(population, fitness_values)
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1)
            child2 = mutate(child2)
            new_population.extend([child1, child2])

        population = new_population[:POPULATION_SIZE]

    # Dopo tutte le generazioni, trova la migliore soluzione
    fitness_values = [fitness(convert(ciphertext, genome)) for genome in population]
    best_genome = population[fitness_values.index(max(fitness_values))]
    plaintext = convert(ciphertext, best_genome)

    print(f"Miglior soluzione finale con valutazione{fitness(plaintext)}")
    print(plaintext)

    return plaintext



if __name__ == '__main__':
    print(fitness("TOOONAWTWONFBSEEUOVIBOAYETHEIAOFBUTNUNTENDONTHEEHWARFSTANNIOTHESDFIHTHENORWFDAHWSITHEATHEDAETIOSBWCATEODDIAFDIDSUATODOEDASUNGUIRISENWIFESISDNINONEATFSDBDSSHEOUTNFAFFUNDWNBWBEBDSBDDWGOFTSUUAEUHWIUA"))