from pony.orm import *

from development.components.entity.core import Playlist


@db_session
def save_playlist(name: str, user_id: str, guild_id: str) -> str | None:
    name = name.replace(' ', '-')
    if Playlist.exists(lambda p: p.name == name and p.guild_id == guild_id):
        return None
    Playlist(name=name, songs=[], guild_id=guild_id, user_id=user_id)
    return name


@db_session
def add_song(guild_id: str, playlist_name: str, song_url: str) -> bool:
    playlist = Playlist.get(lambda p: p.name == playlist_name and p.guild_id == guild_id)
    if playlist is None or song_url in playlist.songs:
        return False
    playlist.songs.append(song_url)
    return True
