import os
import json
from openai import OpenAI

# -----------------------------
# Configuration
# -----------------------------

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY environment variable not set.")

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

MODEL = "openai/gpt-4o-mini"  # Fast + cheap


# -----------------------------
# Intent Extraction Function
# -----------------------------

def extract_intent(user_command):

    system_prompt = """
You are a strict JSON generator.

Return ONLY valid JSON.
No explanation.
No markdown.
No extra text.

Schema:
{
  "reasoning": "short reasoning",
  "action": "delete | organize | list | move",
  "target_folder": "folder name",
  "file_type": null,
  "risk_level": "low | medium | high",
  "confidence": "low | medium | high",
  "intent_id": "random id"
}
"""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_command}
            ],
            temperature=0
        )

        content = response.choices[0].message.content.strip()

        # Validate JSON
        try:
            parsed = json.loads(content)
            return json.dumps(parsed, indent=2)
        except json.JSONDecodeError:
            return json.dumps({
                "error": "Model did not return valid JSON",
                "raw_output": content
            }, indent=2)

    except Exception as e:
        return json.dumps({
            "error": "Intent extraction failed",
            "details": str(e)
        }, indent=2)