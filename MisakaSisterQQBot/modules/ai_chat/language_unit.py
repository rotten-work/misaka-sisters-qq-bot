import json
import requests
import random
import zhon.hanzi

# Should be async for practical use
def get_chat_result(text: str, url: str, key: str, id: int=0):
    req = {
        "reqType":0,
        "perception": {
            "inputText": {"text": text},
            "selfInfo": {
                "location": {
                    "city": "学园都市", "province": "第七学区", "street": "常盘台"
                }
            },
        },
        "userInfo": {"apiKey": key, "userId": str(id)}
    }

    payload = json.dumps(req)
    json_response = requests.post(url, data=payload)
    assert(json_response.status_code == 200)
    resp_payload = json.loads(json_response.text)

    if resp_payload["results"]:
        for result in resp_payload["results"]:
            if result["resultType"] == "text":
                text = result["values"]["text"]
                if "请求次数超过" in text:
                    text = ""
    return text


misaka_name = "御坂"

misaka_key_word = 'と'

# period = '。'

# 御坂如此不厌其烦地说明
# 询问

misaka_catchphrases = [
    "御坂如此回答。",
    "御坂如此回应。",
    "御坂如此表达。",
    "御坂如此说明。",
    "御坂如此述说。"
]

def post_process(response: str):
    processed_resp = response
    processed_resp = processed_resp.replace("我", misaka_name)
    processed_resp = processed_resp.replace("人家", misaka_name)
    processed_resp = processed_resp.replace("伦家", misaka_name)

    last_char = processed_resp[-1]
    random_phrase = random.choice(misaka_catchphrases)

    if last_char in zhon.hanzi.punctuation:
        post_catchphrase = f"{misaka_key_word}，{random_phrase}"
    else:
        post_catchphrase = f"。{misaka_key_word}，{random_phrase}"

    processed_resp = f"{processed_resp}{post_catchphrase}"
    
    return processed_resp


if __name__ == "__main__":
    import yaml
    with open('config.yml', 'r') as file:
        config = yaml.safe_load(file)

    request_text = "我身体难受"
    print("Request text:")
    print(request_text)

    response = get_chat_result(request_text, config['turing']['url'], config['turing']['key'])
    
    print("response text:")
    print(response)

    processed_resp = post_process(response)

    print("processed text:")
    print(processed_resp)

