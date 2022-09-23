from aip import AipNlp
from PIL import Image

postive_label = 'optimistic'
negative_label = 'pessimistic'

def get_sentiment_result(text: str, id: str, key: str, scret_key: str, scene: str='talk'):
    client = AipNlp(id, key, scret_key)

    options ={}
    options['scene'] = scene

    result = client.emotion(text, options)

    return result

if __name__ == "__main__":
    import yaml

    with open('config.yml', 'r') as file:
        config = yaml.safe_load(file)
    
    """ 你的 APPID AK SK """
    APP_ID = config['baidu']['app_id']
    API_KEY = config['baidu']['api_key']
    SECRET_KEY = config['baidu']['secret_key']

    test_text = "气死我了"

    sentiment_res = get_sentiment_result(test_text, str(APP_ID), API_KEY, SECRET_KEY)
    print(sentiment_res)
    # sentiment_list = sentiment_res['items']
    # print(sentiment_list)

    im = Image.open("emoticons/negative/angry/aim_0.jpg")
    im.show()