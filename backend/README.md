# 🧠 Backend – Health Report Interpreter

This backend service handles file ingestion, text extraction, and AI-based processing of medical reports.

## 🚀 Features (v1)
- Upload PDF and image reports
- Extract text using:
  - pdfplumber (PDF parsing)
  - Tesseract OCR (image processing)
- REST API using FastAPI

## 📂 Endpoints

### GET /
Health check endpoint

### POST /upload
Upload a report file and extract raw text

## 🛠 Tech Stack
- FastAPI
- pdfplumber
- pytesseract
- Pillow

## 📌 Next Steps
- Convert extracted text → structured JSON (LLM)
- Add medical insights and explanations
- Implement RAG for knowledge grounding

## ⚠️ Disclaimer
This system is for informational purposes only and does not provide medical diagnosis.