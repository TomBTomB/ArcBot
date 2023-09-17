class Strings:
    class Action:
        user_not_connected = 'It seems you are in the void.'
        bot_not_connected = 'I am not amongst you.'
        bot_already_connected = 'I am already amongst you.'
        bot_connected = 'Who disturbs my slumber?'
        bot_disconnected = 'I have returned to the void from whence I came.'
        bot_moved = 'Whomst has summoned the almighty one?'

        @staticmethod
        def now_playing(file_name): return f'Now playing: `{file_name}`'

        @staticmethod
        def song_added_to_queue(song): return f'Added `{song}` to queue.'

        @staticmethod
        def song_moved(moved_song, to): return f'Moved `{moved_song}` to position `{to}`.'

        @staticmethod
        def song_removed(removed_song): return f'Removed `{removed_song}` from queue.'

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

    class Queue:
        empty = 'The Queue is empty.'

    class Error:
        generic = 'Something went wrong.'
        invalid_move = 'Invalid move operation.'
        invalid_remove = 'Invalid remove operation.'
