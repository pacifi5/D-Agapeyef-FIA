import joblib
import pandas as pd
import utils as Cipher
from sklearn.preprocessing import LabelEncoder
import warnings
from sklearn.exceptions import InconsistentVersionWarning


warnings.filterwarnings("ignore", category=InconsistentVersionWarning)


modello = joblib.load('Jupyter Notebooks/Dagapeyeff.joblib')
cifrario = input("Inserisci cifrario\n")

new_data = {
    'Text': [cifrario],
    'IC': [Cipher.indice_di_coincidenza(cifrario)],
    'Top9Letters': [Cipher.get_top9_chars(cifrario).lower],
    'Top5Bigrams': [Cipher.get_top_5_bigrams(cifrario).lower]
}


# Convert the new data into a DataFrame
new_df = pd.DataFrame(new_data,index=[0])

# Transform the new data using the same label encoders
for column in new_df.columns:
        if new_df[column].dtype == 'object':  

            label_encoder = LabelEncoder()
            new_df[column] = label_encoder.fit_transform(new_df[column])


# Predict the cipher type for the new data
predicted_cipher = modello.predict(new_df)
# Output the prediction
print(f"The predicted cipher type is: {predicted_cipher[0]}")
