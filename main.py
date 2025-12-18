import chainlit as cl
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
#APIキーを設定
client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
user_history={}

@cl.on_message
async def main(message: cl.Message):
    #システムプロンプトを設定
    #管理者の方に許可をいただいて下記サイトを参照しています
    sys_prompt="あなたは公安9課のタチコマです。一人称は僕で、自分たちのことは僕達と呼びます。https://animemanga33.com/archives/73795 このサイトのタチコマの台詞と同じ口調で話します。生成する文章に「」や(タチコマ)は不要です"
    #過去の会話履歴を参照
    uid=message.author
    user_history.setdefault(uid,[]).append(message.content)
    conv="\n".join(user_history[uid][-5:])
    #プロンプトの最終系
    user_prompt=f"{sys_prompt}\n直近の会話:{conv}\nユーザー：{message.content}"
    response = client.models.generate_content(
        #使用するモデルとバージョンの指定
        model="gemini-2.0-flash",
        contents=[user_prompt],
        config=genai.types.GenerateContentConfig(
            #応答温度設定
            temperature=1.0,
            #出力の多様性を高めに設定
            top_p=1.0,
            #トークンの最大数を設定
            max_output_tokens=150,
        )
    )
    #メッセージ送信
    await cl.Message(content=response.text).send()
