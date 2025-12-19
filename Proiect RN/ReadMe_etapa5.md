# 📘 Raport Etapa 5: Configurarea și Antrenarea Modelului RN

**Disciplina:** Rețele Neuronale  
**Instituție:** POLITEHNICA București – FIIR  
**Student:** [Numele Tău]  
**Data predării:** 19 Decembrie 2025

---

## 1. Verificare Prerechizite Etapa 4
- [x] **State Machine** definit și documentat în `docs/state_machine.drawio`.
- [x] **Contribuție date ≥40%**: Dataset-ul final conține date reale (Framingham) și date sintetice (GMM), asigurând volumul necesar.
- [x] **Module funcționale**: Data Acquisition, Neural Network și UI sunt integrate.

---

## 2. Configurarea Antrenării (Nivel 1)

Am utilizat o arhitectură de tip **Multi-Layer Perceptron (MLP)** antrenată pe setul de date combinat.

### Tabel Hiperparametri și Justificări
| **Hiperparametru** | **Valoare Aleasă** | **Justificare** |
|--------------------|-------------------|-----------------|
| Learning rate | 0.001 | Valoare standard pentru Adam, asigură o convergență stabilă fără oscilații mari. |
| Batch size | 32 | Echilibru optim între stabilitatea gradientului și utilizarea memoriei pentru ~7700 de probe. |
| Number of epochs | 50 | Suficiente iterații pentru ca modelul să conveargă, utilizând Early Stopping. |
| Optimizer | Adam | Algoritm adaptiv, foarte robust pentru date tabulare clinice. |
| Loss function | Binary Crossentropy | Obligatorie pentru clasificarea binară a riscului cardiovascular (0/1). |
| Activation functions| ReLU (straturi ascunse) | Previne problema "vanishing gradient" și oferă non-linearitate. |

**Justificare Batch Size:**
Am ales `batch_size=32` pentru a asigura un gradient suficient de stabil. Un batch prea mic ar fi introdus prea mult zgomot, în timp ce unul prea mare ar fi încetinit învățarea pe un dataset de această dimensiune.

---

## 3. Metrici de Performanță (Nivel 1 & 2)

Antrenarea a fost efectuată cu o împărțire stratificată de **80% Train / 10% Val / 10% Test**.

- **Acuratețe pe Test Set:** ~85% (Prag minim: 65%)
- **F1-Score (Macro):** ~0.76 (Prag minim: 0.60)

---

## 4. Analiză Erori în Context Medical (Nivel 2)

1. **Pe ce clase greșește modelul?**
Modelul are dificultăți uneori în a identifica pacienții tineri care fumează dar au restul indicatorilor normali, clasificându-i eronat ca "fără risc" (clasa 0).

2. **Cauze ale erorilor:**
Erorile sunt cauzate de lipsa unor factori de stil de viață suplimentari în datele de intrare (ex. stres, sedentarism) care ar putea rafina predicția.

3. **Implicații Medicale:**
False Negatives (bolnav considerat sănătos) sunt **critice** în medicină. False Positives sunt mai puțin grave, ducând doar la investigații suplimentare.

4. **Măsuri corective:**
- Colectarea de date suplimentare pentru grupuri de vârstă sub-reprezentate.
- Implementarea unei penalizări mai mari pentru erorile de tip False Negative în funcția de cost.

---

## 5. Verificare Consistență cu State Machine

| **Stare (Etapa 4)** | **Implementare (Etapa 5)** |
|---------------------|----------------------------|
| `ACQUIRE_DATA`      | Citire input din formularul Streamlit. |
| `PREPROCESS`        | Aplicare `scaler.pkl` pe datele introduse. |
| `RN_INFERENCE`      | Execuție `model.predict()` cu rețeaua antrenată. |
| `ALERT`             | Afișare verdict de risc (Scăzut / Ridicat) în UI. |

---