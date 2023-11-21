class Strings:
    class Action:
        user_not_connected = 'It seems you are in the void.'
        bot_not_connected = 'I am not amongst you.'
        bot_already_connected = 'I am already amongst you.'
        bot_connected = 'Who disturbs my slumber?'
        bot_disconnected = 'I have returned to the void from whence I came.'
        bot_moved = 'Whomst has summoned the almighty one?'
        pause = 'Someone stopped the party.'
        resume = 'The party goes on.'
        skipped = "Hey! I was listening to that..."

        @staticmethod
        def now_playing(file_name): return f'Now playing: `{file_name}`'

        @staticmethod
        def song_added_to_queue(song): return f'Added `{song}` to queue.'

        @staticmethod
        def song_moved(moved_song, to): return f'Moved `{moved_song}` to position `{to}`.'

        @staticmethod
        def song_removed(removed_song): return f'Removed `{removed_song}` from queue.'

        @staticmethod
        def playlist_created(response): return f'Created playlist `{response}`.'

        @staticmethod
        def song_added_to_playlist(file_name,
                                   playlist_name): return f'Added `{file_name}` to playlist `{playlist_name}`.'

        @staticmethod
        def playlist_deleted(playlist_name): return f'Deleted playlist `{playlist_name}`.'

        @staticmethod
        def song_removed_from_playlist(file_name,
                                       playlist_name): return f'Removed `{file_name}` from playlist `{playlist_name}`.'

        @staticmethod
        def poll_forced(playlist_name, admin_id):
            return f'Poll ended. Playlist `{playlist_name}` was forced to win by <@{admin_id}>.'

        @staticmethod
        def subscribed(user_id, topic_name):
            return f'User <@{user_id}> subscribed to {topic_name}.'

        @staticmethod
        def unsubscribed(user_id, topic_name):
            return f'User <@{user_id}> unsubscribed from {topic_name}.'

    class Description:
        help = 'Shows every possible command.'
        ping = 'Pings the bot.'
        join = 'Joins the voice channel you are in.'
        leave = 'Leaves the voice channel you are in.'
        play = 'Plays the requested song.'
        pause = 'Pauses the current song.'
        resume = 'Resumes the current song.'
        stop = 'Stops the current song.'
        skip = 'Skips the current song.'
        queue = 'Shows the current queue.'
        move = 'Moves a song to a different position in the queue.'
        remove = 'Removes a song from the queue.'
        playlist = 'Lists all available playlist for the guild.'
        playlist_create = 'Creates a playlist with the given name.'
        playlist_add = 'Adds a song to a playlist. Usage: `playlist-add <playlist_name> <song>`'
        playlist_delete = 'Deletes a playlist with the given name.'
        playlist_remove = 'Removes a song from a playlist. Usage: `playlist-remove <playlist_name> <song>`'
        playlist_play = 'Plays a playlist with the given name.'
        playlist_info = 'Lists the songs in the playlist with the given name. Usage: `playlist-info <playlist_name>`'
        poll_force = 'Forces poll to end and a playlist to win.'
        subscribe = 'Subscribes you to a topic.'
        subscription_topics = 'Lists all available subscription topics.'
        subscriptions = 'Lists all your subscriptions.'

    class Queue:
        empty = 'The Queue is empty.'

    class Error:
        admin_only = 'Only admins can do that.'
        generic = 'Something went wrong.'
        invalid_move = 'Invalid move operation.'
        invalid_remove = 'Invalid remove operation.'
        no_playlists = 'There are no playlists, to create one run the command `playlist-create`.'
        no_topics = 'Currently there are no topics available.'
        topic_not_found = 'Topic does not exist.'
        already_subscribed = 'You are already subscribed to that topic.'
        not_subscribed = 'You are not subscribed to that topic.'
        no_subscriptions = 'You are not subscribed to any topics.'
        creating_playlist = 'There was an error creating the playlist.'
        adding_to_playlist = ('There was an error adding the song to the playlist. Check if the playlist with that '
                              'name exists.')
        deleting_playlist = 'There was an error deleting the playlist. Check if the playlist with that name exists.'
        removing_from_playlist = 'There was an error removing the song from the playlist.'
        playlist_not_found = 'Playlist does not exist or is empty.'
        poll_not_found = 'There is no poll running.'
