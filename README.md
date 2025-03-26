# D'Agapeyef-FIA

## Introduzione
D'Agapeyef-FIA è un progetto sviluppato nel corso di Fondamenti di Intelligenza Artificiale con l'obiettivo di riconoscere e decifrare testi cifrati in quattro tecniche diverse utilizzando tecniche di Machine Learning e Algoritmi Genetici.

## Tipi di Cifrari Supportati
1. **Sostituzione Monoalfabetica**
2. **Cifrario di Cesare**
3. **Cifrario di Vigenère**
4. **Trasposizione Colonnare**


## Obiettivi del Progetto
Il software è progettato per:
1. Riconoscere il metodo di cifratura utilizzato su un testo cifrato.
2. Individuare la chiave corretta per decifrare il testo.
3. Implementare un agente intelligente che utilizza metodi crittoanalitici e tecniche di apprendimento automatico.

## Tecniche Utilizzate
- **Machine Learning**: Per il riconoscimento del cifrario viene utilizzato un **RandomForestClassifier**, addestrato su un dataset generato ad-hoc.
- **Algoritmi Genetici**: Per la decodifica del testo cifrato, con diverse strategie per mutazione, selezione e crossover.
- **Tecniche di analisi crittografica**: Per migliorare la robustezza del riconoscimento del cifrario.

### Prerequisiti
Sono necessari **Python 3.8+** e i seguenti pacchetti:
```sh
pip install numpy pandas scikit-learn matplotlib joblib
```
