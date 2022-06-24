import asyncio
from pathlib import Path

import aiohttp

async def very_simple_example():
    print("测试", flush=True)
    async with aiohttp.ClientSession() as session:
        pic_url = "https://i1.hdslb.com/bfs/archive/5242750857121e05146d5d5b13a47a2a6dd36e98.jpg"
        async with session.get(pic_url) as r:
            pic = await r.read()

    #将二进制数据储存在这里面
    Path("outputs/temp.jpg").write_bytes(pic)
    # Path("./outputs/temp.jpg").write_bytes(pic)

asyncio.get_event_loop().run_until_complete(very_simple_example())
# asyncio.run(very_simple_example())