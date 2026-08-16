import streamlit as st
import joblib
import pandas as pd

st.markdown(
    "<h1 style='text-align: center; font-size: 32px;'>💧 Sistema de Predicción de Calidad del Agua</h1>", 
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align: center; font-size: 16px; color: #555555;'>Ingrese los parámetros fisicoquímicos para evaluar el semáforo del agua.</p>", 
    unsafe_allow_html=True
)

# Cargamos el modelo entrenado
modelo = joblib.load('modelo_calidad_agua.pkl')

with st.form("form_prediccion"):
    st.subheader("Parámetros de Calidad")
    
    col1, col2 = st.columns(2)
    with col1:
        alc = st.number_input("ALC_mg/L", value=220.0)
        conduct = st.number_input("CONDUCT_mS/cm", value=900.0)
        sdt_m = st.number_input("SDT_M_mg/L", value=600.0)
        fluo = st.number_input("FLUORUROS_mg/L", value=0.9)
        dur = st.number_input("DUR_mg/L", value=210.0)
        coli = st.number_input("COLI_FEC_NMP/100_mL", value=1.1)
        no3 = st.number_input("N_NO3_mg/L", value=4.1)
    with col2:
        as_tot = st.number_input("AS_TOT_mg/L", value=0.015, format="%.4f")
        cd_tot = st.number_input("CD_TOT_mg/L", value=0.003, format="%.4f")
        cr_tot = st.number_input("CR_TOT_mg/L", value=0.005, format="%.4f")
        hg_tot = st.number_input("HG_TOT_mg/L", value=0.0005, format="%.5f")
        pb_tot = st.number_input("PB_TOT_mg/L", value=0.005, format="%.4f")
        mn_tot = st.number_input("MN_TOT_mg/L", value=0.0015, format="%.4f")
        fe_tot = st.number_input("FE_TOT_mg/L", value=0.08, format="%.4f")

    submitted = st.form_submit_button("Obtener Predicción")

if submitted:
    datos = {
        "ALC_mg/L": [alc], "CONDUCT_mS/cm": [conduct], "SDT_M_mg/L": [sdt_m],
        "FLUORUROS_mg/L": [fluo], "DUR_mg/L": [dur], "COLI_FEC_NMP/100_mL": [coli],
        "N_NO3_mg/L": [no3], "AS_TOT_mg/L": [as_tot], "CD_TOT_mg/L": [cd_tot],
        "CR_TOT_mg/L": [cr_tot], "HG_TOT_mg/L": [hg_tot], "PB_TOT_mg/L": [pb_tot],
        "MN_TOT_mg/L": [mn_tot], "FE_TOT_mg/L": [fe_tot]
    }
    df_entrada = pd.DataFrame(datos)
    prediccion = modelo.predict(df_entrada)[0]
    
    # Muestra el resultado traducido según el valor del modelo
    if prediccion == 0:
     st.success("🟢 Óptima: Apta para consumo y riego")
    elif prediccion == 1:
     st.warning("🟡 Precaución: Requiere filtración o tratamiento")
    else:
     st.error("🔴 Crítica: No apta para uso humano ni agrícola")