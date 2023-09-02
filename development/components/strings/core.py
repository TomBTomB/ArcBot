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

    class Description:
        help = 'Shows every possible command.'
        ping = 'Pings the bot.'
        join = 'Joins the voice channel you are in.'
        leave = 'Leaves the voice channel you are in.'
        play = 'Plays the requested song.'
