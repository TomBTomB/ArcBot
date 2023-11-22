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


class Topic(db.Entity):
    name = Required(str)
    external_id = Required(str)
    subscriptions = Set('Subscription', lazy=False)
    last_release_date = Optional(str)


class Subscription(db.Entity):
    user_id = Required(str)
    guild_id = Required(str)
    topic = Required(Topic, lazy=False)
    composite_key(user_id, topic)


db.generate_mapping(create_tables=False)
# db.drop_all_tables(with_all_data=True)
# db.create_tables()
#
# with db_session:
#     Topic(name='Twenty Øne Piløts', external_id='3YQKmKGau1PzlVlkL1iodx', last_release_date='2023-04-21')
#     Topic(name='Alec Benjamin', external_id='5IH6FPUwQTxPSXurCrcIov', last_release_date='2023-11-16')
#     Topic(name='The Band CAMINO', external_id='6d4jrmreCmsenscuieJERc', last_release_date='2023-08-10')
