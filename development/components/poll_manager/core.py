from random import random

from development.components.bot_action.core import send_message, add_reactions
from development.components.command.core import play, playlist_play
from development.components.repository import core as repository

emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']


class DotDict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


async def send_poll_messages(client):
    print(f'Sending polls to {client.guilds}')
    for guild in client.guilds:
        print(f"Sending poll for {guild.name}")
        channel = guild.system_channel
        if channel is None:
            continue
        playlists = repository.get_playlists(str(guild.id))
        if len(playlists) == 0:
            continue
        message = "Vote for tomorrow's Playlists:\n"
        for i in range(min(len(playlists), 10)):
            message += f'{emojis[i]} {playlists[i].name}\n'
        sent_message = await send_message(channel, message)
        await add_reactions(sent_message, emojis[:min(len(playlists), 10)])
        repository.save_poll(str(guild.id), str(sent_message.get_id()), str(channel.id))


async def notify_poll_winners(client):
    for poll in repository.get_polls():
        repository.delete_poll(poll.id)
        guild = client.get_guild(int(poll.guild_id))
        channel = guild.get_channel(int(poll.channel_id))

        if poll.winner_name is not None:
            await play_winner_playlist(poll.winner_name, channel, guild, client)
            continue

        message = await channel.fetch_message(int(poll.message_id))
        vote_count = {}
        for reaction in message.reactions:
            if reaction.emoji in emojis:
                vote_count[reaction.emoji] = reaction.count
        # sort by vote count
        vote_count = {k: v for k, v in sorted(vote_count.items(), key=lambda item: item[1], reverse=True)}
        # check for tie
        if list(vote_count.values())[0] == list(vote_count.values())[1]:
            await send_message(channel, "There was a tie! Picking random playlist...")
            winner = list(vote_count.keys())[int(random() * len(vote_count))]
        else:
            winner = list(vote_count.keys())[0]
        playlist = repository.get_playlist_by_name(str(guild.id),
                                                   message.content.split('\n')[emojis.index(winner) + 1].split(' ')[1])
        if playlist is None:
            continue
        await play_winner_playlist(playlist.name, channel, guild, client)


async def play_winner_playlist(playlist_name, channel, guild, client):
    await send_message(channel, f'The winner is {playlist_name}!')
    # loop through voice channels to find someone connected
    for voice_channel in guild.voice_channels:
        if len(voice_channel.members) > 0:
            await playlist_play(playlist_name, DotDict(
                {'message': DotDict({'guild': guild,
                                     'author': DotDict({'voice': DotDict({'channel': voice_channel})})
                                     }, ), 'client': client, 'channel': channel}))
