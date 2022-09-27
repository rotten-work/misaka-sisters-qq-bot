from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.event.mirai import NudgeEvent
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group
from graia.ariadne.message.parser.twilight import FullMatch, Twilight
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

from graia.ariadne.message.element import *
from graia.ariadne.message.parser.base import *

from pathlib import Path
from datetime import datetime

channel = Channel.current()

def contain_key_word(keyword, message):
    return keyword in message

@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage]))
async def test(app: Ariadne, member: Member, group: Group, message: MessageChain):
    if At(app.account) in message:
        fullString = str(message.include(At, Plain))
        subString = "御坂妹妹好"
        if (subString in fullString):
            if (member.id == 1078268141):
                await app.send_message(
                    group,
                    MessageChain([At(member), Plain(" 姐姐大人好，と，御坂压抑不住见到姐姐大人激动的心情，兴奋地说道"),
                        Image(path=Path("data_test", "happy.jpg"))])
                )
            elif (member.id == 469140955):
                await app.send_message(
                    group,
                    MessageChain([At(member), Plain(" 啊，是白吃的大儿子，と，御坂迅速地反应道")])
                )
            else:
                await app.send_message(
                    group,
                    MessageChain([At(member), Plain(" 请问你是谁，と，御坂歪着脑袋，警惕地打量着眼前的这个陌生人，困惑地询问道"),
                        Image(path=Path("data_test", "confused.png"))])
                )

        subString = "请问coh2这个游戏怎么样"
        if (subString in fullString):
            await app.send_message(
                group,
                MessageChain([At(member), Plain(" 盟棍连，盟军op，建议德棍uninstall，と，御坂通过御坂网络计算模拟分析后，作出了客观且准确的评价，并给出了中肯的建议")])
            )

        subString = "白吃是谁"
        if (subString in fullString):
            await app.send_message(
                group,
                MessageChain([At(member), Plain(" 是炸鸡的爸爸，と，御坂叹了口气，摇了摇头，因竟然有人不知道白吃是谁而惊讶地回答道"),
                    Image(path=Path("data_test", "sigh.png"))])
            )

        subString = "炸鸡的爸爸是谁"
        if (subString in fullString):
            # profile = await app.getUserProfile(1078268141)
            # profile2 = await app.getMemberProfile(1078268141)
            # profile2.nickname
            fwd_nodeList = [
                ForwardNode(
                        target=469140955,
                        senderName="菊花月下",
                        time=datetime.now(),
                        message=MessageChain(["我是白吃的大儿子"]) 
                    )
            ]

            message = MessageChain(Forward(nodeList=fwd_nodeList))
            await app.send_message(group, message)
            await app.send_message(
                group, 
                MessageChain([At(469140955), Plain(" do, 御坂强忍住不笑"), Image(path=Path("data_test", "giggle.png"))])
            )
    
    message_str = str(message.include(At, Plain))
    if (contain_key_word("英雄连", message_str) or
        contain_key_word("德棍", message_str) or 
        contain_key_word("盟棍", message_str) or
        contain_key_word("萌棍", message_str) or
        contain_key_word("盟军", message_str) or
        contain_key_word("德军", message_str) or
        re.match(r'[cC][oO][hH]2?', message_str)):
        await app.send_message(
            group,
            MessageChain([At(member), 
            Plain(" 盟棍连，盟军op，建议德棍uninstall，と，御坂通过御坂网络计算模拟分析后，作出了客观且准确的评价，并给出了中肯的建议"),
            Image(path=Path("data_test", "adorkable.jpg"))])
        )

@channel.use(ListenerSchema(listening_events=[NudgeEvent]))
async def nudged(app: Ariadne, event: NudgeEvent):
    if event.context_type == "group":
        if (event.target == app.account):            
            await app.send_group_message(
                event.group_id,
                MessageChain("检体番号：10032")
        )