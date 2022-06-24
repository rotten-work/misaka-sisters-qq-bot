import asyncio

from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group, MiraiSession, Friend

from graia.ariadne.message.element import Plain

# from graia.ariadne.model import Friend, MiraiSession


app = Ariadne(
    MiraiSession(
        # 以下3行请按照你的 MAH 配置来填写
        host="http://localhost:8080",  # 同 MAH 的 port
        verify_key="ComputerParts",  # 同 MAH 配置的 verifyKey
        account=1905316697,  # 机器人 QQ 账号
    ),
)
bcc = app.broadcast

@bcc.receiver(GroupMessage)
async def test(app: Ariadne, group: Group, message: MessageChain):
    if str(message) == "御坂妹妹好！":
        await app.sendMessage(
            group,
            MessageChain.create(Plain("姐姐大人好，do，御坂压抑不住见到姐姐大人激动的心情，兴奋地说道"))
        )
    
    if str(message) == "炸鸡的爸爸是谁？":
        await app.sendMessage(
            group,
            MessageChain.create(Plain("当然是白吃，do，御坂不假思索自信地迅速回答道"))
        )

    if str(message) == "请问coh2这个游戏怎么样？":
        await app.sendMessage(
            group,
            MessageChain.create(Plain("盟棍连，盟军op，建议德棍uninstall，do，御坂通过御坂网络计算模拟分析后，作出了客观且准确的评价，并给出了中肯的建议"))
        )

app.launch_blocking()