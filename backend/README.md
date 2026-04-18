# 🧠 Backend – Health Report Interpreter

This backend service handles file ingestion, text extraction, and AI-based processing of medical reports.

## 🚀 Features (v1)
- Upload PDF and image reports
- Extract text using:
  - pdfplumber (PDF parsing)
  - Tesseract OCR (image processing)
- REST API using FastAPI

## 🚀 Features (v2 – Current)
- Convert extracted text → **structured JSON using LLMs**
- Automatically extract:
  - Test names
  - Values
  - Normal ranges
  - Status (Low / Normal / High)
- Integration with **Groq API (Llama models)** for fast inference
- Return clean, machine-readable structured data from medical reports

## 📂 Endpoints

### GET /
Health check endpoint

### POST /upload
Upload a report file and:
- Extract raw text
- Convert into structured medical data (LLM processed)

## 🛠 Tech Stack
- FastAPI
- pdfplumber
- pytesseract
- Pillow
- Groq API (LLMs)

## 📌 Next Steps
- Add intelligent insight generation layer (pattern detection)
- Provide natural language explanations
- Implement risk scoring (Low / Moderate / High)
- Implement RAG for knowledge grounding

## ⚠️ Disclaimer
This system is for informational purposes only and does not provide medical diagnosis.