import asyncio
import logging
import os
import sys
import yaml

import pykeybasebot.types.chat1 as chat1
from pykeybasebot import Bot

inputs = None
with open('MyPack.yaml', 'r') as stream:
    inputs = yaml.safe_load(stream)

packs = inputs['Packages']
keyphrase = inputs['KeyPhrase'].lower()

logging.basicConfig(level=logging.DEBUG)

if "win32" in sys.platform:
    # Windows specific event-loop policy
    asyncio.set_event_loop_policy(
        asyncio.WindowsProactorEventLoopPolicy()  # type: ignore
    )

listen_options = {
    "local": True,
    "wallet": True,
    "dev": True,
    "hide-exploding": False,
    "convs": True,
    "filter_channel": None,
    "filter_channels": None,
}


def makeString(dict):
    pack_str = 'My Packages 📦\n'
    for key, value in dict.items():
        pack_str = pack_str + key + ' : ' + value + '\n'
    return pack_str + '\n'


async def handler(bot, event):
    if event.msg.content.type_name != chat1.MessageTypeStrings.TEXT.value:
        return
    msg = str(event.msg.content.text.body).lower()
    if keyphrase in msg:
        channel = event.msg.channel
        sender = event.msg.sender.username
        # print(sender)
        if sender == bot.username:
            # print(msg)
            return
        pack_str = makeString(packs)
        # print(pack_str)
        await bot.chat.send(channel, pack_str)

paperkey = os.environ.get("KEYBASE_PAPERKEY")
username = os.environ.get('KEYBASE_USERNAME')

bot = Bot(
    username=username, paperkey=paperkey, handler=handler
)

asyncio.run(bot.start(listen_options))
