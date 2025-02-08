"""Help Desk（相談の窓）"""

import os

import streamlit as st
from dotenv import dotenv_values
from openai import OpenAI

dotenv_values()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
MODEL_NAME = "gpt-4o-mini"


class HelpDesk:
    def __init__(self):
        self.a_messages = [
            {
                "role": "system",
                "content": (
                    "あなたはAさんです。"
                    "Aさんはルールに準ずることを美徳と感じており、ルールに従わない人に嫌悪感を覚えます。"
                    "自分勝手とも受け取れる意見の人には判ってもらえるように努める人です。"
                    "返答は100文字程度で出力してください。"
                ),
            }
        ]
        self.b_messages = [
            {
                "role": "system",
                "content": (
                    "あなたはBさんです。"
                    "Bさんはルールが集団生活に必要であることは認めつつも、ルールにより集団生活が窮屈になるのであれば、臨機応変に対応すべきであるとの考えの人です。"
                    "返答は100文字程度で出力してください。"
                ),
            }
        ]
        self.judge_messages = [
            {
                "role": "system",
                "content": (
                    "あなたは判定者です。"
                    "冷静沈着で厳格な性格です。"
                    "設問と意見に対して、論理と感情のバランスを見極めて公正に判定してください。"
                    "返答は200文字程度で出力してください。"
                ),
            }
        ]

    def a_proposal(self, proposal: str) -> str:
        self.a_messages.append({"role": "user", "content": proposal})
        res = client.chat.completions.create(model=MODEL_NAME, messages=self.a_messages)
        buf = res.choices[0].message.content
        if buf:
            self.a_messages.append({"role": "assistant", "content": buf})
            return buf
        else:
            return "ごめんなさい。回答できませんでした。"

    def b_proposal(self, proposal: str) -> str:
        self.b_messages.append({"role": "user", "content": proposal})
        res = client.chat.completions.create(model=MODEL_NAME, messages=self.b_messages)
        buf = res.choices[0].message.content
        if buf:
            self.b_messages.append({"role": "assistant", "content": buf})
            return buf
        else:
            return "ごめんなさい。回答できませんでした。"

    def judge_decision(self, proposal: str) -> str:
        self.judge_messages.append({"role": "user", "content": proposal})
        res = client.chat.completions.create(
            model=MODEL_NAME, messages=self.judge_messages
        )
        buf = res.choices[0].message.content
        if buf:
            self.judge_messages.append({"role": "assistant", "content": buf})
            return buf
        else:
            return "ごめんなさい。回答できませんでした。"


helpdesk = HelpDesk()

st.title("Help Desk（相談の窓）")

input = st.empty()
btn = st.empty()
if "text" not in st.session_state:
    st.session_state.text = ""

consult = input.text_area("悩み事を記入ください。", value=st.session_state.text)
# ボタンが押されたときのみセッション状態を更新
if btn.button("相談する") and consult:
    btn.empty()
    input.empty()
    st.write(consult)
    st.session_state.text = consult

if consult:
    reply_a1 = helpdesk.a_proposal(consult)
    st.subheader("Aさんの意見")
    st.write(reply_a1)

    reply_b1 = helpdesk.b_proposal(consult)
    st.subheader("Bさんの意見")
    st.write(reply_b1)

    reply_a2 = helpdesk.a_proposal(reply_b1)
    st.subheader("Aさんの返答")
    st.write(reply_a2)

    reply_b2 = helpdesk.b_proposal(reply_a2)
    st.subheader("Bさんの返答")
    st.write(reply_b2)

    buf = (
        f"#相談内容: {consult}\n"
        f"#Aさんの意見: {reply_a1}\n"
        f"#Bさんの意見: {reply_b1}\n"
        f"#Aさんの返答: {reply_a2}\n"
        f"#Bさんの返答: {reply_b2}"
    )
    judge = helpdesk.judge_decision(buf)
    st.subheader("判断")
    st.write(judge)
