import uvicorn
from fastapi import FastAPI, HTTPException
import pickle
import pandas as pd
import numpy as np

from derma_base import DermaInput, PredictionResult
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder

app = FastAPI()

MODEL_PATH = 'fp_fin_mod.pkl'
ORD_ENC_PATH = 'fp_ord_enc.pkl'
OHE_ENC_PATH = 'fp_ohe_enc.pkl'
TRG_ENC_PATH = 'fp_trg_enc.pkl'
FTR_ORD_PATH = 'fp_ftr_ord.pkl'

classifier = None
_ordinal_encoders_map = None
_onehot_encoder = None
_target_encoder = None
MODEL_FEATURES_ORDER = None

with open(MODEL_PATH, 'rb') as f:
    classifier = pickle.load(f)

with open(ORD_ENC_PATH, 'rb') as f:
    _ordinal_encoders_map = pickle.load(f)
with open(OHE_ENC_PATH, 'rb') as f:
    _onehot_encoder = pickle.load(f)
with open(TRG_ENC_PATH, 'rb') as f:
    _target_encoder = pickle.load(f)
with open(FTR_ORD_PATH, 'rb') as f:
    MODEL_FEATURES_ORDER = pickle.load(f)

@app.get("/")
async def root():
    return {"message": "Obesity Level Predictor API"}

@app.post('/predict', response_model=PredictionResult)
def predict(data: DermaInput):
    raw_input_df = pd.DataFrame([data.model_dump()])

    processed_features_df = raw_input_df.copy()

    numeric_features_list = ['Age', 'Height', 'Weight', 'FCVC', 'NCP', 'CH2O', 'FAF', 'TUE']
    for col in numeric_features_list:
        if col in raw_input_df.columns:
            processed_features_df[col] = raw_input_df[col]

    for col, encoder in _ordinal_encoders_map.items():
        processed_features_df[col] = encoder.transform(raw_input_df[[col]].values.reshape(-1, 1))
        
    mtrans_encoded_data = _onehot_encoder.transform(raw_input_df[['MTRANS']].values.reshape(-1, 1))
    mtrans_encoded_df = pd.DataFrame(mtrans_encoded_data, columns=_onehot_encoder.get_feature_names_out(['MTRANS']))
    
    if 'MTRANS' in processed_features_df.columns:
        processed_features_df.drop(columns=['MTRANS'], inplace=True)

    final_input_df = pd.concat([processed_features_df.reset_index(drop=True), mtrans_encoded_df.reset_index(drop=True)], axis=1)
    final_input_df = final_input_df[MODEL_FEATURES_ORDER]
    
    prediction_encoded = classifier.predict(final_input_df)
    predicted_label = _target_encoder.inverse_transform(prediction_encoded.reshape(-1, 1))[0][0]

    return PredictionResult(predicted_Result=predicted_label)

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)