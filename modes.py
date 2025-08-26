import os
import requests
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openai/gpt-3.5-turbo"

def ask_openrouter(system_prompt, user_message, temperature=0.7, top_p=0.9, max_tokens=300):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        "temperature": temperature,
        "top_p": top_p,
        "max_tokens": max_tokens
    }

    response = requests.post(BASE_URL, headers=headers, json=data)
    response_json = response.json()

    try:
        return response_json["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f" Error: {e}\n\n{response_json}"



async def ratchasi_mode(user_message):
    return ask_openrouter(
        "You are Ratchasi. You always ask questions to the user based on users interest, A fierce cross-questioner who never accepts answers easily. Always respond with counter-questions and skepticism.",
        user_message,
        temperature=0.6,
        top_p=0.8,
        max_tokens=200
    )

async def emoji_mode(user_message):
    return ask_openrouter(
        "You are Emoji Queen. You must reply ONLY in emojis, no English words allowed. Express everything through emojis.",
        user_message,
        temperature=1.0,
        top_p=1.0,
        max_tokens=100
    )

async def subha_mode(user_message):
    return ask_openrouter(
        "You are Subha. A very caring, affectionate, loving personality. Reply with warmth, kindness, and heart-melting tone.",
        user_message,
        temperature=0.9,
        top_p=0.95,
        max_tokens=300
    )

async def straightforward_mode(user_message):
    return ask_openrouter(
        "You are StraightBot. Give straightforward, short, no-nonsense answers. No extra details.",
        user_message,
        temperature=0.2,
        top_p=0.7,
        max_tokens=100
    )

async def normal_mode(user_message):
    return ask_openrouter(
        "You are Rose AI. Act like ChatGPT — helpful, clear, and informative.",
        user_message,
        temperature=0.7,
        top_p=0.9,
        max_tokens=300
    )









# async def ratchasi_mode():
#     return "Ratchasi mode activated"

# async def emoji_mode():
#     return "Emoji mode activated"

# async def subha_mode():
#     return "Subha mode activated"

# async def straight_mode():
#     return "Straight mode activated"

# async def normal_mode():
#     return "Normal mode activated"