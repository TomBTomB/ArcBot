import discord.ext.test as dpytest
import pytest
import pytest_asyncio

from arcbot.bot_client import core as bot_client
from arcbot.command.core import commands


@pytest_asyncio.fixture
async def bot():
    b = bot_client.get_client()
    await b._async_setup_hook()
    dpytest.configure(b)
    return b


@pytest.mark.asyncio
async def test_ping(bot):
    await dpytest.message('$ping')
    assert dpytest.verify().message().content('Pong!')


@pytest.mark.asyncio
async def test_help(bot):
    await dpytest.message('$help')
    content = dpytest.get_message().content
    lines = content.split('\n')
    assert len(lines) == len(commands)


@pytest.mark.asyncio
async def test_help_with_argument(bot):
    # test sending the help command with an argument
    await dpytest.message('$help ping')
    assert dpytest.verify().message().content('ping: Pings the bot.')


@pytest.mark.asyncio
async def test_ping_with_argument(bot):
    # test sending the ping command with an argument
    await dpytest.message('$ping foo')
    assert dpytest.verify().message().content('Pong!')


@pytest.mark.asyncio
async def test_join_no_voice_channel(bot):
    # test sending the join command with no voice channel
    await dpytest.message('$join')
    assert dpytest.verify().message().content('It seems your are in the void.')


@pytest.mark.asyncio
async def test_leave_no_voice_client(bot):
    # test sending the leave command with no voice client
    await dpytest.message('$leave')
    assert dpytest.verify().message().content('I am not amongst you.')


@pytest.mark.asyncio
async def test_play_with_invalid_url(bot):
    # test sending the play command with an invalid URL
    await dpytest.message('$play https://www.example.com')
    assert dpytest.verify().message().content('Invalid URL.')


@pytest.mark.asyncio
async def test_help_with_invalid_argument(bot):
    # test sending the help command with an invalid argument
    await dpytest.message('$help foo')
    assert dpytest.verify().message().content('No such command: foo')


@pytest.mark.asyncio
async def test_ping_with_no_argument(bot):
    # test sending the ping command with no argument
    await dpytest.message('$ping')
    assert dpytest.verify().message().content('Pong!')


@pytest.mark.asyncio
async def test_join_with_voice_channel(bot):
    # test sending the join command with a voice channel
    await dpytest.member_join_voice(dpytest.get_config().guilds[0].channels[2])  # join a mock voice channel
    await dpytest.message('$join')
    assert dpytest.verify().message().content('Who disturbs my slumber?')


@pytest.mark.asyncio
async def test_leave_with_voice_client(bot):
    # test sending the leave command with a voice client
    await dpytest.member_join_voice(dpytest.get_config().guilds[0].channels[2])  # join a mock voice channel
    await dpytest.message('$join')  # join the same channel with the bot
    await dpytest.message('$leave')
    assert dpytest.verify().message().content('I have returned to the void from whence I came.')


@pytest.mark.asyncio
async def test_play_with_valid_url(bot):
    # test sending the play command with a valid URL
    await dpytest.member_join_voice(dpytest.get_config().guilds[0].channels[2])  # join a mock voice channel
    await dpytest.message('$join')  # join the same channel with the bot
    await dpytest.message('$play https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    assert dpytest.verify().message().content('Now playing: Rick Astley - Never Gonna Give You Up (Video)')
