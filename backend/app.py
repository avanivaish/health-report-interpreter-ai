from fastapi import FastAPI, UploadFile, File
import pdfplumber
import pytesseract
from PIL import Image
import io

# NEW IMPORTS
from openai import OpenAI
from dotenv import load_dotenv
import os
from pathlib import Path

import json
import re

# ✅ Robust .env loading
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

#debug
print("ENV PATH:", BASE_DIR / ".env")
#print("KEY:", os.getenv("GROQ_API_KEY"))

# 🔐 API key handling
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found. Check your .env file.")

# ✅ Grok client setup
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Health Report AI Backend Running 🚀"}


# 🔥 LLM FUNCTION
def extract_structured_data(text):
    prompt = f"""
    You are a medical report analyzer.

    Extract all lab test values.

    Return ONLY valid JSON. No explanation. No markdown. No backticks.

    Format:
    {{
      "lab_test_values": [
        {{
          "name": "Hemoglobin",
          "value": 10.8,
          "normal_range": "12-15",
          "status": "Low"
        }}
      ]
    }}

    Text:
    {text}
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        content = response.choices[0].message.content

        # 🔥 Remove ```json ``` or ``` wrappers
        content = re.sub(r"```.*?```", lambda m: m.group(0).strip("`"), content, flags=re.DOTALL)
        content = content.replace("```json", "").replace("```", "").strip()

        # 🔥 Convert to JSON
        return json.loads(content)

    except Exception as e:
        return {"error": str(e)}

# 🔥 INSIGHT GENERATION
def generate_insights(data):
    insights = []

    lab_values = data.get("lab_test_values", [])

    low_params = []
    high_params = []

    for item in lab_values:
        if item.get("status") == "Low":
            low_params.append(item["name"])
        elif item.get("status") == "High":
            high_params.append(item["name"])

    if low_params:
        insights.append(f"Some parameters are lower than normal: {', '.join(low_params[:5])}")

    if high_params:
        insights.append(f"Some parameters are higher than normal: {', '.join(high_params[:5])}")

    blood_markers = ["Hemoglobin", "RBC", "HCT", "MCV", "MCH"]
    low_blood = [p for p in blood_markers if p in low_params]

    if len(low_blood) >= 2:
        insights.append("Multiple blood-related parameters are low, which may indicate anemia or related conditions.")

    inflammation_markers = [
        "High sensitivity CRP",
        "Erythrocyte Sedimentation Rate"
    ]
    high_inflammation = [p for p in inflammation_markers if p in high_params]

    if high_inflammation:
        insights.append("Inflammation markers are elevated, which may indicate inflammation or infection.")

    return insights

# 🔥 EXPLANATION GENERATION - LLM Powered
def generate_explanation(structured_data, insights):
    prompt = f"""
    You are a medical assistant.

    Based ONLY on the provided data and insights:
        - Do NOT infer conditions unless clearly supported by multiple abnormal markers
        - If a value is within normal range, DO NOT describe it as a problem
        - Avoid alarming language
        - Explain in simple, human-friendly language what it means.
        - Keep it Short, Clear, Non-alarming and Easy to understand

    IMPORTANT:
    - Order the explanations by PRIORITY
    - Most critical health concern FIRST
    - Less important observations later
    - GROUP related abnormalities into ONE explanation
    - Focus on overall patterns, not individual values
    - Prioritize based on severity and number of abnormal related markers

    Rules:
    - Do NOT create separate points for related parameters
    - Do NOT repeat similar explanations
    - Do NOT mention normal values as abnormal
    - Do NOT say things like "kidney issue" or another condition unless clearly abnormal, and supported by multiple related markers
    - Return ONLY a JSON array (list of strings)
    - Each point must be short (1 line)
    - No headings, no bullets, no markdown
    - No extra text

    Structured Data:
    {structured_data}

    Insights:
    {insights}

    Return as a list of explanations.
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        content = response.choices[0].message.content.strip()

        # 🔥 Clean markdown if present
        content = content.replace("```json", "").replace("```", "").strip()

        # 🔥 Parse JSON safely
        parsed = json.loads(content)

        # 🔥 Handle case where it's still a string
        if isinstance(parsed, str):
            parsed = json.loads(parsed)

        return parsed

    except Exception as e:
        return {"error": f"Explanation parsing failed: {str(e)}", "raw": content}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    text = ""

    # 📄 Handle PDF
    if file.filename.endswith(".pdf"):
        with open("temp.pdf", "wb") as f:
            f.write(contents)

        with pdfplumber.open("temp.pdf") as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"

    # 🖼️ Handle images (OCR)
    elif file.filename.endswith((".png", ".jpg", ".jpeg")):
        image = Image.open(io.BytesIO(contents))
        text = pytesseract.image_to_string(image)

    # 🔥 CALL LLM
    structured = extract_structured_data(text[:3000])  # limit size
    insights = generate_insights(structured)
    explanation = generate_explanation(structured, insights)

    return {
        "filename": file.filename,
        "structured_data": structured,
        "insights": insights,
        "explanation": explanation
    }

