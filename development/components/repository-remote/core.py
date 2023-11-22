import requests

from development.components.entity.core import *


class DotDict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


URL = 'http://localhost:5000/'


def save_playlist(name: str, user_id: str, guild_id: str) -> str | None:
    response = requests.post(URL + 'playlist', json={'name': name, 'user_id': user_id, 'guild_id': guild_id})
    if response.status_code == 200:
        return response.json()['name']
    return None


def add_song(guild_id: str, playlist_name: str, song_url: str, song_name: str, requesting_user_id: str) -> bool:
    response = requests.post(URL + 'playlist/' + playlist_name + '/song',
                             json={'guild_id': guild_id, 'song_url': song_url, 'song_name': song_name,
                                   'requesting_user_id': requesting_user_id})
    return response.status_code == 200


def delete_playlist(guild_id: str, playlist_name: str, requesting_user_id: str) -> str | None:
    response = requests.delete(URL + 'playlist/' + playlist_name,
                               json={'guild_id': guild_id, 'requesting_user_id': requesting_user_id})
    if response.status_code == 200:
        return response.json()['name']
    return None


def remove_song(guild_id: str, playlist_name: str, song_url: str, song_name: str, requesting_user_id: str) -> bool:
    response = requests.delete(URL + 'playlist/' + playlist_name + '/song',
                               json={'guild_id': guild_id, 'song_url': song_url, 'song_name': song_name,
                                     'requesting_user_id': requesting_user_id})
    return response.status_code == 200


def get_playlist_by_name(guild_id: str, playlist_name: str) -> Playlist | None:
    response = requests.get(URL + 'playlist/' + playlist_name, json={'guild_id': guild_id})
    if response.status_code == 200:
        return DotDict(response.json())
    return None


def get_playlists(guild_id: str) -> list[Playlist]:
    response = requests.get(URL + 'playlist', json={'guild_id': guild_id})
    if response.status_code == 200:
        return [DotDict(playlist) for playlist in response.json()]
    return []


def save_poll(guild_id: str, message_id: str, channel_id: str):
    requests.post(URL + 'poll', json={'guild_id': guild_id, 'message_id': message_id, 'channel_id': channel_id})


def set_poll_winner(poll_id: int, playlist_name: str):
    requests.put(URL + 'poll/' + str(poll_id), json={'winner_name': playlist_name})


def get_polls():
    response = requests.get(URL + 'poll')
    if response.status_code == 200:
        return [DotDict(poll) for poll in response.json()]
    return []


def delete_poll(poll_id):
    requests.delete(URL + 'poll/' + str(poll_id))


def get_poll(guild_id: str) -> Poll | None:
    response = requests.get(URL + 'poll/' + guild_id)
    if response.status_code == 200:
        return DotDict(response.json())
    return None


def get_topics():
    response = requests.get(URL + 'topic')
    if response.status_code == 200:
        return [DotDict(topic) for topic in response.json()]
    return []


def get_topic_by_name(name: str) -> Topic | None:
    response = requests.get(URL + 'topic/' + name)
    if response.status_code == 200:
        return DotDict(response.json())
    return None


def update_topic_last_release_date(topic_id: int, last_release_date: str):
    requests.put(URL + 'topic/' + str(topic_id), json={'last_release_date': last_release_date})


def get_subscription_by_user_id_and_topic_id(user_id: str, topic_id: int) -> Topic | None:
    response = requests.get(URL + 'subscription/' + user_id + '/' + str(topic_id))
    if response.status_code == 200:
        return DotDict(response.json())
    return None


def save_subscription(user_id: str, topic_id: int, guild_id: str):
    requests.post(URL + 'subscription', json={'user_id': user_id, 'topic_id': topic_id, 'guild_id': guild_id})


def get_subscriptions_by_user_id(user_id: str) -> list[Topic]:
    response = requests.get(URL + 'subscription/' + user_id)
    if response.status_code == 200:
        subscriptions = [DotDict(subscription) for subscription in response.json()]
        for subscription in subscriptions:
            subscription.topic = DotDict(subscription.topic)
        return subscriptions
    return []


def delete_subscription(subscription_id: int):
    requests.delete(URL + 'subscription/' + str(subscription_id))
