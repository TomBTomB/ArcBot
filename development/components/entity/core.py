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


db.generate_mapping(create_tables=True)
# db.drop_all_tables(with_all_data=True)
# db.create_tables()
