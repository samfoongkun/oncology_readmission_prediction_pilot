This repository provides a fully de-identified, synthetic hospital dataset and a reproducible analysis pipeline for demonstrating end-to-end data cleaning, feature engineering, and clinical NLP modeling.

Dataset Description:
basic_info.csv
Contains patient-level basic attributes (age, city type, inpatient type, operation status, etc.)
All fields anonymized; ID numbers are fictional.
DRG.csv
Diagnosis-related group data with cost and outcome indicators
Synthetic structure matching DRG datasets.
face_sheet.csv
Admission and discharge summaries (diagnoses, operation dates, fees)
Placeholder dates (2000/1/1 etc.) used.
note.csv
Narrative clinical notes (doctor’s progress notes, consultations, summaries)
Fully de-identified, human-written synthetic examples; no real patients.

Data Characteristics:
Texts follow realistic EHR syntax and section headers.
Lab values and diagnoses are medically plausible but not factual.
All temporal, institutional, and personal identifiers have been replaced with placeholders (XX, 00001, etc.).

Code Components:
data_cleaning_func.py
Common preprocessing and normalization utilities for tabular & text data.
01_data_exploration.ipynb
Exploratory Data Analysis (EDA): distributions, missing values, correlations, text length stats.
02_build_dataset_andmodel.ipynb
Feature construction and model building (e.g., logistic regression, clinical NER, or classification).

Results and Future Directions:
The tree-based model (XGBoost) maintained good generalization performance while significantly improving the identification of minority cases (readmissions). Logistic regression, meanwhile, retains clear advantages in interpretability and coefficient visualization.

This project establishes a prototype framework that integrates structured and unstructured EHR data. The framework can be further expanded in the following directions:

(1) Multimodal Feature Fusion
Combine structured features (diagnoses, surgeries, laboratory results) with unstructured text (progress notes, discharge summaries).
Use Transformer or TabTransformer models for feature-level fusion to improve both prediction accuracy and interpretability.

(2) Temporal Sequence Modeling
Model the hospitalization process as a time series, leveraging RNNs, LSTMs, or Temporal Fusion Transformers to capture dynamic clinical trajectories such as disease progression or deterioration patterns.

(3) Medical Text Mining (NER & Relation Extraction)
Based on note.csv, train clinical Named Entity Recognition models (for diseases, symptoms, medications, and lab findings)

(4) Causal Inference and Explainable AI
Integrate causal graphs (Causal Graphs) and interpretable AI techniques such as SHAP or LIME to investigate the causal contributions of surgeries, medications, and comorbidities to readmission risk.
