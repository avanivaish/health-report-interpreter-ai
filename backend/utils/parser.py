import pdfplumber
import pytesseract
from PIL import Image
import io


async def extract_text(file):
    contents = await file.read()
    text = ""

    if file.filename.endswith(".pdf"):
        with open("temp.pdf", "wb") as f:
            f.write(contents)

        with pdfplumber.open("temp.pdf") as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"

    elif file.filename.endswith((".png", ".jpg", ".jpeg")):
        image = Image.open(io.BytesIO(contents))
        text = pytesseract.image_to_string(image)

    return text