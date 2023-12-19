import importlib
import os

from dotenv import load_dotenv

from arcbot.audio_fetcher.core import fetch_audio_file
from arcbot.bot_action.core import *
from arcbot.log.core import get_logger
from arcbot.queue_manager.core import add_song, get_queue_song_names, move_song, remove_song
from arcbot.strings.core import Strings

logger = get_logger('arcBot-logger')
load_dotenv()

repository = importlib.import_module(os.getenv('REPOSITORY_MODULE'))
send_message = importlib.import_module(os.getenv('SEND_MESSAGE_MODULE')).send_message


async def help_command(_args, context) -> Message:
    response = '\n'.join([str(command) for command in commands.values()])
    return await send_message(DiscordChannel(context.message.channel), response)


async def ping(_args, context) -> Message:
    return await send_message(context.channel, 'Pong!')


async def join(_args, context) -> Message:
    return await run_join_or_leave(context.message, should_join=True)


async def leave(_args, context) -> Message:
    return await run_join_or_leave(context.message, should_join=False)


async def play(args, context) -> Message:
    if os.name != 'nt' and not discord.opus.is_loaded():
        discord.opus.load_opus(os.getenv('OPUS_LIB'))

    voice_channel, voice_client = get_voice_channel_and_client(context.message)

    join_response = await join_or_leave(voice_channel, voice_client, should_join=True)
    logger.info(f'Join/Leave response from $play command: {join_response}')

    # Refresh voice client in case we just joined a channel
    _, voice_client = get_voice_channel_and_client(context.message)
    if voice_client is None:
        return await send_message(context.channel, join_response)

    file_name, url, _ = await fetch_audio_file(args)

    if voice_client.is_playing() or voice_client.is_paused():
        add_song(context.message.guild.id, file_name, url)
        return await send_message(context.channel, song_added_to_queue_message(file_name))

    reply = play_audio_file(file_name, url, voice_client,
                            lambda: play_next_song(context.channel, voice_client, context.message.guild.id,
                                                   context.client.loop))
    return await send_message(context.channel, reply)


async def pause(_args, context) -> Message:
    return await run_pause_or_resume(context, Strings.Action.pause)


async def resume(_args, context) -> Message:
    return await run_pause_or_resume(context, Strings.Action.resume)


async def run_pause_or_resume(context, response) -> Message:
    _, voice_client = get_voice_channel_and_client(context.message)
    if voice_client is None:
        return await send_message(context.channel, Strings.Action.bot_not_connected)
    pause_or_resume(voice_client)
    return await send_message(context.channel, response)


async def skip(_args, context) -> Message:
    _, voice_client = get_voice_channel_and_client(context.message)
    if voice_client is None:
        return await send_message(context.channel, Strings.Action.bot_not_connected)
    new_song = skip_song(context.message.guild.id, voice_client, context.channel, context.client.loop)
    if new_song is None:
        await leave_channel(voice_client)
        return await send_message(context.channel, Strings.Action.bot_disconnected)
    return await send_message(context.channel, Strings.Action.now_playing(new_song))


async def queue(args, context) -> Message:
    songs: list[str] = get_queue_song_names(context.message.guild.id)
    if len(songs) == 0:
        return await send_message(context.channel, Strings.Queue.empty)
    return await send_message(context.channel, '\n'.join([f'{i + 1}. {song}' for i, song in enumerate(songs)]))


async def move(args, context) -> Message:
    move_from, move_to = args.split(' ')
    moved_song = move_song(context.message.guild.id, int(move_from) - 1, int(move_to) - 1)
    if moved_song is None:
        return await send_message(context.channel, Strings.Error.invalid_move)
    return await send_message(context.channel, Strings.Action.song_moved(moved_song, move_to))


async def remove(args, context) -> Message:
    removed_song = remove_song(context.message.guild.id, int(args) - 1)
    if removed_song is None:
        return await send_message(context.channel, Strings.Error.invalid_remove)
    return await send_message(context.channel, Strings.Action.song_removed(removed_song))


async def list_playlists(_args, context) -> Message:
    playlists = repository.get_playlists(str(context.message.guild.id))
    if len(playlists) == 0:
        return await send_message(context.channel, Strings.Error.no_playlists)
    return await send_message(context.channel,
                              '\n'.join([f'- {playlist.name} by <@{playlist.user_id}>' for i, playlist in
                                         enumerate(playlists)]))


async def playlist_create(args, context) -> Message:
    saved_name = repository.save_playlist(args, str(context.message.author.id), str(context.message.guild.id))
    if saved_name:
        return await send_message(context.channel, Strings.Action.playlist_created(saved_name))
    return await send_message(context.channel, Strings.Error.creating_playlist)


async def playlist_add(args, context) -> Message:
    playlist_name, song_name = args.split(' ', 1)
    file_name, _, original_url = await fetch_audio_file(song_name)
    was_added = repository.add_song(str(context.message.guild.id), playlist_name, original_url, file_name,
                                    str(context.message.author.id))
    if was_added:
        return await send_message(context.channel, Strings.Action.song_added_to_playlist(file_name, playlist_name))
    return await send_message(context.channel, Strings.Error.adding_to_playlist)


async def playlist_delete(args, context) -> Message:
    playlist_name = repository.delete_playlist(str(context.message.guild.id), args, str(context.message.author.id))
    if playlist_name:
        return await send_message(context.channel, Strings.Action.playlist_deleted(playlist_name))
    return await send_message(context.channel, Strings.Error.deleting_playlist)


async def playlist_remove(args, context) -> Message:
    playlist_name, song_name = args.split(' ', 1)
    file_name, _, original_url = await fetch_audio_file(song_name)
    was_removed = repository.remove_song(str(context.message.guild.id), playlist_name, original_url, file_name,
                                         str(context.message.author.id))
    if was_removed:
        return await send_message(context.channel, Strings.Action.song_removed_from_playlist(file_name, playlist_name))
    return await send_message(context.channel, Strings.Error.removing_from_playlist)


async def playlist_play(args, context) -> Message:
    playlist = repository.get_playlist_by_name(str(context.message.guild.id), args)
    if playlist is None or len(playlist.songs) == 0:
        return await send_message(context.channel, Strings.Error.playlist_not_found)
    song_to_play = playlist.songs[0].split(' ', 1)[0]
    response = await play(song_to_play, context)
    for song in playlist.songs[1:]:
        asyncio.run_coroutine_threadsafe(play(song.split(' ', 1)[0], context), context.client.loop)
    return response


async def playlist_info(args, context) -> Message:
    playlist = repository.get_playlist_by_name(str(context.message.guild.id), args)
    if playlist is None or len(playlist.songs) == 0:
        return await send_message(context.channel, Strings.Error.playlist_not_found)
    song_names = []
    for song in playlist.songs:
        song_names.append(f'- {song.split(" ", 1)[1]}')
    return await send_message(context.channel, '\n'.join(song_names))


async def poll_force(args, context) -> Message:
    if not context.message.author.guild_permissions.administrator:
        return await send_message(context.channel, Strings.Error.admin_only)
    playlist = repository.get_playlist_by_name(str(context.message.guild.id), args)
    if playlist is None:
        return await send_message(context.channel, Strings.Error.playlist_not_found)
    poll = repository.get_poll(str(context.message.guild.id))
    if poll is None:
        return await send_message(context.channel, Strings.Error.poll_not_found)
    repository.set_poll_winner(poll.id, playlist.name)
    return await send_message(context.channel, Strings.Action.poll_forced(playlist.name, context.message.author.id))


async def list_topics(args, context) -> Message:
    topics = repository.get_topics()
    if len(topics) == 0:
        return await send_message(context.channel, Strings.Error.no_topics)
    return await send_message(context.channel,
                              '\n'.join([f'- {topic.name}' for topic in
                                         topics]))


async def subscribe(args, context) -> Message:
    topic = repository.get_topic_by_name(args)
    if topic is None:
        return await send_message(context.channel, Strings.Error.topic_not_found)
    subscription = repository.get_subscription_by_user_id_and_topic_id(str(context.message.author.id), topic.id)
    if subscription is not None:
        return await send_message(context.channel, Strings.Error.already_subscribed)
    repository.save_subscription(str(context.message.author.id), topic.id, str(context.message.guild.id))
    return await send_message(context.channel, Strings.Action.subscribed(str(context.message.author.id), topic.name))


async def unsubscribe(args, context) -> Message:
    topic = repository.get_topic_by_name(args)
    if topic is None:
        return await send_message(context.channel, Strings.Error.topic_not_found)
    subscription = repository.get_subscription_by_user_id_and_topic_id(str(context.message.author.id), topic.id)
    if subscription is None:
        return await send_message(context.channel, Strings.Error.not_subscribed)
    repository.delete_subscription(subscription.id)
    return await send_message(context.channel, Strings.Action.unsubscribed(str(context.message.author.id), topic.name))


async def list_subscriptions(_args, context) -> Message:
    subscriptions = repository.get_subscriptions_by_user_id(str(context.message.author.id))
    if len(subscriptions) == 0:
        return await send_message(context.channel, Strings.Error.no_subscriptions)
    return await send_message(context.channel,
                              '\n'.join([f'- {subscription.topic.name}' for subscription in
                                         subscriptions]))


class Command:
    def __init__(self, name: str, description: str, function: callable):
        self.__name = name
        self.__description = description
        self.__function = function

    def __str__(self):
        return f'{self.__name}: {self.__description}'

    def execute(self, args, context):
        return self.__function(args, context)


commands = {
    'help': Command(name='help', description=Strings.Description.help, function=help_command),
    'ping': Command(name='ping', description=Strings.Description.ping, function=ping),
    'join': Command(name='join', description=Strings.Description.join, function=join),
    'leave': Command(name='leave', description=Strings.Description.leave, function=leave),
    'play': Command(name='play', description=Strings.Description.play, function=play),
    'pause': Command(name='pause', description=Strings.Description.pause, function=pause),
    'resume': Command(name='resume', description=Strings.Description.resume, function=resume),
    'stop': Command(name='stop', description=Strings.Description.stop, function=leave),
    'skip': Command(name='skip', description=Strings.Description.skip, function=skip),
    'queue': Command(name='queue', description=Strings.Description.queue, function=queue),
    'move': Command(name='move', description=Strings.Description.move, function=move),
    'remove': Command(name='remove', description=Strings.Description.remove, function=remove),
    'playlist': Command(name='playlist', description=Strings.Description.playlist, function=list_playlists),
    'playlist-create': Command(name='playlist-create', description=Strings.Description.playlist_create,
                               function=playlist_create),
    'playlist-delete': Command(name='playlist-delete', description=Strings.Description.playlist_delete,
                               function=playlist_delete),
    'playlist-add': Command(name='playlist-add', description=Strings.Description.playlist_add,
                            function=playlist_add),
    'playlist-remove': Command(name='playlist-remove',
                               description=Strings.Description.playlist_remove,
                               function=playlist_remove),
    'playlist-play': Command(name='playlist-play', description=Strings.Description.playlist_play,
                             function=playlist_play),
    'playlist-info': Command(name='playlist-info', description=Strings.Description.playlist_info,
                             function=playlist_info),
    'poll-force': Command(name='poll-force', description=Strings.Description.poll_force,
                          function=poll_force),
    'subscription-topics': Command(name='subscription-topics', description=Strings.Description.subscription_topics,
                                   function=list_topics),
    'subscribe': Command(name='subscribe', description=Strings.Description.subscribe,
                         function=subscribe),
    'unsubscribe': Command(name='unsubscribe', description=Strings.Description.unsubscribe,
                           function=unsubscribe),
    'subscriptions': Command(name='subscriptions', description=Strings.Description.subscriptions,
                             function=list_subscriptions)

}


async def run(name, args, context):
    command = commands[name]
    try:
        return await command.execute(args, context)
    except Exception as e:
        logger.error(f'Error executing command: {e}')
        return await send_message(context.channel, Strings.Error.generic)


async def run_join_or_leave(message, should_join) -> Message:
    voice_channel, voice_client = get_voice_channel_and_client(message)
    reply = await join_or_leave(voice_channel, voice_client, should_join=should_join)
    return await send_message(DiscordChannel(message.channel), reply)


def get_voice_channel_and_client(message):
    voice_channel = None if message.author.voice is None \
        else DiscordChannel(message.author.voice.channel)
    voice_client = None if message.guild.voice_client is None \
        else DiscordVoiceClient(message.guild.voice_client)
    return voice_channel, voice_client
