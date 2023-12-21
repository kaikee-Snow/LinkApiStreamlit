import streamlit as st
import LinkApi
#以下密钥信息从控制台获取
api_key ="Link_JKarAw3EXbwVg2hX0AAfwuu1Xu8CsHbpDhizzQIHdk"
Link_url = "https://api.link-ai.chat/v1/chat/completions"
st.set_page_config(page_title="AD家园AI小助手", layout="centered", page_icon="🔥")

text =[]
def getText(role,content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text

def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length

def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text


if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if __name__ == '__main__':
    st.success("欢迎与AD家园AI小助手进行交流,咨询结果不能作为治疗依据,详情请咨询专业医生！")
    user_input = st.chat_input("请输入你想咨询的问题！")
    if user_input is not None:
        progress_bar = st.empty()
        with st.spinner("内容已提交，AI小助手正在作答中！"):
            question = checklen(getText("user", user_input))
            LinkApi.answer = ""
            LinkApi.main(user_input)
            feedback = getText("assistant", LinkApi.answer)[1]["content"]
            if feedback:
                progress_bar.progress(100)
                st.session_state['chat_history'].append((user_input, feedback))
                for i in range(len(st.session_state["chat_history"])):
                    user_info = st.chat_message("user")
                    user_content = st.session_state["chat_history"][i][0]
                    user_info.write(user_content)
                    assistant_info = st.chat_message("assistant")
                    assistant_content = st.session_state["chat_history"][i][1]
                    assistant_info.write(assistant_content)

                with st.sidebar:
                    if st.sidebar.button("清除对话历史"):
                        st.session_state["chat_history"] = []

            else:
                st.info("对不起，我回答不了这个问题，请你更换一个问题，谢谢！")