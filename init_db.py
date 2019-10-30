import asyncio
import aiopg

from ba.settings import config
from ba.db import users


DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"
db_url = DSN.format(**config['postgres'])


async def create_tables():
    conn = await aiopg.connect(db_url)
    cur = await conn.cursor()
    await cur.execute("CREATE TABLE users (id serial PRIMARY KEY, name text, passwd text, role text)")
    res = cur.statusmessage
    print(res)
    conn.close()



async def insert_data():
    conn = await aiopg.connect(db_url)
    cur = await conn.cursor()
    await cur.execute("INSERT INTO users VALUES (2, 'test_user', '46025', 'user')")
    res = cur.statusmessage
    print(res)
    conn.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(insert_data())