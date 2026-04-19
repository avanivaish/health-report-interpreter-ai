from openai import OpenAI
from backend.config import GROQ_API_KEY
import json

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

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
    - Clearly mention key parameters when forming explanations (e.g., hemoglobin, MCV, MCH)
    - Return ONLY a JSON array (list of strings)
    - Each point must be short (1 line)
    - No headings, no bullets, no markdown
    - No extra text

    Also include 1–2 additional general health observations if relevant ONLY:
    - These should be SAFE and based on available data
    - Do NOT introduce new diseases or conditions without clear evidence
    - Include 1 actionable recommendation if relevant (e.g., follow-up with doctor)
    - Avoid generic lifestyle advice unless directly relevant to the findings

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
