import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Carica il modello
modello = joblib.load('Dagapeyeff.joblib')

# Nuovi dati
cipher = 'ZKHQ ZRUG VHSDUDWLRQ EHFDPH WKH VWDQGDUG VBVWHP LW ZDV VHHQ DV D VLPSOLILFDWLRQ RI URPDQ FXOWXUH EHFDXVH LW XQGHUPLQHG WKH PHWULF DQG UKBWKPLF IOXHQFB JHQHUDWHG WKURXJK VFULSWLR FRQWLQXD LQ FRQWUDVW SDOHRJUDSKHUV WRGDB LGHQWLIB WKH HAWLQFWLRQ RI VFULSWLR FRQWLQXD DV D FULWLFDO IDFWRU LQ DXJPHQWLQJ WKH ZLGHVSUHDG DEVRUSWLRQ RI NQRZOHGJH LQ WKH SUHPRGHUQ HUD'

new_data = {
    'Text' : [cipher],
    'IC': [0.06583],
    'Top9Letters': ['hwlqdurvf'],
    'Top5Bigrams': ['WL RQ AV UL KH']
}


# Convert the new data into a DataFrame
new_df = pd.DataFrame(new_data)

# Transform the new data using the same label encoders
for column in new_df.columns:
        label_encoder = LabelEncoder()
        new_df[column] = label_encoder.fit_transform(new_df[column])



# Load the trained model
model = joblib.load('Dagapeyeff.joblib')

# Predict the cipher type for the new data
predicted_cipher = model.predict(new_df)

# Output the prediction
print(f"The predicted cipher type is: {predicted_cipher[0]}")