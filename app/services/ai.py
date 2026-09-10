import json
import httpx
from fastapi import Request

from app.core.config import settings




class AIService:
    def __init__(
        self,
        client: httpx.AsyncClient,
        api_key: str,
    ):
        self.client = client
        self.api_key = api_key

    async def evaluate(
        self,
        exercise: str,
        code: str,
    ) -> dict:

        prompt = f"""
You are a programming exercise evaluator.

Exercise:
{exercise}

Student's code:
{code}

Evaluate the student's code.

Return ONLY valid JSON.
Do not use Markdown.
Do not add ```json.
Do not add any explanation outside the JSON.

Return exactly this structure:

{{
  "exerciseId": 1,
  "score": 100,
  "correctness": 10,
  "functionality": 10,
  "cleanCode": 10,
  "readability": 10,
  "maintainability": 10,
  "feedback": "string",
  "hints": [
    {{
      "text": "string"
    }}
  ]
}}

Rules:
- exerciseId: integer > 0
- score: integer from 0 to 100
- correctness: integer from 0 to 10
- functionality: integer from 0 to 10
- cleanCode: integer from 0 to 10
- readability: integer from 0 to 10
- maintainability: integer from 0 to 10
- feedback: 1 to 400 characters
- hints: 1 to 5 items
- each hint.text: 1 to 200 characters
- answers should be in persian
"""

        response = await self.client.post(
            "/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
            },
            json={
                "model": "openai/gpt-oss-120b",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                "temperature": 0,
            },
        )

        response.raise_for_status()

        data = response.json()

        try:
            content = data["choices"][0]["message"]["content"]
            return json.loads(content)

        except (
            KeyError,
            IndexError,
            TypeError,
            json.JSONDecodeError,
        ):
            raise ValueError("Invalid AI response")


def get_ai_service(request: Request) -> AIService:
    return AIService(
        client=request.app.state.http_client,
        api_key=settings.groq_api_key,
    )
