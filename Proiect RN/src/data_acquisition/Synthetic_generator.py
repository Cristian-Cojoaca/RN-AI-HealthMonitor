import pandas as pd
import numpy as np
import os
from sklearn.mixture import GaussianMixture
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler

# --- CONFIGURAȚIE ---
# --- CONFIGURAȚIE DINAMICĂ ---

# 1. Aflăm unde se află exact acest script (Synthetic_generator.py) pe disk
script_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Construim calea către folderul 'data' navigând un nivel mai sus (din 'data_acquisition' în 'src')
# Structura: src/data_acquisition/.. -> src/data/raw
RAW_DIR = os.path.join(script_dir, '..', 'data', 'raw')
PROCESSED_DIR = os.path.join(script_dir, '..', 'data', 'processed')

OUTPUT_FILE = os.path.join(PROCESSED_DIR, 'final_dataset_augmented.csv')

# (Opțional) Verificare vizuală pentru debugging
print(f"Calea detectată pentru RAW: {os.path.abspath(RAW_DIR)}")

# Nota: Linia 'df = pd.read_csv(file_path)' din codul tau original este inutilă 
# aici, deoarece funcția load_and_combine() va citi fișierele din nou. 
# O poți șterge.
# Fișierele sursă
FILES = {
    'framingham': 'framingham.csv',
    'cleveland': 'processed.cleveland.data',
    'hungarian': 'processed.hungarian.data',
    'switzerland': 'processed.switzerland.data',
    'va': 'processed.va.data'
}

# Coloanele UCI (fără header în original)
UCI_COLS = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 
            'exang', 'oldpeak', 'slope', 'ca', 'thal', 'num']

def load_and_combine():
    """Încarcă și combină toate seturile de date reale (Framingham + UCI)."""
    print("[1/5] Încărcare date reale...")
    
    # 1. Framingham
    df_main = pd.read_csv(os.path.join(RAW_DIR, FILES['framingham']))
    
    # 2. UCI (cele 4 fișiere)
    uci_dfs = []
    for name in ['cleveland', 'hungarian', 'switzerland', 'va']:
        path = os.path.join(RAW_DIR, FILES[name])
        if os.path.exists(path):
            d = pd.read_csv(path, names=UCI_COLS, na_values='?')
            # Mapează la formatul Framingham
            d = d.rename(columns={
                'sex': 'male', 'chol': 'totChol', 'trestbps': 'sysBP', 
                'thalach': 'heartRate', 'fbs': 'diabetes', 'num': 'TenYearCHD'
            })
            # Binarizare Target
            d['TenYearCHD'] = d['TenYearCHD'].apply(lambda x: 1 if x > 0 else 0)
            uci_dfs.append(d)
    
    df_uci = pd.concat(uci_dfs, ignore_index=True)
    
    # Păstrăm doar coloanele comune + cele importante din Framingham
    common_cols = ['male', 'age', 'education', 'currentSmoker', 'cigsPerDay', 
                   'BPMeds', 'prevalentStroke', 'prevalentHyp', 'diabetes', 
                   'totChol', 'sysBP', 'diaBP', 'BMI', 'heartRate', 
                   'glucose', 'TenYearCHD']
    
    # Adăugăm coloanele lipsă la UCI
    for col in common_cols:
        if col not in df_uci.columns:
            df_uci[col] = np.nan
            
    df_final = pd.concat([df_main, df_uci[common_cols]], ignore_index=True)
    
    # Imputare rapidă pentru a putea antrena generatorul
    imputer = SimpleImputer(strategy='median')
    df_imputed = pd.DataFrame(imputer.fit_transform(df_final), columns=common_cols)
    
    print(f" -> Total date reale: {len(df_imputed)} rânduri")
    return df_imputed

def generate_synthetic_data(df_real, n_samples=3500):
    """
    Generează date sintetice folosind Gaussian Mixture Models.
    Acesta învață distribuția multidimensională a datelor reale.
    """
    print(f"[2/5] Antrenare model generator (GMM) pe {len(df_real)} exemple...")
    
    # Antrenăm GMM
    gmm = GaussianMixture(n_components=10, covariance_type='full', random_state=42)
    gmm.fit(df_real)
    
    print(f"[3/5] Generare {n_samples} pacienți sintetici...")
    data_generated, _ = gmm.sample(n_samples)
    
    # Convertim în DataFrame
    df_gen = pd.DataFrame(data_generated, columns=df_real.columns)
    
    # Adăugăm o coloană de marcaj (0=Real, 1=Sintetic)
    df_gen['is_synthetic'] = 1
    df_real['is_synthetic'] = 0
    
    return df_gen, df_real

def post_process_synthetic(df):
    """Corectează valorile generate (ex: vârsta nu poate fi negativă, sexul e 0 sau 1)."""
    print("[4/5] Post-procesare și curățare date sintetice...")
    
    # 1. Rotunjire și limitare la intervale valide
    integers = ['age', 'cigsPerDay', 'totChol', 'sysBP', 'diaBP', 'heartRate', 'glucose']
    binary = ['male', 'currentSmoker', 'BPMeds', 'prevalentStroke', 'prevalentHyp', 'diabetes', 'TenYearCHD']
    
    for col in df.columns:
        if col in integers:
            df[col] = df[col].round().astype(int)
            df[col] = df[col].clip(lower=0) # Fără valori negative
        elif col in binary:
            # GMM scoate valori gen 0.9 sau 0.1 -> rotunjim la 0 sau 1
            df[col] = df[col].round().clip(0, 1).astype(int)
        elif col == 'BMI':
            df[col] = df[col].round(2).clip(10, 60) # Limite biologice rezonabile
            
    # Corecții logice specifice
    # Dacă nu fumează, cigsPerDay trebuie să fie 0
    df.loc[df['currentSmoker'] == 0, 'cigsPerDay'] = 0
    
    return df

def main():
    # 1. Obținem datele reale complete
    df_real = load_and_combine()
    
    # 2. Generăm datele sintetice (3500 rânduri = ~40% din totalul final de 8660)
    df_syn, df_real = generate_synthetic_data(df_real, n_samples=3500)
    
    # 3. Curățăm datele sintetice
    df_syn = post_process_synthetic(df_syn)
    
    # 4. Combinăm
    df_final = pd.concat([df_real, df_syn], ignore_index=True)
    
    # 5. Salvare
    print(f"[5/5] Salvare dataset final...")
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    df_final.to_csv(OUTPUT_FILE, index=False)
    
    print("-" * 50)
    print(f"REZULTAT FINAL:")
    print(f"Total observații: {len(df_final)}")
    print(f"Originale (Reale): {len(df_real)} ({len(df_real)/len(df_final):.1%})")
    print(f"Sintetice (Generate): {len(df_syn)} ({len(df_syn)/len(df_final):.1%})")
    print(f"Fișier salvat: {OUTPUT_FILE}")
    print("-" * 50)

if __name__ == "__main__":
    main()