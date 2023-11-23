import asyncio
import os
from threading import Thread

import discord
from dotenv import load_dotenv
from flask import Flask, request

from arcbot.bot_action.core import DiscordChannel
from arcbot.messenger.core import send_message


load_dotenv()
DISCORD_KEY = os.getenv('BOT_TOKEN')
app = Flask(__name__)


def setup_client():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    intents.guilds = True
    if os.getenv('SHARDED'):
        return discord.AutoShardedClient(intents=intents)
    return discord.Client(intents=intents)


def init():
    loop = asyncio.get_event_loop()
    loop.create_task(client.start(DISCORD_KEY))
    Thread(target=loop.run_forever).start()


client = setup_client()


@app.post('/message/<guild_id>/<channel_id>')
async def send_message_to_channel(guild_id: int, channel_id: int):
    message = request.json['message']
    guild = asyncio.run_coroutine_threadsafe(client.fetch_guild(guild_id), client.loop).result()
    channel = asyncio.run_coroutine_threadsafe(guild.fetch_channel(channel_id), client.loop).result()
    message = asyncio.run_coroutine_threadsafe(send_message(DiscordChannel(channel), message), client.loop).result()
    return {'content': message.get_content(), 'id': message.get_id()}
