# 🎙️ AcousticSpace-RIR-Deepfake-Detection

> AI-powered Deepfake Audio Detection using **Room Impulse Response (RIR)**, **Audio Signal Processing**, and **Deep Learning**.

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![PyTorch](https://img.shields.io/badge/PyTorch-DeepLearning-red?logo=pytorch)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📌 Overview

**AcousticSpace-RIR-Deepfake-Detection** is a collaborative deep learning project that detects AI-generated speech by analyzing **Room Impulse Response (RIR)** and acoustic features extracted from audio signals.

The system combines audio preprocessing, feature engineering, transformer-based classification, REST APIs, and a modern web dashboard into a complete end-to-end deepfake detection pipeline.

---

## ✨ Key Features

- 🎧 Audio preprocessing using Librosa
- 🔊 Room Impulse Response (RIR) feature extraction
- 🤖 Deepfake audio classification using AST
- 📊 Model evaluation & performance analysis
- ⚡ FastAPI backend for inference
- 🎨 React dashboard for visualization
- 🐳 Docker-ready deployment
- 🔄 Modular architecture for easy scalability

---

## 🏗️ Project Architecture

```
Audio Input
      │
      ▼
Preprocessing
      │
      ▼
Feature Extraction (RIR)
      │
      ▼
Deep Learning Model
      │
      ▼
FastAPI Backend
      │
      ▼
React Dashboard
```

---

## 🛠️ Technology Stack

| Category | Technologies |
|----------|--------------|
| Language | Python |
| Audio Processing | Librosa |
| Deep Learning | PyTorch, Hugging Face |
| Backend | FastAPI |
| Frontend | React.js |
| Version Control | Git & GitHub |
| Deployment | Docker |

---

## 📂 Repository Structure

```
AcousticSpace-RIR-Deepfake-Detection
│
├── dataset/
├── src/
├── backend/
├── frontend/
├── notebooks/
├── reports/
├── README.md
├── requirements.txt
└── LICENSE
```

---

## 🚀 Getting Started

### Clone Repository

```bash
git clone https://github.com/harsh5145sharma-ux/AcousticSpace-RIR-Deepfake-Detection.git
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Start Backend

```bash
uvicorn main:app --reload
```

### Start Frontend

```bash
npm install
npm start
```

---

# 👥 Team Contributions

| Member | Role | Responsibilities |
|--------|------|------------------|
| **Member 1** | ML / Audio Pipeline Lead | Audio preprocessing, RIR feature extraction, dataset preparation, feature engineering |
| **Member 2** | ML Model Engineer | AST model training, hyperparameter tuning, evaluation, optimization |
| **Member 3** | Backend Engineer | FastAPI development, authentication, database, model serving |
| **Member 4** | Frontend Engineer | React dashboard, waveform visualization, API integration, UI/UX |

The division of responsibilities, deliverables, and branch strategy follows the team's project plan. :contentReference[oaicite:0]{index=0}

---

## 🌿 Git Workflow

```
main
 │
develop
 ├── feature/audio-pipeline
 ├── feature/ast-model
 ├── feature/backend-api
 └── feature/frontend-dashboard
```

---

## 📈 Future Enhancements

- Real-time inference
- Explainable AI visualizations
- Cloud deployment
- Mobile application
- Multi-language support

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push your branch
5. Open a Pull Request

---

## 📜 License

This project is licensed under the **MIT License**.

---

## ⭐ Acknowledgements

- ASVspoof Dataset
- Librosa
- Hugging Face
- PyTorch
- FastAPI
- React

---

<div align="center">

**Developed as a collaborative academic project on AI-powered Deepfake Audio Detection.**

⭐ If you found this project useful, consider giving it a star.

</div>
