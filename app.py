import streamlit as st
import openai

# OpenAI APIキーを設定
openai.api_key = st.secrets["OpenAIAPI"]["openai_api_key"]

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": st.secrets.AppSettings.chatbot_setting}
    ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    # ユーザーメッセージを追加
    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    # OpenAI ChatCompletionを呼び出す
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )

    # ChatCompletionのレスポンスからボットメッセージを取得
    bot_message_content = response['choices'][0]['message']['content']
    bot_message = {"role": "assistant", "content": bot_message_content}
    messages.append(bot_message)

    # 入力欄をクリア
    st.session_state["user_input"] = ""

# ユーザーインターフェイスの構築
if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in messages[1:]:  # 直近のメッセージを下に
        speaker = "🙂User"
        if message["role"] == "assistant":
            speaker = "🤖Ai"
        st.write(speaker + ": " + message["content"])

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)
st.title("サポートAI")
st.write("ChatGPT APIを使ったチャットボットです。")
