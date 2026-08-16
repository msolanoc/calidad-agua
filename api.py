"""
API para el Sistema de Predicción de Calidad del Agua.
Requiere: pip install fastapi uvicorn joblib scikit-learn pandas
Ejecutar localmente: uvicorn api:app --reload
"""

from fastapi import FastAPI
from pydantic import BaseModel, Field
import joblib
import pandas as pd

app = FastAPI(title="API - Sistema de Predicción de Calidad del Agua")

# Cargamos el mismo pipeline (preprocesamiento + modelo) ya entrenado
modelo = joblib.load("modelo_calidad_agua.pkl")

# Mensajes según la predicción (0=Verde, 1=Amarillo, 2=Rojo)
# Mismos textos que ya usa interfaz.py, para no cambiar la experiencia del usuario
MENSAJES = {
    0: "🟢 Óptima: Apta para consumo y riego",
    1: "🟡 Precaución: Requiere filtración o tratamiento",
    2: "🔴 Crítica: No apta para uso humano ni agrícola",
}


class MuestraAgua(BaseModel):
    ALC_mg_L: float = Field(..., alias="ALC_mg/L")
    CONDUCT_mS_cm: float = Field(..., alias="CONDUCT_mS/cm")
    SDT_M_mg_L: float = Field(..., alias="SDT_M_mg/L")
    FLUORUROS_mg_L: float = Field(..., alias="FLUORUROS_mg/L")
    DUR_mg_L: float = Field(..., alias="DUR_mg/L")
    COLI_FEC_NMP_100_mL: float = Field(..., alias="COLI_FEC_NMP/100_mL")
    N_NO3_mg_L: float = Field(..., alias="N_NO3_mg/L")
    AS_TOT_mg_L: float = Field(..., alias="AS_TOT_mg/L")
    CD_TOT_mg_L: float = Field(..., alias="CD_TOT_mg/L")
    CR_TOT_mg_L: float = Field(..., alias="CR_TOT_mg/L")
    HG_TOT_mg_L: float = Field(..., alias="HG_TOT_mg/L")
    PB_TOT_mg_L: float = Field(..., alias="PB_TOT_mg/L")
    MN_TOT_mg_L: float = Field(..., alias="MN_TOT_mg/L")
    FE_TOT_mg_L: float = Field(..., alias="FE_TOT_mg/L")

    class Config:
        populate_by_name = True  # permite enviar tanto "ALC_mg_L" como "ALC_mg/L"


@app.get("/")
def home():
    return {"mensaje": "API del Sistema de Predicción de Calidad del Agua"}


@app.post("/predict")
def predecir(muestra: MuestraAgua):
    # Mismo orden y nombres de columnas exactos con los que se entrenó el modelo
    datos = pd.DataFrame([{
        "ALC_mg/L": muestra.ALC_mg_L,
        "CONDUCT_mS/cm": muestra.CONDUCT_mS_cm,
        "SDT_M_mg/L": muestra.SDT_M_mg_L,
        "FLUORUROS_mg/L": muestra.FLUORUROS_mg_L,
        "DUR_mg/L": muestra.DUR_mg_L,
        "COLI_FEC_NMP/100_mL": muestra.COLI_FEC_NMP_100_mL,
        "N_NO3_mg/L": muestra.N_NO3_mg_L,
        "AS_TOT_mg/L": muestra.AS_TOT_mg_L,
        "CD_TOT_mg/L": muestra.CD_TOT_mg_L,
        "CR_TOT_mg/L": muestra.CR_TOT_mg_L,
        "HG_TOT_mg/L": muestra.HG_TOT_mg_L,
        "PB_TOT_mg/L": muestra.PB_TOT_mg_L,
        "MN_TOT_mg/L": muestra.MN_TOT_mg_L,
        "FE_TOT_mg/L": muestra.FE_TOT_mg_L,
    }])

    prediccion = int(modelo.predict(datos)[0])

    return {
        "prediccion": prediccion,
        "mensaje": MENSAJES.get(prediccion, "Sin mensaje definido para este resultado."),
    }
