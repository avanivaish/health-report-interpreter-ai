from openai import OpenAI
from backend.config import GROQ_API_KEY
import json
import re

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

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