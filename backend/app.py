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

    return {
        "filename": file.filename,
        "structured_data": structured
    }