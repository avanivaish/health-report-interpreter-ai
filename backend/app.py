from pathlib import Path
import sys

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.services.llm_service import extract_structured_data
from backend.services.insight_service import generate_insights
from backend.services.explanation_service import generate_explanation
from backend.services.risk_service import generate_risk
from backend.services.history_service import HistoryStore
from backend.utils.parser import extract_text

app = FastAPI()
history_store = HistoryStore()
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

    result = {
        "filename": file.filename,
        "structured_data": structured,
        "insights": insights,
        "explanation": explanation,
        "risk_level": risk
    }
    history_store.save_result(file.filename or "report", result)

    return result


@app.get("/history")
def get_history(search: str = None, risk_level: str = None):
    return history_store.get_history(search_query=search, risk_level=risk_level)


@app.get("/report/{report_id}")
def get_report(report_id: str):
    report = history_store.get_report(report_id)
    if report is None:
        return {"error": "Report not found"}, 404
    return report


@app.delete("/report/{report_id}")
def delete_report(report_id: str):
    success = history_store.delete_report(report_id)
    if not success:
        return {"error": "Report not found"}, 404
    return {"deleted": True}


@app.get("/report/{report_id}/export")
def export_report(report_id: str, format: str = "json"):
    import json as json_lib

    report = history_store.get_report(report_id)
    if report is None:
        return {"error": "Report not found"}, 404

    if format == "json":
        return report

    if format == "pdf":
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas
            from reportlab.lib.utils import ImageReader
            from io import BytesIO
            from fastapi.responses import StreamingResponse

            buffer = BytesIO()
            pdf = canvas.Canvas(buffer, pagesize=letter)
            width, height = letter
            
            # Helper function to wrap text
            def wrap_text(text, max_width, font_size, font_name="Helvetica"):
                pdf.setFont(font_name, font_size)
                words = text.split()
                lines = []
                current_line = ""
                
                for word in words:
                    test_line = current_line + (" " if current_line else "") + word
                    if pdf.stringWidth(test_line, font_name, font_size) < max_width:
                        current_line = test_line
                    else:
                        if current_line:
                            lines.append(current_line)
                        current_line = word
                
                if current_line:
                    lines.append(current_line)
                return lines
            
            # Helper to draw wrapped text
            def draw_wrapped_text(text, x, y, max_width, font_size, font_name="Helvetica", is_bold=False):
                font = f"{font_name}-Bold" if is_bold else font_name
                lines = wrap_text(text, max_width, font_size, font_name)
                for line in lines:
                    pdf.setFont(font, font_size)
                    pdf.drawString(x, y, line)
                    y -= font_size + 2
                return y

            pdf.setFont("Helvetica-Bold", 16)
            pdf.drawString(50, height - 50, f"Report: {report['filename']}")

            pdf.setFont("Helvetica", 9)
            pdf.drawString(50, height - 70, f"Generated: {report['created_at']}")

            result = report.get("result", {})
            y = height - 100
            max_text_width = width - 120

            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(50, y, "Risk Level:")
            pdf.setFont("Helvetica", 11)
            pdf.drawString(150, y, result.get("risk_level", "Unknown"))

            y -= 25
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(50, y, "Insights:")
            y -= 15

            for insight in result.get("insights", [])[:5]:
                y = draw_wrapped_text(f"• {insight}", 70, y, max_text_width, 9)
                y -= 5

            y -= 10
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(50, y, "Explanation:")
            y -= 15

            for exp in result.get("explanation", [])[:5]:
                y = draw_wrapped_text(f"• {exp}", 70, y, max_text_width, 9)
                y -= 5

            pdf.save()
            buffer.seek(0)

            return StreamingResponse(
                iter([buffer.getvalue()]),
                media_type="application/pdf",
                headers={"Content-Disposition": f"attachment;filename={report_id}.pdf"},
            )
        except ImportError:
            return {
                "error": "PDF export requires reportlab. Install: pip install reportlab"
            }, 400

    return {"error": "Invalid format. Use 'json' or 'pdf'"}, 400