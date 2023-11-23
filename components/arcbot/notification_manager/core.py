import importlib
import os

import requests
from dotenv import load_dotenv

from arcbot.discord_model.core import *
from arcbot.repository import core as repository

load_dotenv()

send_message = importlib.import_module(os.getenv('SEND_MESSAGE_MODULE')).send_message


async def send_notification_messages(client):
    URL = "https://accounts.spotify.com/api/token"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    body = {
        'grant_type': 'client_credentials',
        'client_id': os.getenv('SPOTIFY_CLIENT_ID'),
        'client_secret': os.getenv('SPOTIFY_CLIENT_SECRET')
    }

    response = requests.post(URL, headers=headers, data=body)
    data = response.json()

    access_token = data['access_token']

    topics = repository.get_topics()
    for topic in topics:

        URL = f'https://api.spotify.com/v1/artists/{topic.external_id}/albums'
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(URL, headers=headers)
        data = response.json()

        albums = data['items']
        for album in albums:
            if topic.last_release_date is None or album['release_date'] > topic.last_release_date:
                topic.last_release_date = album['release_date']
                repository.update_topic_last_release_date(topic.id, album['release_date'])
                subscribers_by_guild = {}
                for subscription in topic.subscriptions:
                    if subscription.guild_id not in subscribers_by_guild:
                        subscribers_by_guild[subscription.guild_id] = []
                    subscribers_by_guild[subscription.guild_id].append(subscription.user_id)
                for guild_id, subscribers in subscribers_by_guild.items():
                    guild = client.get_guild(int(guild_id))
                    channel = guild.system_channel
                    if channel is None:
                        continue
                    message = (f'Hey {" ".join([f"<@{subscriber}>" for subscriber in subscribers])} there\'s a new '
                               f'release from {topic.name}!\n{album["name"]}\n{album["external_urls"]["spotify"]}')
                    await send_message(DiscordChannel(channel), message)
