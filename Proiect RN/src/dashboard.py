import streamlit as st
import pandas as pd
import plotly.express as px
import os
import seaborn as sns
import matplotlib.pyplot as plt


st.set_page_config(page_title="Heart Disease Analysis", layout="wide",)


@st.cache_data
def load_data():
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    file_path = os.path.join(script_dir, 'data', 'processed', 'final_dataset_augmented.csv')
    
    if not os.path.exists(file_path):
        st.error(f"Fișierul nu a fost găsit la: {file_path}. Rulează întâi generatorul de date!")
        return None
    
    df = pd.read_csv(file_path)
    return df


def main():
    st.title("Heart Disease Data Dashboard")
    st.markdown("Analiză comparativă între datele **Reale** și cele **Sintetice (Generate)**.")

    df = load_data()
    if df is None:
        return

    
    st.sidebar.header("Filtre Globale")
    data_type = st.sidebar.radio("Alege tipul de date:", ["Toate", "Doar Reale", "Doar Sintetice"])

    if data_type == "Doar Reale":
        df_view = df[df['is_synthetic'] == 0]
    elif data_type == "Doar Sintetice":
        df_view = df[df['is_synthetic'] == 1]
    else:
        df_view = df

    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Pacienți", len(df_view))
    col2.metric("Vârsta Medie", f"{df_view['age'].mean():.1f} ani")
    col3.metric("Fumători", f"{df_view['currentSmoker'].sum()} ({df_view['currentSmoker'].mean()*100:.1f}%)")
    col4.metric("Risc CHD (10 ani)", f"{df_view['TenYearCHD'].sum()} cazuri")

    st.markdown("---")

    
    tab1, tab2, tab3 = st.tabs(["Distribuții", "Corelații", "Date Brute"])

    with tab1:
        st.subheader("Distribuția Datelor: Real vs Sintetic")
        
        
        col_dist = st.selectbox("Alege variabila de analizat:", 
                                ['age', 'sysBP', 'chol', 'BMI', 'heartRate', 'cigsPerDay'])
        
       
        fig = px.histogram(df, x=col_dist, color="is_synthetic", barmode="overlay",
                           title=f"Distribuția {col_dist} (Real=0 vs Sintetic=1)",
                           opacity=0.7, nbins=30)
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("Observă dacă datele sintetice (1) se suprapun bine peste cele reale (0). Asta indică o generare de calitate.")

    with tab2:
        st.subheader("Matrice de Corelație")
        
        
        corr_cols = ['age', 'sysBP', 'diaBP', 'BMI', 'heartRate', 'glucose', 'totChol', 'TenYearCHD']
        corr = df_view[corr_cols].corr()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
        st.pyplot(fig)

    with tab3:
        st.subheader("Vizualizare Tabelară")
        st.dataframe(df_view.head(100))
        
        
        csv = df_view.to_csv(index=False).encode('utf-8')
        st.download_button(" Descarcă datele filtrate", csv, "date_export.csv", "text/csv")

if __name__ == "__main__":
    main()