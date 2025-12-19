import streamlit as st
import joblib
import numpy as np
import os
import pandas as pd


st.set_page_config(page_title="Cardio Predictor AI", layout="centered")


@st.cache_resource
def load_resources():
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(script_dir,'models', 'heart_model.pkl')
    scaler_path = os.path.join(script_dir,'models', 'scaler.pkl')
    
    try:
        
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        return model, scaler
    except FileNotFoundError:
        st.error("Nu am găsit fișierele .pkl! Rulează mai întâi scriptul de antrenare (Pasul 1).")
        return None, None


model, scaler = load_resources()

def main():
    st.title("Predicție Risc Cardiovascular")
    st.markdown("Introduceți datele pacientului pentru a obține o estimare a riscului pe 10 ani.")

    if model is None:
        return 

   
    st.subheader("Date Pacient")
    
    col1, col2 = st.columns(2)
    
    with col1:
        sex = st.selectbox("Sex", ["Masculin", "Feminin"])
        age = st.number_input("Vârsta", 20, 90, 45)
        education = st.selectbox("Educație", ["Primară/Gimnaziu", "Liceu/Bac", "Facultate", "Post-universitar"])
        is_smoker = st.radio("Fumător curent?", ["Nu", "Da"])
        cigs = 0
        if is_smoker == "Da":
            cigs = st.slider("Țigări pe zi", 1, 60, 10)
        
        bp_meds = st.radio("Ia tratament pt Tensiune?", ["Nu", "Da"])
        prev_stroke = st.checkbox("Istoric de AVC?")
        prev_hyp = st.checkbox("Istoric de Hipertensiune?")

    with col2:
        diabetes = st.radio("Diabet?", ["Nu", "Da"])
        tot_chol = st.number_input("Colesterol Total (mg/dL)", 100, 600, 200)
        sys_bp = st.number_input("Tensiune Sistolică (mm Hg)", 80, 250, 120)
        dia_bp = st.number_input("Tensiune Diastolică (mm Hg)", 40, 160, 80)
        bmi = st.number_input("BMI", 10.0, 50.0, 25.0)
        heart_rate = st.number_input("Puls (BPM)", 40, 150, 75)
        glucose = st.number_input("Glicemie (mg/dL)", 40, 400, 85)

   
    if st.button("Analizează Risc", type="primary"):
        
        sex_val = 1 if sex == "Masculin" else 0
        edu_map = {"Primară/Gimnaziu": 1, "Liceu/Bac": 2, "Facultate": 3, "Post-universitar": 4}
        edu_val = edu_map[education]
        smoker_val = 1 if is_smoker == "Da" else 0
        bp_meds_val = 1 if bp_meds == "Da" else 0
        stroke_val = 1 if prev_stroke else 0
        hyp_val = 1 if prev_hyp else 0
        diab_val = 1 if diabetes == "Da" else 0

       
        input_data = [sex_val, age, edu_val, smoker_val, cigs, bp_meds_val, 
                      stroke_val, hyp_val, diab_val, tot_chol, sys_bp, dia_bp, 
                      bmi, heart_rate, glucose]
        
        
        input_scaled = scaler.transform([input_data])
        
       
        prediction = model.predict(input_scaled)[0]
        probability = model.predict_proba(input_scaled)[0][1] * 100

        st.divider()
        if prediction == 1:
            st.error(f"RISC DETECTAT! Probabilitate: {probability:.1f}%")
            st.warning("Recomandare: Consultați un medic cardiolog.")
        else:
            st.success(f"RISC SCĂZUT. Probabilitate: {probability:.1f}%")
            st.info("Recomandare: Mențineți stilul de viață sănătos.")

if __name__ == "__main__":
    main()