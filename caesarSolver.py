import string 
from time import sleep 
import commons
import trigrammi
import monosolver as monosolver
alphabet = string.ascii_lowercase # "abcdefghijklmnopqrstuvwxyz" 
dizionario_valutazione = trigrammi.trigrams
parole_comuni = commons.commons
def decrypt(encrypted_message:str,key:int): 
     
     
    decrypted_message = []
 
    for c in encrypted_message: 
 
        if c in alphabet: 
            position = alphabet.find(c) 
            new_position = (position - key) % 26 
            new_character = alphabet[new_position] 
            decrypted_message.append(new_character) 
        else: 
            decrypted_message += c 
        
    return ''.join(decrypted_message)
    
def fitness(testo:str):
    testo = testo.upper()
    valutazione = 0.0
    for elem in parole_comuni:
        if elem in testo:
            valutazione += elem.length()/200.0
    trigrams = [testo[i:i+3] for i in range(len(testo)-1)]
    for tri in trigrams:
        if tri in dizionario_valutazione:
            valutazione += dizionario_valutazione[tri]
    return valutazione

def giveAllDecryptions(ciphertext:str):
    listOfDecryptions = []
    for key in range(26):
        text = decrypt(ciphertext,key)
        listOfDecryptions.append(text)
    return listOfDecryptions



def giveBestOfAll(listOfDecryptions):
    max = ''
    for elem in listOfDecryptions:
        if fitness(elem)>=fitness(max):
            max = elem
    
    if(len(max)/fitness(max)>1600):
        return -1
    print("Tentativo di risoluzione con Cesare:")
    return max




#<1600 circa è sbagliato
if __name__ == '__main__':
    lista = (giveAllDecryptions("cdzgkiluceuixsonczkddcogsarlkgczktkdzwsymdkdiumductmgymuksdsxwsyoaoszocii"))
    print(giveBestOfAll(lista))

