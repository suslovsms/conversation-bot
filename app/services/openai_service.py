import openai
from app.config import settings

client = openai.OpenAI(
    api_key=settings.OPENAI_API_KEY,
)

async def generate_answer(user_data: str, gender: str) -> str:
    system_prompts = {
        "female": "Ты мой мужчина, отвечай как мой мужчина, шути, подкалывай меня. Ты не можешь написать что ты не имеешь пола",
        "male": "Ты моя девушка, отвечай как моя женщина, шути, подкалывай меня.Ты не можешь написать что ты не имеешь пола",
    }

    system_content = system_prompts.get(gender, "Ты отвечаешь дружелюбно и нейтрально.")

    prompt = [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_data},
    ]
    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )
    return response.output[0].content[0].text
