from fastapi import FastAPI, UploadFile, File

from backend.services.llm_service import extract_structured_data
from backend.services.insight_service import generate_insights
from backend.services.explanation_service import generate_explanation
from backend.services.risk_service import generate_risk
from backend.utils.parser import extract_text

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Health Report AI Backend Running 🚀"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    text = await extract_text(file)

    structured = extract_structured_data(text[:3000])
    insights = generate_insights(structured)
    explanation = generate_explanation(structured, insights)
    risk = generate_risk(structured)

    return {
        "filename": file.filename,
        "structured_data": structured,
        "insights": insights,
        "explanation": explanation,
        "risk_level": risk
    }