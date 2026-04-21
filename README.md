# 🧠 Health Report Interpreter AI

An AI-powered full-stack application that analyzes medical lab reports and generates structured insights, explanations, and risk assessment.

---

## 🚀 Features

### 📄 Report Processing
- Upload PDF or image-based lab reports
- Extract text using OCR and parsing

### 🤖 AI-Powered Analysis
- Convert unstructured report → structured JSON
- Identify:
  - Test names
  - Values
  - Normal ranges
  - Status (Low / Normal / High)

### 🧠 Insights Generation
- Detect abnormal parameters
- Identify patterns (e.g., anemia, inflammation)

### 📊 Explanation Engine
- Human-friendly explanation
- Priority-based insights (most important first)

### ⚠️ Risk Assessment
- Categorizes report into:
  - Low
  - Mild
  - Moderate
  - High

### 🎨 Modern UI
- Angular frontend
- Drag & drop upload
- Clean dashboard with results

---

## Screenshots

### 🖥️ Upload Interface
![1776786100926](image/README/1776786100926.png)

### 📊 Analysis Results
![1776786162382](image/README/1776786162382.png)


## 🏗️ Architecture

Frontend (Angular)
    ↓
FastAPI Backend
    ↓
Services Layer
    ├── LLM (Groq)
    ├── Insights Engine
    ├── Explanation Engine
    └── Risk Engine
    ↓
Utilities
    └── OCR + PDF Parsing

---

## 🛠 Tech Stack

### Backend
- FastAPI
- Groq API (LLM)
- pdfplumber
- pytesseract
- Pillow

### Frontend
- Angular (Standalone Components)
- TypeScript
- CSS (custom UI)

---

## 📂 Project Structure

health-report-interpreter-ai/
│
├── backend/
│   ├── app.py
│   ├── services/
│   ├── utils/
│   └── .env
│
├── frontend-angular/
│   ├── src/app/
│   └── ...
│
└── README.md

---

## ⚙️ Backend Setup

### 1. Create environment

conda create -n health-ai python=3.10
conda activate health-ai

### 2. Install dependencies

pip install -r requirements.txt

### 3. Add environment variables

Create backend/.env and add:

GROQ_API_KEY=your_api_key_here

### 4. Run backend

uvicorn backend.app:app --reload

[Ensure backend is running at: http://127.0.0.1:8000]
---

## ⚙️ Frontend Setup

### 1. Navigate to frontend

cd frontend-angular

### 2. Install dependencies

npm install

### 3. Run Angular app

npx ng serve

[Open frontend in browser: http://localhost:4200]
---

## 📦 How to Use

1. Open frontend in browser  
2. Upload or drag & drop a lab report  
3. Click Analyze Report  
4. View insights, explanation, and risk level  

---

## ⚠️ Disclaimer

This system is for informational purposes only.  
It does NOT provide medical diagnosis or treatment advice.

---

## 👩‍💻 Author

Avani  
AI Engineer | Generative AI | RAG Systems
