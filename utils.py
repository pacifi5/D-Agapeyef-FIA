from collections import Counter
def get_top9_chars(testo):
    # Rimuovi gli spazi dal testo
    testo_senza_spazi = testo.replace(" ", "")
    
    # Conta la frequenza di ogni carattere nel testo
    contatore = Counter(testo_senza_spazi)
    
    # Ottieni i 9 caratteri più comuni
    nove_comuni = contatore.most_common(9)
    
    # Estrai solo i caratteri, ignorando le frequenze
    caratteri_piu_usati = ''.join([carattere for carattere, _ in nove_comuni])
    
    return caratteri_piu_usati


# Funzione per ottenere i 5 bigrammi più comuni
def get_top_5_bigrams(text:str):
    text=text.lower()
    text = text.replace(" ", "")
    # Creiamo una lista di bigrammi (coppie di lettere consecutive)
    bigrams = [text[i:i+2] for i in range(len(text)-1)]
    # Contiamo la frequenza di ogni bigramma
    bigram_counter = Counter(bigrams)
    # Otteniamo i 5 bigrammi più comuni
    most_common_bigrams = [bigram for bigram, _ in bigram_counter.most_common(5)]
    # Uniamo la lista in una stringa e la ritorniamo
    return ' '.join(most_common_bigrams)


def indice_di_coincidenza(testo):
    # Rimuovi gli spazi e trasforma tutto in maiuscolo (o minuscolo) per uniformità
    testo = testo.replace(" ", "").lower()
    
    # Calcola la lunghezza del testo
    n = len(testo)
    
    # Conta la frequenza di ogni carattere
    frequenze = Counter(testo)
    
    # Calcola l'indice di coincidenza
    IC = sum(f * (f - 1) for f in frequenze.values()) / (n * (n - 1)) if n > 1 else 0
    
    return IC



if __name__ == '__main__':
    x = get_top_5_bigrams("L IHHO OLNH WKLV ZRUNV EHVW RQ VKRUW PHVVDJHV RU PDBEH WKRVH ZLWK DYHUDJH OHQJWKI")
    print(x)