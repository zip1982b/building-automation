import aiopg.sa
from sqlalchemy import MetaData, Table, Column, ForeignKey, Integer, String


from sqlalchemy.sql import select


meta = MetaData()

users = Table(
    'users', meta,

    Column('id', Integer, primary_key=True),
    Column('name', String(50), nullable=False),
    Column('password_hash', String(128), nullable=False),
    Column('role', String(50), nullable=False)
)


async def init_pg(app):
    conf = app['config']['postgres']
    engine = await aiopg.sa.create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize'],
    )
    app['db'] = engine





async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()



async def get_user_by_name(conn, username):
    s = select([users])
    result = await conn.execute(s)
    async for row in result:
        print(row)
        if row[1] == username:
            print('username = user')
            return row
        else:
            return False


