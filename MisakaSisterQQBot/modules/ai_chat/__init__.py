from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

# Import magic cause weired problems. Don't know why for now.
# from graia.ariadne.message.element import Plain
from graia.ariadne.message.element import *
# from graia.ariadne.message.element import Member
# import graia.ariadne.message.element as element
# from graia.ariadne.message.parser.base import *

import os
import pathlib
import yaml

import random

# or
# file_dir = os.path.dirname(__file__)
# sys.path.append(file_dir)
# import language_unit
from . import language_unit
from . import sentiment_unit

config_path = pathlib.Path(__file__).with_name('config.yml')

with open(config_path, 'r') as file:
    config = yaml.safe_load(file)

channel = Channel.current()

prob_min_sentiment = 0.75
prob_min_angry = 0.5

current_file_dir = pathlib.Path(__file__).parent.resolve()
POSITIVE_MAIN_EMOTICONS_DIR = "emoticons/positive/main/"
POSITIVE_MAIN_EMOTICONS_DIR = os.path.join(current_file_dir, POSITIVE_MAIN_EMOTICONS_DIR)

ANGRY_EMOTICONS_DIR = "emoticons/negative/angry/"
ANGRY_EMOTICONS_DIR = os.path.join(current_file_dir, ANGRY_EMOTICONS_DIR)

def get_file_paths(dir):
    files = os.listdir(dir)
    paths = []
    for f in files:
        paths.append(os.path.join(dir, f))
    return paths

positive_main_emoticon_paths = get_file_paths(POSITIVE_MAIN_EMOTICONS_DIR)
angry_emoticon_paths = get_file_paths(ANGRY_EMOTICONS_DIR)

# print(positive_main_emoticon_paths)
# print(angry_emoticon_paths)

from .misaka_writer_V2 import generate

@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage]))
async def respond(app: Ariadne, member: Member, group: Group, message: MessageChain):
    if At(app.account) in message:
        plain_string = str(message.include(At, Plain))

        use_misaka_writer = True
        if use_misaka_writer:
            import time
            text=plain_string.replace( '氼。','\n')
            start=time.time()

            nums=1#开头生成多个下文
            k=0.8#搜索窗口
            batch_size=32
            max_len=32#最大长度
            repeat_punish=0.99#惩罚因子

            #输入，建议开头字数在50字到200字之间
            result=generate.writer([text.replace('\n', '氼')],#文本数据就是上面的data
                        nums=nums,#输入要生成几个文本
                        k=k,
                        batch_size=batch_size,
                        max_len=max_len,
                        repeat_punish=repeat_punish)#检查重复解码
            end=time.time()

            s=''
            for t in text.split('\n'):
                s+='\t'+t+'\n'
            text=s
            for i in range(nums):
                print(text)
                print('*******************************************************************************')
                for t in result[i].split('氼'):
                    print('\t'+t)
                print('*******************************************************************************')
            print('消耗时间'+str(end-start))

            response = result[0].replace('氼', '\n')

            await app.send_message(
                group,
                MessageChain([At(member), Plain(f" {response}"),]))

        else:
            response = language_unit.get_chat_result(plain_string, config['turing']['url'], config['turing']['key'])

            processed_resp = language_unit.post_process(response)

            """ 你的 APPID AK SK """
            APP_ID = config['baidu']['app_id']
            API_KEY = config['baidu']['api_key']
            SECRET_KEY = config['baidu']['secret_key']

            sentiment_res = sentiment_unit.get_sentiment_result(response, str(APP_ID), API_KEY, SECRET_KEY)
            print(sentiment_res)

            # Parse sentiment result
            sentiment_items = sentiment_res['items']

            item = None
            for current_item in sentiment_items:
                if item is not None:
                    if current_item['prob'] >= item['prob']:
                        item = current_item
                else:
                    item = current_item
            
            prob = item['prob']
            label = item['label']
            subitems = item['subitems']

            postive_label = sentiment_unit.postive_label
            negative_label = sentiment_unit.negative_label

            random_emoticon_path = None
            if prob >= prob_min_sentiment:
                if label == postive_label:
                    print("Show positive emoticon")
                    random_emoticon_path = random.choice(positive_main_emoticon_paths)
                elif label == negative_label:
                    for subitem in subitems:
                        if (subitem['label'] == 'angry' and
                            subitem['prob'] >= prob_min_angry):
                            print("Show angry negative emoticon")
                            random_emoticon_path = random.choice(angry_emoticon_paths)
                            break
            
            print(random_emoticon_path)
            if random_emoticon_path is None:
                await app.send_message(
                    group,
                    MessageChain([At(member), Plain(f" {processed_resp}"),]))
            else:
                img_elem = Image(path=random_emoticon_path)
                await app.send_message(
                    group,
                    MessageChain([At(member), img_elem, Plain(f" {processed_resp}"),]))