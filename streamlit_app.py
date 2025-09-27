import streamlit as st
import requests
import json

FASTAPI_URL = "http://127.0.0.1:8000/predict"

st.set_page_config(page_title="Obesity Level Predictor", layout="centered")
st.title("Obesity Level Prediction")

col1, col2, col3, col4 = st.columns(4)
with col1:
    gender = st.selectbox("Gender", ["Male", "Female"])
with col2:
    age = st.number_input("Age (Years)", min_value=10, max_value=80, value=20)
with col3:
    height = st.number_input("Height (meters)", min_value=1.45, max_value=1.95, value=1.81, format="%.2f")
with col4:
    weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=75.0, format="%.2f")

col5, col6 = st.columns(2)
with col5:
    family_history = st.selectbox("Family History with Overweight", ["no", "yes"], key="family_history_select")
with col6:
    smoke = st.selectbox("Smokes", ["no", "yes"], key="smoke_select")


col7, col8 = st.columns(2)
with col7:
    favc = st.selectbox("Frequent Consumption of High Caloric Food", ["no", "yes"], key="favc_select")
with col8:
    scc = st.selectbox("Monitors Calorie Consumption", ["no", "yes"], key="scc_select")



col9, col10, col11 = st.columns(3)
with col9:
    ncp = st.slider("Number of Main Meals (per day)", min_value=1.0, max_value=4.0, value=3.0, step=0.01)
with col10:
    fcvc = st.slider("Freq of Vegetable Consumption (1-3)", min_value=1.0, max_value=3.0, value=2.0, step=0.01)
with col11:
    ch2o = st.slider("Daily Water Intake (1-3 liters/day)", min_value=1.0, max_value=3.0, value=2.0, step=0.01)

col12, col13 = st.columns(2)
with col12:
    faf = st.slider("Freq of Physical Activity (0-3 days/week)", min_value=0.0, max_value=3.0, value=1.0, step=0.1)
with col13:
    tue = st.slider("Time Using Technology (0-3 hours/day)", min_value=0.0, max_value=3.0, value=1.0, step=0.1)

col14, col15, col16 = st.columns(3)
with col9:
    caec = st.selectbox("Consumption of Food Between Meals", ["no", "Sometimes", "Frequently", "Always"])
with col10:
    calc = st.selectbox("Frequency of Alcohol Consumption", ["no", "Sometimes", "Frequently", "Always"])
with col11:
    mtrans = st.selectbox("Main Transportation Mode", ["Public_Transportation", "Automobile", "Walking", "Motorbike", "Bike"])


if st.button("Predict Obesity Level"):
    input_data = {
        "Gender": gender,
        "Age": float(age),
        "Height": float(height),
        "Weight": float(weight),
        "FamilyHistory": family_history,
        "FAVC": favc,
        "FCVC": float(fcvc),
        "NCP": float(ncp),
        "CAEC": caec,
        "SMOKE": smoke,
        "CH2O": float(ch2o),
        "SCC": scc,
        "FAF": float(faf),
        "TUE": float(tue),
        "CALC": calc,
        "MTRANS": mtrans
    }

    response = requests.post(FASTAPI_URL, json=input_data)
    prediction = response.json()
    predicted_level = prediction.get("predicted_Result")
    st.success(f"Predicted Obesity Level: **{predicted_level.replace('_', ' ')}**")
