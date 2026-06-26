import streamlit as st
import requests


st.title(
    "Cardiovascular Risk Prediction System"
)

patient_id = st.text_input(
    "Patient ID"
)

patient_name = st.text_input(
    "Patient Name"
)

sex = {
    "Female": 0,
    "Male": 1
}[st.selectbox("Sex", ["Female", "Male"])]
age = st.selectbox(
    "Age",
    list(range(0, 100))
)

weight = st.number_input(
    "Weight (kg)"
)

height = st.number_input(
    "Height (m)"
)

bmi = st.number_input(
    "BMI"
)

abdominal = st.number_input(
    "Abdominal Circumference"
)

cholesterol = st.number_input(
    "Total Cholesterol"
)

hdl = st.number_input(
    "HDL"
)

sugar = st.number_input(
    "Fasting Blood Sugar"
)

smoking = {
    "No": 0,
    "Yes": 1
}[st.selectbox("Smoking", ["No", "Yes"])]

diabetes = {
    "No": 0,
    "Yes": 1
}[st.selectbox("Diabetes", ["No", "Yes"])]

activity = {
    "Low": 0,
    "Moderate": 1,
    "High": 2
}[st.selectbox(
    "Physical Activity",
    ["Low", "Moderate", "High"]
)]

family_history = {
    "No": 0,
    "Yes": 1
}[st.selectbox(
    "Family History of Heart Disease",
    ["No", "Yes"]
)]

waist_ratio = st.number_input(
    "Waist-to-Height Ratio"
)

systolic = st.number_input(
    "Systolic BP"
)

diastolic = st.number_input(
    "Diastolic BP"
)

ldl = st.number_input(
    "Estimated LDL"
)

if st.button(
    "Predict Risk"
):

    response = requests.get(

        "http://127.0.0.1:8000/predict",

        params={
            "patient_id": patient_id,
            "patient_name": patient_name,
            "sex": sex,
            "age": age,
            "weight": weight,
            "height": height,

            "bmi": bmi,

            "abdominal": abdominal,

            "cholesterol": cholesterol,

            "hdl": hdl,

            "sugar": sugar,

            "smoking": smoking,

            "diabetes": diabetes,

            "activity": activity,

            "family_history": family_history,

            "waist_ratio": waist_ratio,

            "systolic": systolic,

            "diastolic": diastolic,

            "ldl": ldl,


        }

    )

    result = response.json()

    st.success(

        f"Risk Score: {result['risk_score']}"

    )

    st.success(

        f"Risk Level: {result['prediction']}"

    )
