import os
import pandas as pd
import json
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


DATA_PATH = os.path.join(SCRIPT_DIR, '..', 'data', 'processed', 'final_dataset_augmented.csv')
MODEL_DIR = os.path.join(SCRIPT_DIR, '..', 'models')
RESULTS_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'results') 


os.makedirs(RESULTS_DIR, exist_ok=True)

def main():
    print("Începere evaluare pentru generare JSON...")
    
    
    if not os.path.exists(DATA_PATH):
        print(f"Eroare: Nu găsesc datele la {DATA_PATH}")
        return

    df = pd.read_csv(DATA_PATH)
    X = df.drop(['TenYearCHD', 'is_synthetic'], axis=1)
    y = df['TenYearCHD']

    
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    
    model_path = os.path.join(MODEL_DIR, 'heart_model.pkl')
    scaler_path = os.path.join(MODEL_DIR, 'scaler.pkl')

    if not os.path.exists(model_path):
        print("Eroare: Nu găsesc modelul salvat. Rulează antrenarea întâi!")
        return

    print("   -> Încărcare model și scaler...")
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)

    
    X_test_scaled = scaler.transform(X_test)
    y_pred = model.predict(X_test_scaled)

    
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='macro')
    prec = precision_score(y_test, y_pred, average='macro')
    rec = recall_score(y_test, y_pred, average='macro')

    metrics = {
        "test_accuracy": round(acc, 4),
        "test_f1_macro": round(f1, 4),
        "test_precision_macro": round(prec, 4),
        "test_recall_macro": round(rec, 4)
    }

   
    output_file = os.path.join(RESULTS_DIR, 'test_metrics.json')
    with open(output_file, 'w') as f:
        json.dump(metrics, f, indent=4)

    print(f"\n SUCCES! Fișierul a fost generat: {output_file}")
    print("Conținut:")
    print(json.dumps(metrics, indent=4))

if __name__ == "__main__":
    main()