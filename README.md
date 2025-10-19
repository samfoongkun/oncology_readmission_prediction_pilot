# Oncology Readmission Prediction Pilot  
**Predicting unplanned readmissions in oncology inpatients using structured and text-based EHR data**

---

## Clinical Goal

Unplanned readmission within 30 days after discharge is a critical quality indicator in oncology care.  
This project aims to **predict unplanned readmission events among hospitalized cancer patients**  
using structured Electronic Health Records (EHR) and prototype-level clinical text data.

**Target population:**  
Adult cancer inpatients (ICD-10: `C11`, `C16`, `C18`, `C20`, `C22`, `C23`, `C24`, `C25`, `C34`, `C50`, `C56`, `C61`, `C64`, `C67`, `C71`, `C79`, etc.)  
across multiple tumor types, surgeries, and adjuvant treatment conditions.

**Clinical motivation:**  
- Reduce preventable readmissions and improve continuity of oncology care.  
- Support hospital quality monitoring and risk-adjusted benchmarking.  
- Provide explainable and reproducible foundations for EHR-based predictive modeling.

---

## Data Source & Composition

**Data origin:**  
Fully de-identified EHR records were extracted for internal model development.  
Sample Size: N = 137243 visits (cancer patient within 202401-202506 timeframe)

All data in this repository are synthetic and fully de-identified. No personally identifiable information, timestamps, or hospital identifiers are included. This dataset structure mimics real EHRs solely for research reproducibility.

| File | Description | Notes |
|------|--------------|-------|
| `basic_info.csv` | Patient demographics & admission metadata | Includes gender, age, occupation, region, admission/discharge date |
| `face_sheet.csv` | Diagnosis, surgery, and procedure summary  | Contains ICD-10 and ICD-9-CM codes, surgery types, operation dates |
| `DRG.csv` | DRG-level structured indicators  | Includes comorbidity flags and encoded treatment-related variables |
| `note.csv` | Textual clinical notes (de-identified)  | Includes progress notes, pre-op discussions, and discharge summaries |


---

## Feature Engineering

Feature extraction integrates **clinical reasoning and domain knowledge** to enhance interpretability.

### Structured Features
- **Demographics:** `Gender`, `Age`, `In-city`, `Occupation`
- **Hospitalization:** `Length of stay`, `Fee`, `Visit type`
- **Cancer Type:** ICD-10 codes grouped by organ system  
- **Surgery-related:** `Is_surgery`, `Class 4 surgery`, `Surgery complications`
- **Treatment-related:** `RT under 96h`, `RT over 96h`, `ECMO`, `CRRT`
- **Pre-discharge markers (72h):** `Ascites`, `Fever`, `Positive bacteria`

### Derived Clinical Indices
- **Comorbidity index (CMI weight rignt WR)** based on `DRG.csv`
- **Procedure severity score** from cumulative operation classes
- **Unplanned discharge flag** to link readmission probability

### Text Feature Prototypes
- Token-level extraction from `note.csv` using regular expression to identify mentions of  
  *“infection”, “re-surgery”, “fever”*  
  (used in pilot NER experiments).

---

## Modeling Pipeline

| Model | Description | Key Parameters |
|--------|--------------|----------------|
| **Logistic Regression (baseline)** | High interpretability, probability-calibrated | `penalty='l2'`, `class_weight='balanced'`, `solver='liblinear'` |
| **XGBoost (tree-based)** | Nonlinear learner with strong imbalance handling | `scale_pos_weight = neg/pos`, `max_depth=4`, temperature scaling applied |

- Data split: **80% train / 20% test**
- Validation: Stratified holdout (temporal leakage prevented)
- Calibration: Post-hoc **temperature scaling** for probabilistic outputs

---

## Evaluation Metrics

Beyond standard discrimination, multiple complementary metrics were used to capture clinical relevance.

| Category | Metric | Purpose |
|-----------|---------|----------|
| **Discrimination** | AUC-ROC, AUPRC | Overall model separability |
| **Sensitivity–Specificity** | Recall, Precision | Evaluate ability to detect true readmissions |
| **Calibration** | Brier Score | Assess reliability of probability outputs |
| **Operational** | Top-k Recall / Precision | Simulate screening workload–benefit tradeoff |

Example results (synthetic dataset):

| Model | Recall@0.05 | Precision@0.05 | AUROC | Brier |
|--------|-------------|----------------|--------|--------|
| Logistic Regression | 0.40 | 0.034 | 0.78 | 0.182 |
| XGBoost | 0.47 | 0.039 | 0.83 | 0.165 |

![alt text](image.png)

**Interpretation:**  
Tree-based XGBoost improves minority-class recall while maintaining reasonable generalization;  
Logistic regression retains interpretability and coefficient transparency.

---

## Key Findings

- **Class imbalance (readmission ~0.4%)** addressed via cost-sensitive learning (`class_weight` / `scale_pos_weight`).  
- **Tree models** better capture nonlinear interactions between surgery, infection, and readmission risk.  
- **Calibration** improved after temperature scaling, yielding more trustworthy probability estimates.  
- **Feature importance** highlights post-operative infection, RT, ECMO, CRRT as top predictors.

---

## Future Research Directions

1. **Multimodal Feature Fusion**  
   Combine structured features with clinical text embeddings (Transformer / TabTransformer).

2. **Temporal Modeling**  
   Model hospitalization as a time series (Patient × Time × Indicators)  
   using RNN / Temporal Fusion Transformer to learn disease progression dynamics.

3. **Clinical Text Mining (NER & Relation Extraction)**  
   Train domain-specific NER models on `note.csv` to extract entities  
   such as *diagnosis, treatment, and complications* for graph-based representation.

4. **Causal Inference & Explainability**  
   Use SHAP / LIME and Causal Graphs to analyze causal contribution  
   of surgery type, comorbidities, and interventions to readmission risk.

5. **Federated Learning & External Validation**  
   Collaborate across institutions using **privacy-preserving federated training**  
   to enhance model generalization and fairness.

---

## Repository Structure

    oncology_readmission_prediction_pilot/
    │
    ├── data/
    │   ├── basic_info.csv
    │   ├── DRG.csv
    │   ├── face_sheet.csv
    │   ├── note.csv
    │   └── data_readme.md    
    │
    ├── notebooks/
    │   ├── 01_data_exploration.ipynb
    │   └── 02_build_dataset_andmodel.ipynb      # dataset construction & model training
    │
    ├── src/
    │   └── data_cleaning_func.py                # data preprocessing and feature extraction
    │
    └── README.md
---

## Environment

| Library | Version |
|----------|----------|
| Python | 3.10+ |
| pandas | 2.1 |
| numpy | 1.26 |
| scikit-learn | 1.5 |
| xgboost | 2.0 |
| matplotlib | visualization |

### This pilot validates the feasibility of EHR-based oncology readmission prediction and establishes a modular, reproducible foundation for future research in multimodal, explainable, and privacy-preserving medical AI.
