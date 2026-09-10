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
    ) -> str:

        prompt = """
You are a programming exercise evaluator.

Exercise:
{0}

Student's code:
{1}

Evaluate the student's code.

Return ONLY valid JSON.
    Do not use Markdown.
    Do not add ```json.
    Do not add any explanation outside the JSON.

Answer exacly in this format:
{
  "exerciseId": 1,
  "score": 100,
  "correctness": 10,
  "functionality": 10,
  "cleanCode": 10,
  "readability": 10,
  "maintainability": 10,
  "feedback": "string",
  "hint": [
    {
      "text": "string"
    }
  ]
the pydantic schema is:
exerciseIdinteger> 0
scoreinteger[0, 100]
correctnessinteger[0, 10]
functionalityinteger[0, 10]
cleanCodeinteger[0, 10]
readabilityinteger[0, 10]
maintainabilityinteger[0, 10]
feedbackstring[1, 400] characters
hint allarray<object>[1, 5] items
Items allobject
textstring[1, 200] characters
""".format(exercise, code)

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
            return data["choices"][0]["message"]["content"]

        except (KeyError, IndexError, TypeError):
            raise ValueError("Invalid AI response")



def get_ai_service(request: Request) -> AIService:
    return AIService(
        client=request.app.state.http_client,
        api_key=settings.groq_api_key,
    )
