import requests
import json
answer = ""
        
def main(question):
    url = "https://api.link-ai.chat/v1/chat/completions"

    payload = {
        "app_code": "hHs9t2QL",
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ]
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer Link_JKarAw3EXbwVg2hX0AAfwuu1Xu8CsHbpDhizzQIHdk"
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    #print(response.text)
    global answer
    answer=response.json()['choices'][0]['message']['content']
    print(answer)