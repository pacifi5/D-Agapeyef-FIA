from collections import Counter
def get_top9_chars(testo):
    testo_senza_spazi = testo.replace(" ", "")
    
    contatore = Counter(testo_senza_spazi)
    
    nove_comuni = contatore.most_common(9)
    
    caratteri_piu_usati = ''.join([carattere for carattere, _ in nove_comuni])
    
    return caratteri_piu_usati


def all_piu_usati(testo):
    testo_senza_spazi = testo.replace(" ", "")
    
    contatore = Counter(testo_senza_spazi)
    
    piu_comuni = contatore.most_common(26)
    
    caratteri_piu_usati = ''.join([carattere for carattere, _ in piu_comuni])
    
    return caratteri_piu_usati


def get_top_5_bigrams(text:str):
    text=text.lower()
    text = text.replace(" ", "")
    bigrams = [text[i:i+2] for i in range(len(text)-1)]
    bigram_counter = Counter(bigrams)
    most_common_bigrams = [bigram for bigram, _ in bigram_counter.most_common(5)]
    return ' '.join(most_common_bigrams)


def indice_di_coincidenza(testo):
    testo = testo.replace(" ", "").lower()
    
    n = len(testo)
    
    frequenze = Counter(testo)
    
    IC = sum(f * (f - 1) for f in frequenze.values()) / (n * (n - 1)) if n > 1 else 0
    
    return IC



if __name__ == '__main__':
    x = indice_di_coincidenza("EYLEUNIBSHEORYXILOOYREELSOWCSOTLUVOEMSETSHUEU")
    print(x)