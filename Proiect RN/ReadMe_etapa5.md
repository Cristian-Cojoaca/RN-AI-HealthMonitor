# 📘 README – Etapa 5: Configurarea și Antrenarea Modelului RN

**Disciplina:** Rețele Neuronale  
**Instituție:** POLITEHNICA București – FIIR  
**Student:** [Cojoaca Cristian]  
**Link Repository GitHub:** [URL complet]  
**Data predării:** [Data]

---

Completați **TOATE** punctele următoare:

1. **Antrenare model** definit în Etapa 4 pe setul final de date (≥40% originale)
2. **Minimum 10 epoci**, batch size 8–32
3. **Împărțire stratificată** train/validation/test: 70% / 15% / 15%
4. **Tabel justificare hiperparametri** (vezi secțiunea de mai jos - OBLIGATORIU)
5. **Metrici calculate pe test set:**
   - **Acuratețe ≥ 65%**
   - **F1-score (macro) ≥ 0.60**
6. **Salvare model antrenat** în `models/trained_model.h5` (Keras/TensorFlow) sau `.pt` (PyTorch) sau `.lvmodel` (LabVIEW)
7. **Integrare în UI din Etapa 4:**
   - UI trebuie să încarce modelul ANTRENAT (nu dummy)
   - Inferență REALĂ demonstrată
   - Screenshot în `docs/screenshots/inference_real.png`

   **Hiperparametru** | **Valoare Aleasă** | **Justificare** |
|--------------------|-------------------|-----------------|
| Learning rate | Ex: 0.001 | Valoare standard pentru Adam optimizer, asigură convergență stabilă |
| Batch size | Ex: 32 | Compromis memorie/stabilitate pentru N=[8661] samples |
| Number of epochs | Ex: 50 | Cu early stopping după 10 epoci fără îmbunătățire |
| Optimizer | Ex: Adam | Adaptive learning rate, potrivit pentru RN cu [numărul vostru] straturi |
| Loss function | Ex: Categorical Crossentropy | Clasificare multi-class cu K=[numărul vostru] clase |
| Activation functions | Ex: ReLU (hidden), Softmax (output) | ReLU pentru non-linearitate, Softmax pentru probabilități clase |