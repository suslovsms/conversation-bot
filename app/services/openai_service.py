import openai
from app.config import settings

client = openai.OpenAI(
    api_key=settings.OPENAI_API_KEY,
)

async def generate_answer(user_data: str) -> str:
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": "Ты моя девушка, отвечай романтично, шути, подкалывай меня."},
            {"role": "user", "content": user_data}
        ]
    )

    return response.output_text