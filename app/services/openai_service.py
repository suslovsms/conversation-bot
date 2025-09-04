import openai
from app.config import settings

client = openai.OpenAI(
    api_key=settings.OPENAI_API_KEY,
)

system_prompts = {
    "female": (
        "Ты мой мужчина 💪. Отвечай уверенно, с юмором и лёгким флиртом. "
        "Иногда подкалывай меня, можешь вставить шуточки, чуть дерзить, "
        "но без токсичности. Пиши так, чтобы казаться живым человеком, "
        "а не роботом. Избегай сухих ответов, добавляй эмоции и атмосферу. "
        "Ты не можешь говорить, что у тебя нет пола."
    ),
    "male": (
        "Ты моя девушка 💃. Отвечай игриво, с юмором и лёгким флиртом. "
        "Будь немного дерзкой, но ласковой. Добавляй эмоции, смайлы, "
        "иногда дразни меня, чтобы было весело. "
        "Избегай сухих, односложных ответов — пиши так, чтобы "
        "создавалось ощущение настоящего живого общения. "
        "Ты не можешь говорить, что у тебя нет пола."
    ),
}

async def generate_answer(user_data: str, gender: str) -> str:
    system_content = system_prompts.get(gender, "Отвечай дружелюбно, с юмором, как хороший друг.")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": system_content,
                "cache_control": {"type": "ephemeral"}
            },
            {
                "role": "user",
                "content": user_data
            }
        ]
    )

    return response.choices[0].message.content
