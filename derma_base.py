from pydantic import BaseModel, Field
from typing import Literal, Optional

class DermaInput(BaseModel):
    Gender: Literal['Male', 'Female']
    Age: float
    Height: float
    Weight: float
    FamilyHistory: Literal['no', 'yes']
    FAVC: Literal['no', 'yes']
    FCVC: float
    NCP: float
    CAEC: Literal['no', 'Sometimes', 'Frequently', 'Always']
    SMOKE: Literal['no', 'yes']
    CH2O: float
    SCC: Literal['no', 'yes']
    FAF: float
    TUE: float
    CALC: Literal['no', 'Sometimes', 'Frequently', 'Always']
    MTRANS: Literal['Public_Transportation', 'Automobile', 'Walking', 'Motorbike', 'Bike']

class PredictionResult(BaseModel):
    predicted_Result: Literal['Insufficient_Weight', 'Normal_Weight',
                                  'Overweight_Level_I', 'Overweight_Level_II',
                                  'Obesity_Type_I', 'Obesity_Type_II', 'Obesity_Type_III']