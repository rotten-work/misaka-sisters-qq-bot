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

@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage]))
async def respond(app: Ariadne, member: Member, group: Group, message: MessageChain):
    if At(app.account) in message:
        plain_string = str(message.include(At, Plain))
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