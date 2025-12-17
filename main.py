import chainlit as cl
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
# API キーを設定
client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
user_history={}

@cl.on_message
async def main(message: cl.Message):
    uid=message.author
    user_history.setdefault(uid,[]).append(message.content)
    sys_prompt=(os.getenv("PROMPT"))
    conv="\n".join(user_history[uid][-3:])
    user_prompt=f"{sys_prompt}\n直近の会話:{conv}\nユーザー：{message.content}"
    response = client.models.generate_content(
        #使用するモデルとバージョンの指定
        model="gemini-2.0-flash",
        contents=[user_prompt],
        config=genai.types.GenerateContentConfig(
            temperature=1.0,
            top_p=1.0,
            max_output_tokens=150,
        )
    )

    await cl.Message(content=response.text).send()
