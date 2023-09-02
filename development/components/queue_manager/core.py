queue: dict[int, list[(str, str)]] = {}


def add_song(guild_id: int, file_name: str, url: str):
    if guild_id not in queue:
        queue[guild_id] = []
    queue[guild_id].append((file_name, url))


def get_next_song(guild_id: int) -> (str, str):
    if guild_id not in queue:
        return None, None
    return queue[guild_id].pop(0)


def remove_song(guild_id: int, song: str):
    if guild_id not in queue:
        return
    queue[guild_id].remove(song)


def move_song(guild_id: int, index_from: int, index_to: int):
    if guild_id not in queue:
        return
    if index_from < 0 or index_from >= len(queue[guild_id]) or index_to < 0 or index_to >= len(queue[guild_id]):
        return
    queue[guild_id].insert(index_to, queue[guild_id].pop(index_from))


def clear_queue(guild_id: int):
    if guild_id not in queue:
        return
    queue[guild_id].clear()


def get_queue_song_names(guild_id: int) -> list[str]:
    if guild_id not in queue:
        return []
    return [song[0] for song in queue[guild_id]]
