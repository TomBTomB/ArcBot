import os

from pony.orm import *
from dotenv import load_dotenv

load_dotenv()
db = Database()
db.bind(
    provider='postgres',
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("POSTGRES_DB"),
)


class Playlist(db.Entity):
    name = Required(str)
    songs = Required(StrArray)
    guild_id = Required(str)
    user_id = Required(str)
    composite_key(guild_id, name)


class Poll(db.Entity):
    guild_id = Required(str)
    message_id = Required(str)
    channel_id = Required(str)
    winner_name = Optional(str)


class Topic(db.Entity):
    name = Required(str)
    external_id = Required(str)
    subscriptions = Set('Subscription', lazy=False)
    last_release_date = Optional(str)


class Subscription(db.Entity):
    user_id = Required(str)
    guild_id = Required(str)
    topic = Required(Topic, lazy=False)
    composite_key(user_id, topic)


db.generate_mapping(create_tables=True)
# db.drop_all_tables(with_all_data=True)
# db.create_tables()

with db_session:
    Topic(name='Twenty Øne Piløts', external_id='3YQKmKGau1PzlVlkL1iodx', last_release_date='2023-04-21')
    Topic(name='Alec Benjamin', external_id='5IH6FPUwQTxPSXurCrcIov', last_release_date='2023-11-16')
    Topic(name='The Band CAMINO', external_id='6d4jrmreCmsenscuieJERc', last_release_date='2023-08-10')


def save_playlist(name: str, user_id: str, guild_id: str) -> str | None:
    name = name.replace(' ', '-')
    if Playlist.exists(name=name, guild_id=guild_id):
        return None
    Playlist(name=name, songs=[], guild_id=guild_id, user_id=user_id)
    return name


def add_song(guild_id: str, playlist_name: str, song_url: str, song_name: str, requesting_user_id: str) -> bool:
    playlist = Playlist.get(lambda p: p.name == playlist_name and p.guild_id == guild_id)
    if playlist is None or song_url in playlist.songs or playlist.user_id != requesting_user_id:
        return False
    playlist.songs.append(song_url + ' ' + song_name)
    return True


def delete_playlist(guild_id: str, playlist_name: str, requesting_user_id: str) -> str | None:
    playlist = Playlist.get(lambda p: p.name == playlist_name and p.guild_id == guild_id)
    if playlist is None or playlist.user_id != requesting_user_id:
        return None
    playlist.delete()
    return playlist_name


def remove_song(guild_id: str, playlist_name: str, song_url: str, song_name: str, requesting_user_id: str) -> bool:
    playlist = Playlist.get(lambda p: p.name == playlist_name and p.guild_id == guild_id)
    if playlist is None or song_url + ' ' + song_name not in playlist.songs or playlist.user_id != requesting_user_id:
        return False
    playlist.songs.remove(song_url + ' ' + song_name)
    return True


def get_playlist_by_name(guild_id: str, playlist_name: str) -> Playlist | None:
    return Playlist.get(name=playlist_name, guild_id=guild_id)


def get_playlists(guild_id: str) -> list[Playlist]:
    return list(Playlist.select(lambda p: p.guild_id == guild_id))


def save_poll(guild_id: str, message_id: str, channel_id: str):
    if Poll.exists(lambda p: p.guild_id == guild_id):
        return
    Poll(guild_id=guild_id, message_id=message_id, channel_id=channel_id)


def set_poll_winner(poll_id: int, playlist_name: str):
    Poll[poll_id].winner_name = playlist_name


def get_polls():
    return list(Poll.select())


def delete_poll(poll_id):
    Poll[poll_id].delete()


def get_poll(guild_id: str) -> Poll | None:
    return Poll.get(guild_id=guild_id)


def get_topics():
    return list(Topic.select())


def get_topic_by_name(name: str) -> Topic | None:
    return Topic.get(name=name)


def update_topic_last_release_date(topic_id: int, last_release_date: str):
    Topic[topic_id].last_release_date = last_release_date


def get_subscription_by_user_id_and_topic_id(user_id: str, topic_id: int) -> Topic | None:
    return Subscription.get(user_id=user_id, topic=Topic[topic_id])


def save_subscription(user_id: str, topic_id: int, guild_id: str):
    Subscription(user_id=user_id, topic=Topic[topic_id], guild_id=guild_id)


def get_subscriptions_by_user_id(user_id: str) -> list[Topic]:
    return list(Subscription.select(lambda s: s.user_id == user_id).prefetch(Topic))


def delete_subscription(subscription_id: int):
    Subscription[subscription_id].delete()
