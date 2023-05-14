import discord.ext.test as dpytest
import pytest
import pytest_asyncio

from bases.arcbot.bot_client import core as bot_client
from components.arcbot.command.core import commands


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
