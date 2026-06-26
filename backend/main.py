from fastapi import FastAPI
import joblib
import numpy as np
import sqlite3
from datetime import datetime

app = FastAPI()


score_model = joblib.load(
    '../model/score_model.pkl'
)

level_model = joblib.load(
    '../model/cvd_model.pkl'
)
conn = sqlite3.connect(
    '../database/patients.db',
    check_same_thread=False
)

cursor = conn.cursor()


cursor.execute("""

CREATE TABLE IF NOT EXISTS patients (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    patient_id TEXT,

    patient_name TEXT,

    risk_score REAL,

    risk_level TEXT,

    created_at TEXT

)

""")

conn.commit()

labels = {

    0: "LOW",

    1: "INTERMEDIARY",

    2: "HIGH"

}


@app.get("/")
def home():

    return {
        "message": "CVD Prediction API Running"
    }


@app.get("/predict")
def predict(
    patient_id: str,
    patient_name: str,
    sex: int,
    age: float,
    weight: float,
    height: float,

    bmi: float,

    abdominal: float,

    cholesterol: float,

    hdl: float,

    sugar: float,

    smoking: int,

    diabetes: int,

    activity: int,

    family_history: int,

    waist_ratio: float,

    systolic: float,

    diastolic: float,

    ldl: float,

):

    data = np.array([[

        sex,
        age,
        weight,
        height,

        bmi,

        abdominal,

        cholesterol,

        hdl,

        sugar,

        smoking,

        diabetes,

        activity,

        family_history,

        waist_ratio,

        systolic,

        diastolic,

        ldl

    ]])

    score = score_model.predict(
        data
    )[0]

    data_with_score = np.append(
        data,
        score
    ).reshape(1, -1)

    prediction = level_model.predict(
        data_with_score
    )[0]

    cursor.execute(

        """

        INSERT INTO patients (

            patient_id,
            patient_name,

            risk_score,
            risk_level,

            created_at

        )

        VALUES (?,?,?,?,?)

        """,

        (

            patient_id,
            patient_name,

            round(score, 2),

            labels[prediction],

            str(datetime.now())

        )

    )

    conn.commit()

    return {

        "risk_score": round(score, 2),

        "prediction": labels[prediction]

    }
