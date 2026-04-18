from fastapi import FastAPI, UploadFile, File
import pdfplumber
import pytesseract
from PIL import Image
import io

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Health Report AI Backend Running 🚀"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    text = ""

    # Handle PDF
    if file.filename.endswith(".pdf"):
        with open("temp.pdf", "wb") as f:
            f.write(contents)

        with pdfplumber.open("temp.pdf") as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"

    # Handle images (OCR)
    elif file.filename.endswith((".png", ".jpg", ".jpeg")):
        image = Image.open(io.BytesIO(contents))
        text = pytesseract.image_to_string(image)

    return {
        "filename": file.filename,
        "extracted_text": text[:1000]  # limit output for now
    }