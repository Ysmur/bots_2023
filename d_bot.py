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
        if "кот" in message.content.lower():
            address = f"https://api.thecatapi.com/v1/images/search"
            response = requests.get(address)
            data = response.json()
            # print(data)
            await message.channel.send(data[0]['url'])
        else:
            await message.channel.send("Собака")


intents = discord.Intents.default()
# intents.members = True
intents.message_content = True
client = YLBotClient(intents=intents)
client.run(TOKEN)