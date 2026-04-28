# Water Quality Monitoring System (WQMS)

A full-stack web application for monitoring, analyzing, and predicting water quality using machine learning.

---

## Tech Stack

Frontend
- HTML
- Tailwind CSS
- Vanilla JavaScript

Backend
- FastAPI (Python)

Database
- PostgreSQL (via Supabase)

Machine Learning
- Scikit-learn

---

## Features

- Dark UI with glassmorphism design
- Interactive dashboard for water sample analysis
- Machine learning model to predict water safety (Safe / Unsafe)
- Data entry form to submit new water samples
- Dynamic reports table with suggestions
- Real-time prediction and storage workflow

---

## Machine Learning

- Model: Logistic Regression / Decision Tree
- Input Features:
  - pH
  - Hardness
  - Solids
  - Chloramines
  - Sulfate
  - Conductivity
  - Organic Carbon
  - Trihalomethanes
  - Turbidity

- Output:
  - Prediction: Safe / Unsafe
  - Probability Score

---

## Setup Instructions

### 1. Create Virtual Environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1