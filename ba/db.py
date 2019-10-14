import aiopg.sa
from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, Date
)

meta = MetaData()

users = Table(
    'users', meta,

    Column('id', Integer, primary_key=True),
    Column('name', String(50), nullable=False),
    Column('passwd', String(50), nullable=False),
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


