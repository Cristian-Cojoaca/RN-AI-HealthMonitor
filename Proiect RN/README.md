**Disciplina:** Retele Neuronale
**Instituție:** Politehnica București - FIIR
**Student:** Cojoacă Cristian Andrei Ionuț
**Data:** 21.11.2025

## Introducere

Acest document descrie activitățile realizate în **Etapa 3**, în care se analizează și se preprocesează setul de date necesar proiectului „Rețele Neuronale". Scopul etapei este pregătirea corectă a datelor pentru instruirea modelului RN, respectând bunele practici privind calitatea, consistența și reproductibilitatea datelor.

## 1. Structura Repository-ului Github



## 2. Descrierea Setului de Date

### 2.1 Sursa datelor

* **Origine:** dataset public: Framingham heart study dataset, UCI machine learning dataset - Heart Disease
* **Modul de achiziție:** Fisier extern
* **Perioada/ condițiile colectării:**

### 2.2 Caracteristicile dataset-ului

* **Număr total de observații:**[4240]
* **Număr de caracteristici (features):**[16]
* **Tipuri de date:** Numerice, Categoriale
* **Format fișiere:** CSV

### 2.3 Descrierea fiecărei caracteristici

| **Caracteristică** | **Tip** | **Unitate** | **Descriere** | **Domeniu valori** |
| Sex | Categorial (Binar) | 1 = Bărbat, 0 = Femeie | {0, 1} |
| Vârstă | Numeric | Vârsta pacientului | 32 – 70 ani |
| Educație | Categorial | Nivelul de studii | {1, 2, 3, 4} |
| Fumător curent | Categorial (Binar) | Dacă pacientul fumează | {0, 1} |
| Țigări pe zi`| Numeric | Numărul mediu de țigări | 0 – 70 |
| Med. Tensiune  | Categorial (Binar) | Tratament hipertensiune | {0, 1}, NA |
| AVC Anterior | Categorial (Binar) | Istoric de accident vascular | {0, 1} |
| Hipertensiune | Categorial (Binar) | Istoric hipertensiune | {0, 1} |
| Diabet | Categorial (Binar) | Diagnostic diabet | {0, 1} |
| Colesterol Total | Numeric | Nivel colesterol (mg/dL) | 107 – 696 |
| Tensiune Sistolică | Numeric | mmHg | 83.5 – 295 |
| Tensiune Diastolică | Numeric | mmHg | 48 – 142.5 |
| BMI | Numeric | Indice masă corporală | 15.54 – 56.8 |
| Puls | Numeric | Bătăi pe minut | 44 – 143 |
| Glucoză | Numeric | Nivelul glicemiei (mg/dL) | 40 – 394 |
| Țintă (Target) | Categorial (Binar) | Risc boală coronariană (10 ani) | {0, 1} |

## 3. Analiza Exploratorie a Datelor (EDA) - Sintetic

### 3.1 Statistici descriptive aplicate

* **Medie, mediană, deviație standard**
Vârsta: medie- 49.58, deviație standard- ~8.57, min- 32, max- 70
Țigări pe zi: medie- 9.01, deviațtie standard- ~11.92, min- 0, max- 70
Colesterol total: medie- 236.70, deviație standard- ~44.59, min- 107, max- 696
Tensiune sistolică: medie- 132.35, deviație standard-  ~22.03, min- 83.5, max-295
Tensiune diastolică: medie-82.90, deviație standard- ~11.91, min- 48, max- 142.5
BMI: medie- 25.80, deviație standard- ~4.08, min- 15.54, max-56.8
Puls: medie- 75.88, deviație standard- ~12.03,, min- 44, max-143
Glucoză: medie- 81.96, deviație standard- ~23.95,, min- 40, max-394
 **Min-max și quartiile**
* **Distribuții pe caracteristi**(histograme)
* **Identificarea outlierilor** (IQR / percentile)
avem un outlier in cadrul glucozei, unde valoarea maxima este de 394, cu mult mai mult de valoarea medie de 44.59

### 3.2 Analiza calității datelor

* **Detectarea valorilor lipsă** (%pe coloană)
Coloanele in care s-au gasit valori lipsa sunt: glucoza, med. tensiune, colesterol, BMI, tigari pe zi
* **Detectarea valorilor inconsistente sau eronate**
* **Identificarea caracteristicilor redundante sau puternic corelate**

### 3.3 Probleme identificate

 **Valori lipsa:** Aproximativ 10-15% din randuri au cel putin o valoare lipsa
 **Dezechilibru de clasa:** Variabila tinta are o proportie de 85% clasa 0(fara risc) si 15% clasa 1(cu risc), ceea ce poate afecta antrenarea retelei neuronale
 **Outlieri:** Valori extreme la tensiunea sistolica(>200) si glucoza(>300) care pot fi erori de masurare sau cazuri medicale extreme


## 4. Preprocesarea Datelor

### 4.1 Curatarea datelor

* **Eliminare** S-au eliminat randurile care aveau mai mult de 2 valori lipsa
* **Imputare:**
    * Pentru glucoza si BMI: s-a folosit **mediana**
    * Pentru Tigari pe zi: s-a folosit **modul** sau 0 daca Fumator curent este 0

### 4.2 Transformarea caracteristicilor

* **Normalizare:** Aplicata pe coloanele numerice (Varsta, colesterol, etc.) folosind Min-max
* **Encoding:** Variabilele binare(Sex, Fumator curent) sunt deja in format 0/1

### 4.3 Structurarea seturilor de date

**Impartire realizata:**
* **80%** - Set de Antrenare
* **10%** - Set de Validare
* **10%** - Set de Testare

**Principii respectate:**
* S-a folosit **Stratified Shuffle Split** pentru a mentine proportia clasei tinta in toate cele 3 seturi

### 4.4 Salvarea rezultatelor preprocesării

* Date preprocesate în `data/processed/`
* Seturi train/val/test în foldere dedicate


