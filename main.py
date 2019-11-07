import aiohttp_jinja2
import jinja2
from aiohttp import web

from ba.settings import config, BASE_DIR
from ba.routes import setup_routes
from ba.db import init_pg, close_pg
from ba.middlewares import setup_middlewares

from aiohttp_security import authorized_userid, SessionIdentityPolicy
from aiohttp_security import setup as setup_security
from aiohttp_session import setup as setup_session
from aiohttp_session.redis_storage import RedisStorage
import aioredis
from ba.db_auth import DBAuthorizationPolicy

async def setup_redis(app):

    pool = await aioredis.create_redis_pool((
        app['config']['redis']['REDIS_HOST'],
        app['config']['redis']['REDIS_PORT']
    ))

    async def close_redis(app):
        pool.close()
        await pool.wait_closed()

    app.on_cleanup.append(close_redis)
    app['redis_pool'] = pool
    return pool







app = web.Application()
app['config'] = config
aiohttp_jinja2.setup(app,
    loader=jinja2.FileSystemLoader(str(BASE_DIR / 'ba' / 'templates')))
setup_routes(app)
setup_middlewares(app)







app.on_startup.append(init_pg)
app.on_cleanup.append(close_pg)

redis_pool = setup_redis(app)
setup_session(app, RedisStorage(redis_pool))

setup_security(
        app,
        SessionIdentityPolicy(),
        DBAuthorizationPolicy(app['db'])
    )








web.run_app(app)





