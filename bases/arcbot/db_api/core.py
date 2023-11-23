from flask import Flask, request
from pony.flask import Pony

from arcbot.repository import core as repository

app = Flask(__name__)
Pony(app)


@app.post('/playlist')
def save_playlist():
    name = request.json['name']
    user_id = request.json['user_id']
    guild_id = request.json['guild_id']
    playlist = repository.save_playlist(name, user_id, guild_id)
    if playlist is None:
        return '', 400
    return f'{{"name": "{playlist}"}}', 200


@app.post('/playlist/<playlist_name>/song')
def add_song(playlist_name: str):
    guild_id = request.json['guild_id']
    song_url = request.json['song_url']
    song_name = request.json['song_name']
    requesting_user_id = request.json['requesting_user_id']
    if not repository.add_song(guild_id, playlist_name, song_url, song_name, requesting_user_id):
        return '', 400
    return '', 200


@app.delete('/playlist/<playlist_name>')
def delete_playlist(playlist_name: str):
    guild_id = request.json['guild_id']
    requesting_user_id = request.json['requesting_user_id']
    playlist = repository.delete_playlist(guild_id, playlist_name, requesting_user_id)
    if playlist is None:
        return '', 400
    return f'{{"name": "{playlist}"}}', 200


@app.delete('/playlist/<playlist_name>/song')
def remove_song(playlist_name: str):
    guild_id = request.json['guild_id']
    song_url = request.json['song_url']
    song_name = request.json['song_name']
    requesting_user_id = request.json['requesting_user_id']
    if not repository.remove_song(guild_id, playlist_name, song_url, song_name, requesting_user_id):
        return '', 400
    return '', 200


@app.get('/playlist/<playlist_name>')
def get_playlist_by_name(playlist_name: str):
    guild_id = request.json['guild_id']
    playlist = repository.get_playlist_by_name(guild_id, playlist_name)
    if playlist is None:
        return '', 400
    return playlist.to_dict(), 200


@app.get('/playlist')
def get_playlists():
    guild_id = request.json['guild_id']
    playlists = repository.get_playlists(guild_id)
    return [playlist.to_dict() for playlist in playlists], 200


@app.post('/poll')
def save_poll():
    guild_id = request.json['guild_id']
    message_id = request.json['message_id']
    channel_id = request.json['channel_id']
    repository.save_poll(guild_id, message_id, channel_id)
    return '', 200


@app.put('/poll/<poll_id>')
def set_poll_winner(poll_id: int):
    playlist_name = request.json['winner_name']
    repository.set_poll_winner(poll_id, playlist_name)
    return '', 200


@app.get('/poll')
def get_polls():
    polls = repository.get_polls()
    return [poll.to_dict() for poll in polls], 200


@app.delete('/poll/<poll_id>')
def delete_poll(poll_id):
    repository.delete_poll(poll_id)
    return '', 200


@app.get('/poll/<guild_id>')
def get_poll(guild_id: str):
    poll = repository.get_poll(guild_id)
    if poll is None:
        return '', 400
    return poll.to_dict(), 200


@app.get('/topic')
def get_topics():
    topics = repository.get_topics()
    return [topic.to_dict() for topic in topics], 200


@app.get('/topic/<name>')
def get_topic_by_name(name: str):
    topic = repository.get_topic_by_name(name)
    if topic is None:
        return '', 400
    return topic.to_dict(), 200


@app.put('/topic/<topic_id>')
def update_topic_last_release_date(topic_id: int):
    last_release_date = request.json['last_release_date']
    repository.update_topic_last_release_date(topic_id, last_release_date)
    return '', 200


@app.get('/subscription/<user_id>/<topic_id>')
def get_subscription_by_user_id_and_topic_id(user_id: str, topic_id: int):
    subscription = repository.get_subscription_by_user_id_and_topic_id(user_id, topic_id)
    if subscription is None:
        return '', 400
    return subscription.to_dict(), 200


@app.post('/subscription')
def save_subscription():
    user_id = request.json['user_id']
    topic_id = request.json['topic_id']
    guild_id = request.json['guild_id']
    repository.save_subscription(user_id, topic_id, guild_id)
    return '', 200


@app.get('/subscription/<user_id>')
def get_subscriptions_by_user_id(user_id: str):
    subscriptions = repository.get_subscriptions_by_user_id(user_id)
    subscriptions = [subscription.to_dict(related_objects=True) for subscription in subscriptions]
    for subscription in subscriptions:
        subscription['topic'] = subscription['topic'].to_dict()
    return subscriptions, 200


@app.delete('/subscription/<subscription_id>')
def delete_subscription(subscription_id: int):
    repository.delete_subscription(subscription_id)
    return '', 200
