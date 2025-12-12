# Etapa 4: Arhitectura Completă a Aplicației SIA bazată pe Rețele Neuronale

### 1. Tabelul Nevoie Reală → Soluție SIA → Modul Software

| **Nevoie reală concretă** | **Cum o rezolvă SIA-ul vostru** | **Modul software responsabil** |
|---------------------------|--------------------------------|--------------------------------|
| Identificarea timpurie a pacienților cu risc ridicat de boală coronariană (CHD) în următorii 10 ani | Analiză predictivă pe baza factorilor clinici  → Acuratețe de predicție > 85% pe setul de testare | Model RN + Data Logging |
| Triajul rapid al pacienților în clinici cardiologice aglomerate | Procesare automată a datelor primare și generare scor de risc în < 500ms per pacient | RN |
| Reducerea diagnosticelor fals-negative pentru a nu omite pacienții critici | Optimizarea pragului de decizie al rețelei pentru a obține un Recall (Sensibilitate) > 90% pentru clasa de risc "1" | RN |

### 2. Contribuția la Setul de Date – MINIM 40% din Totalul Observațiilor Finale

| **Tip contribuție** | **Exemple concrete din inginerie** | **Dovada minimă cerută** |
| **Date sintetice prin metode avansate** | • Simulări FEM/CFD pentru date dinamice proces | Cod implementare metodă + exemple before/after + justificare hiperparametri + validare pe subset real |

### Contribuția originală la setul de date:

**Total observații finale:** [N] (după Etapa 3 + Etapa 4)
**Observații originale:** [M] ([X]%)

**Tipul contribuției:**
[ ] Date generate prin simulare fizică  
[ ] Date achiziționate cu senzori proprii  
[ ] Etichetare/adnotare manuală  
[X] Date sintetice prin metode avansate  

**Descriere Detaliată:**

Pentru generarea datelor sintetice, am utilizat algoritmul Gaussian Mixture Model (GMM), o metodă probabilistică nesupervizată capabilă să modeleze distribuția multivariată complexă a datelor originale. Procesul a început prin consolidarea seturilor de date reale (Framingham și cele 4 seturi UCI Heart Disease) și curățarea preliminară a acestora prin imputarea valorilor lipsă. Modelul GMM a fost antrenat pentru a învăța structura statistică și corelațiile dintre variabilele clinice (precum vârsta, colesterolul, tensiunea arterială), permițând generarea unor noi instanțe care, deși sunt artificiale, respectă fidel distribuția populației reale.

**Locația codului:** `src/data_acquisition/Synthetic_generator.py`
**Locația datelor:** `src/processed/final_dataset_augmented.csv`

### 3. Diagrama State Machine a Întregului Sistem

**Legendă**

Am ales modelarea sistemului sub forma unui State Machine secvențial pentru a garanta integritatea datelor în procesul de Data Augmentation. Deoarece generarea de date sintetice medicale implică riscuri de "halucinație" a valorilor (ex: vârste negative sau tensiuni arteriale imposibile), am definit o stare intermediară critică (Synthetic Generation) separată de starea finală.



Starile principale sunt:
1. [Idle]: Sistemul este gata, configurările sunt citite si se asteaptă încărcarea datelor
2. [`Raw data aggregation`]: Datele din cele 5 seturi sunt încărcate în memorie
3. [`Preprocessed data`]: Datele sunt aranjate si pregătite pentru învățare
4. [`synthetic generation`]: Sunt create date noi, încă incorecte
5. [`Data augmented and validated`]: Datele create anterior sunt corectate
6. [`Final dataset ready`]: Fișierul completat de date este creat

Tranziții critice:

[`Synthetic generation`] -> [`Data augmented and validated`] :  Tranziția dintre generare și starea finală (Data Augmented) este condiționată obligatoriu de procesul de Post-Processing, care acționează ca un filtru de validare biologică. Această arhitectură asigură că nicio dată sintetică nu ajunge în setul final de antrenament fără a fi verificată și corectată, eliminând astfel zgomotul statistic produs de modelul Gaussian Mixture.

### 4. Scheletul Complet al celor 3 Module Cerute la Curs
| **Modul** | **Python (exemple tehnologii)** | **LabVIEW** | **Cerință minimă funcțională (la predare)** |
|-----------|----------------------------------|-------------|----------------------------------------------|
| **1. Data Logging / Acquisition** | `src/data_acquisition/` | LLB cu VI-uri de generare/achiziție | **MUST:** Produce CSV cu datele voastre (inclusiv cele 40% originale). Cod rulează fără erori și generează minimum 100 samples demonstrative. |
| **2. Neural Network Module** | `src/neural_network/model.py` sau folder dedicat | LLB cu VI-uri RN | **MUST:** Modelul RN definit, compilat, poate fi încărcat. **NOT required:** Model antrenat cu performanță bună (poate avea weights random/inițializați). |
| **3. Web Service / UI** | Streamlit | WebVI sau Web Publishing Tool | **MUST:** Primește input de la user și afișează un output. **NOT required:** UI frumos, funcționalități avansate. |

### Detalii per modul:

#### **Modul 1: Data Logging / Acquisition**

**Funcționalități obligatorii:**
- [X] Cod rulează fără erori: `python src/data_acquisition/generate.py` sau echivalent LabVIEW
- [X] Generează CSV în format compatibil cu preprocesarea din Etapa 3
- [X] Include minimum 40% date originale în dataset-ul final
- [X] Documentație în cod: ce date generează, cu ce parametri

#### **Modul 2: Neural Network Module**

**Funcționalități obligatorii:**
- [X] Arhitectură RN definită și compilată fără erori
- [X] Model poate fi salvat și reîncărcat
- [X] Include justificare pentru arhitectura aleasă (în docstring sau README)
- [X] **NU trebuie antrenat** cu performanță bună (weights pot fi random)


#### **Modul 3: Web Service / UI**

**Funcționalități MINIME obligatorii:**
- [X] Propunere Interfață ce primește input de la user (formular, file upload, sau API endpoint)
- [ ] Includeți un screenshot demonstrativ în `docs/screenshots/`
