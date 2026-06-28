# 🚀 Setup Guide - Health Report Interpreter AI

Complete setup instructions for developers to get the application running locally.

---

## 📋 Prerequisites

- **Python 3.10+** (use 3.11 recommended)
- **Node.js 18+** (LTS recommended)
- **Conda** (Miniconda or Anaconda)
- **Git**

### Check versions:
```bash
python --version
node --version
npm --version
conda --version
```

---

## 🔧 Backend Setup

### 1. Create & Activate Conda Environment

```bash
cd "/Users/avanivaish/Desktop/Avani's Projects/health-report-interpreter-ai"

# Create environment
conda create -n health-ai python=3.11 -y

# Activate environment
conda activate health-ai
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

**What's installed:**
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `pdfplumber` & `pytesseract` - PDF/image processing
- `openai` - LLM API client
- `pymongo` - MongoDB driver (optional)
- `reportlab` - PDF generation
- `python-dotenv` - Environment variables

### 3. Setup Environment Variables

Copy the provided `.env.example` template to create your `.env` file in the backend:

```bash
cp .env.example backend/.env
```

**Required variables in `.env`:**
```
GROQ_API_KEY=your_groq_api_key
OPENAI_API_KEY=your_openai_api_key
MONGO_URI=mongodb://localhost:27017/
GOOGLE_API_KEY=your_google_api_key
```

### 4. Start Backend Server

```bash
source ~/miniconda3/etc/profile.d/conda.sh
conda activate health-ai

cd "/Users/avanivaish/Desktop/Avani's Projects/health-report-interpreter-ai"

python -m uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
INFO:     Will watch for changes in these directories: ['/path/to/project']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

**Verify backend is running:**
```bash
curl http://localhost:8000/
# Response: {"message": "Health Report AI Backend Running 🚀"}
```

---

## 🎨 Frontend Setup

### 1. Navigate to Frontend Directory

```bash
cd "/Users/avanivaish/Desktop/Avani's Projects/health-report-interpreter-ai/frontend-angular"
```

### 2. Install Node Dependencies

```bash
npm install
```

This installs:
- Angular 21
- TypeScript
- Supporting libraries

### 3. Start Frontend Development Server

```bash
npm start
```

**Alternative command (if needed):**
```bash
ng serve --host 0.0.0.0 --port 4200
```

**Expected output:**
```
✔ Building...
Application bundle generation complete. [2.5 seconds]
➜  Local:   http://localhost:4200/
➜  Network: http://192.168.0.105:4200/
```

---

## ✅ Verify Full Setup

Once both backend and frontend are running:

### 1. Open Frontend
- **Browser:** http://localhost:4200
- Should see upload interface with "🧠 Health Report AI" heading

### 2. Test Upload
1. Click "Browse File" or drag a PDF/image report
2. Click "Analyze Report"
3. Wait for processing (should complete in 5-10 seconds)
4. View results: Insights, Explanation, Risk Level

### 3. Test History Features
- View recent reports in the list below upload area
- **⚖️** Click to select 2 reports for comparison
- **💾** Export as JSON
- **📄** Export as PDF
- **🗑️** Delete report

### 4. Test Search & Filter
- Type in search box to filter by filename
- Use dropdown to filter by risk level (Low/Mild/Moderate/High)

### 5. Test Backend API Directly

```bash
# Get all reports
curl http://localhost:8000/history

# Get specific report
curl http://localhost:8000/report/0

# Export as JSON
curl http://localhost:8000/report/0/export?format=json

# Export as PDF
curl http://localhost:8000/report/0/export?format=pdf > report.pdf
```

---

## 📁 Project Structure

```
health-report-interpreter-ai/
├── backend/
│   ├── app.py                    # FastAPI main app
│   ├── config.py                 # Configuration
│   ├── .env                       # Environment variables (git ignored)
│   ├── services/
│   │   ├── llm_service.py        # Groq LLM integration
│   │   ├── insight_service.py    # Insight generation
│   │   ├── explanation_service.py # Explanation engine
│   │   ├── risk_service.py       # Risk assessment
│   │   └── history_service.py    # Report history (MongoDB/JSON)
│   ├── utils/
│   │   └── parser.py             # PDF/image text extraction
│   └── data/
│       └── history.json          # Local history storage (git ignored)
│
├── frontend-angular/
│   ├── src/
│   │   ├── index.html
│   │   ├── main.ts
│   │   ├── styles.css
│   │   └── app/
│   │       ├── app.ts
│   │       └── upload/
│   │           ├── upload.ts     # Main component (history, compare, export)
│   │           ├── upload.html   # Template with interactive UI
│   │           └── upload.css    # Styling with tooltips
│   ├── package.json
│   ├── angular.json
│   └── tsconfig.json
│
├── requirements.txt              # Python dependencies
├── .gitignore                    # Git ignore rules
├── README.md                     # Project overview
├── SETUP.md                      # This file
└── env                           # Example .env (copy to backend/)
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/upload` | Upload & analyze report |
| GET | `/history?search=X&risk_level=Y` | Get reports (with filters) |
| GET | `/report/{id}` | Get specific report |
| DELETE | `/report/{id}` | Delete report |
| GET | `/report/{id}/export?format=json\|pdf` | Export report |

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is already in use
lsof -i :8000

# Kill existing process
kill -9 <PID>

# Restart backend
python -m uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

### Frontend build errors
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
npm start
```

### Python import errors
```bash
# Verify environment is activated
conda activate health-ai

# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### PDF export fails
```bash
# Ensure reportlab is installed
pip install reportlab --upgrade
```

### History not persisting
- Check if `backend/data/` directory exists
- If using MongoDB, verify `MONGO_URI` in `.env`
- Default fallback: `backend/data/history.json`

---

## 📝 Development Workflow

### Making changes

**Backend:**
1. Edit files in `backend/`
2. Backend auto-reloads with `--reload` flag
3. Refresh browser to see changes

**Frontend:**
1. Edit files in `frontend-angular/src/`
2. Angular auto-rebuilds and refreshes
3. Changes appear instantly in browser

### Adding new dependencies

**Python:**
```bash
pip install <package>
pip freeze | grep <package> >> requirements.txt
```

**Node:**
```bash
npm install <package>
npm list <package>
```

---

## 🚢 Production Deployment

For production deployment:

1. **Build frontend:**
   ```bash
   npm run build
   ```
   Output: `frontend-angular/dist/frontend-angular/`

2. **Run backend without reload:**
   ```bash
   python -m uvicorn backend.app:app --host 0.0.0.0 --port 8000 --workers 4
   ```

3. **Serve with Docker (optional):**
   - Backend: Dockerfile for FastAPI
   - Frontend: Serve dist/ with Nginx

---

## ✨ Features Implemented

- ✅ PDF & image report upload
- ✅ AI-powered structured data extraction (Groq LLM)
- ✅ Insight generation & pattern detection
- ✅ Natural language explanations
- ✅ Risk level assessment
- ✅ Report history with MongoDB/JSON storage
- ✅ View, delete, and compare reports
- ✅ Search by filename & filter by risk level
- ✅ Export as JSON or PDF
- ✅ Tooltips for better UX
- ✅ Proper text wrapping in PDFs

---

## 📞 Support

For issues or questions, check:
- Backend logs: Terminal running `uvicorn`
- Frontend logs: Browser console (F12)
- Network tab: Check API requests/responses

---

**Last updated:** 2026-06-28  
**Developed by:** Avani  
**Tech Stack:** FastAPI + Angular + Groq LLM
