import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib 


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


DATA_PATH = os.path.join(SCRIPT_DIR, '..', 'data', 'processed', 'final_dataset_augmented.csv')

MODEL_SAVE_PATH = os.path.join(SCRIPT_DIR, '..', 'models')
os.makedirs(MODEL_SAVE_PATH, exist_ok=True)

def load_and_preprocess():
    print(f"[1/4] Încărcare date din: {os.path.abspath(DATA_PATH)}")
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Lipsă fișier date: {DATA_PATH}")
        
    df = pd.read_csv(DATA_PATH)
    

    X = df.drop(['TenYearCHD', 'is_synthetic'], axis=1)
    y = df['TenYearCHD']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler

def train_neural_network(X_train, y_train):
    print("[2/4] Antrenare Rețea Neuronală (MLP)...")
    
    model = MLPClassifier(
        hidden_layer_sizes=(64, 32, 16), 
        activation='relu',              
        solver='adam',                  
        alpha=0.0001,                    
        batch_size=32,                  
        learning_rate_init=0.001,       
        max_iter=200,                    
        early_stopping=True,             
        random_state=42,
        verbose=True                     
    )
    
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    print("[3/4] Evaluare...")
    y_pred = model.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    print(f"\nACURATEȚE FINALĂ: {acc*100:.2f}%")
    
    print("\nRaport Detaliat:")
    print(classification_report(y_test, y_pred))
    
   
    plt.figure(figsize=(6, 5))
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Matrice de Confuzie (Rețea Neuronală)')
    plt.ylabel('Real')
    plt.xlabel('Predicție')
    plt.show()
    
   
    plt.figure(figsize=(8, 4))
    plt.plot(model.loss_curve_)
    plt.title("Evoluția Erorii în timpul Antrenării")
    plt.xlabel("Iterații")
    plt.ylabel("Loss (Eroare)")
    plt.show()

if __name__ == "__main__":
    
    X_train, X_test, y_train, y_test, _ = load_and_preprocess()

   
    model = train_neural_network(X_train, y_train)

    
    evaluate_model(model, X_test, y_test)

  
    print("[4/4] Salvare Model și Scaler pentru Aplicație...")
    
   
    model_path = os.path.join(MODEL_SAVE_PATH, 'heart_model.pkl')
    joblib.dump(model, model_path)
    
    
    df = pd.read_csv(DATA_PATH)
    X = df.drop(['TenYearCHD', 'is_synthetic'], axis=1)
    scaler = StandardScaler()
    scaler.fit(X) 
    
    scaler_path = os.path.join(MODEL_SAVE_PATH, 'scaler.pkl')
    joblib.dump(scaler, scaler_path)
    
    print(f"Gata! Fișiere salvate în: {MODEL_SAVE_PATH}")
    print("   - heart_model.pkl")
    print("   - scaler.pkl")