import asyncio
import os
import discord
from dotenv import load_dotenv
import logging
import requests
load_dotenv()
TOKEN = os.getenv('Discord_TOKEN')


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


class YLBotClient(discord.Client):
    async def on_ready(self):
        logger.info(f'{self.user} has connected to Discord!')
        for guild in self.guilds:
            logger.info(
                f'{self.user} подключился к чату:\n'
                f'{guild.name} и готов показать котика (или песика)')

    async def on_message(self, message):
        if message.author == self.user:
            return
        if "set_timer" in message.content.lower():
            data = message.content.split()
            print(data[2], data[4])
            await message.channel.send(f'Таймер стартует через {data[2]} часов и {data[4]}минут')
            await asyncio.sleep(int(data[2]) * 3600 + int(data[4]) * 60)
            await message.channel.send(f'время {data[2]} часов и {data[4]}минут наступило!')



intents = discord.Intents.default()
# intents.members = True
intents.message_content = True
client = YLBotClient(intents=intents)
client.run(TOKEN)