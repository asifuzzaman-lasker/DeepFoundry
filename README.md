# 🫁 DeepFoundry

## Clinical Imaging AI Pipeline: Design, Training, Evaluation & Inference

DeepFoundry is an **end-to-end Clinical Imaging AI application** that supports the complete lifecycle of medical image classification — from dataset preparation to model design, training, evaluation, and inference.

The project is built with a **research-to-industry mindset**, focusing on modular design, reproducibility, interpretability, and real-world deployment readiness.

---

## 🔍 Overview

DeepFoundry provides a structured, step-by-step workflow for developing deep learning models for **medical image classification**, particularly suited for clinical imaging tasks such as X-ray and CT analysis.

The application emphasizes:
- Clean pipeline orchestration
- Transparent evaluation
- Explainable inference
- Professional, healthcare-oriented UI

---

## 🏗️ System Architecture

Dataset → Preprocessing → Model Design → Training → Evaluation → Inference → Explainability
---

## 🚀 Features

### 📁 Dataset Management
- Load and validate medical image datasets
- Automatic class distribution analysis
- Dataset preview and sampling

### 🧠 Model Design
- Configurable deep learning architectures
- Hyperparameter selection via UI
- Modular model-building pipeline

### 🏋️ Training
- Model training using TensorFlow/Keras
- Real-time training visualization
- Training history tracking

### 📊 Evaluation
- Standard and advanced evaluation metrics
- Confusion matrix and performance plots
- Research-oriented reporting

### 🔬 Inference & Explainability
- Single-image and batch inference
- Class probability outputs
- Grad-CAM–based visual explanations for clinical interpretability

### 🖥️ User Interface
- Fixed pipeline-oriented navigation
- Step-based workflow (Dataset → Model → Training → Inference)
- Clean, clinical-grade Streamlit UI

---

## 🏗️ Project Structure

```text
deepfoundry/
│
├── app.py                      # Main Streamlit application
├── requirements.txt
├── README.md
│
├── deepfoundry/
│   ├── ui/
│   │   ├── style.py             # Custom theme and UI styling
│   │   └── pages/
│   │       ├── dataset_page.py
│   │       ├── model_page.py
│   │       ├── training_page.py
│   │       └── inference_page.py
│   │
│   ├── data/
│   │   └── data_loader.py
│   │
│   ├── models/
│   │   └── model_builder.py
│   │
│   ├── training/
│   │   └── trainer.py
│   │
│   ├── evaluation/
│   │   ├── metrics.py
│   │   └── plotting.py
│   │
│   └── explainability/
│       └── gradcam.py
