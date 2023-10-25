from pony.orm import *

from development.components.entity.core import Playlist, Poll, Topic, Subscription


@db_session
def save_playlist(name: str, user_id: str, guild_id: str) -> str | None:
    name = name.replace(' ', '-')
    if Playlist.exists(name=name, guild_id=guild_id):
        return None
    Playlist(name=name, songs=[], guild_id=guild_id, user_id=user_id)
    return name


@db_session
def add_song(guild_id: str, playlist_name: str, song_url: str, song_name: str, requesting_user_id: str) -> bool:
    playlist = Playlist.get(lambda p: p.name == playlist_name and p.guild_id == guild_id)
    if playlist is None or song_url in playlist.songs or playlist.user_id != requesting_user_id:
        return False
    playlist.songs.append(song_url + ' ' + song_name)
    return True


@db_session
def delete_playlist(guild_id: str, playlist_name: str, requesting_user_id: str) -> str | None:
    playlist = Playlist.get(lambda p: p.name == playlist_name and p.guild_id == guild_id)
    if playlist is None or playlist.user_id != requesting_user_id:
        return None
    playlist.delete()
    return playlist_name


@db_session
def remove_song(guild_id: str, playlist_name: str, song_url: str, song_name: str, requesting_user_id: str) -> bool:
    playlist = Playlist.get(lambda p: p.name == playlist_name and p.guild_id == guild_id)
    if playlist is None or song_url + ' ' + song_name not in playlist.songs or playlist.user_id != requesting_user_id:
        return False
    playlist.songs.remove(song_url + ' ' + song_name)
    return True


@db_session
def get_playlist_by_name(guild_id: str, playlist_name: str) -> Playlist | None:
    return Playlist.get(name=playlist_name, guild_id=guild_id)


@db_session
def get_playlists(guild_id: str) -> list[Playlist]:
    return list(Playlist.select(lambda p: p.guild_id == guild_id))


@db_session
def save_poll(guild_id: str, message_id: str, channel_id: str):
    if Poll.exists(lambda p: p.guild_id == guild_id):
        return
    Poll(guild_id=guild_id, message_id=message_id, channel_id=channel_id)


@db_session
def set_poll_winner(poll_id: int, playlist_name: str):
    Poll[poll_id].winner_name = playlist_name


@db_session
def get_polls():
    return list(Poll.select())


@db_session
def delete_poll(poll_id):
    Poll[poll_id].delete()


@db_session
def get_poll(guild_id: str) -> Poll | None:
    return Poll.get(guild_id=guild_id)


@db_session
def get_topics():
    return list(Topic.select())


@db_session
def get_topic_by_name(name: str) -> Topic | None:
    return Topic.get(name=name)


@db_session
def get_subscription_by_user_id_and_topic_id(user_id: str, topic_id: int) -> Topic | None:
    return Subscription.get(user_id=user_id, topic=Topic[topic_id])


@db_session
def save_subscription(user_id: str, topic_id: int):
    Subscription(user_id=user_id, topic=Topic[topic_id])


@db_session
def get_subscriptions_by_user_id(user_id: str) -> list[Topic]:
    return list(Subscription.select(lambda s: s.user_id == user_id).prefetch(Topic))


@db_session
def delete_subscription(subscription_id: int):
    Subscription[subscription_id].delete()
