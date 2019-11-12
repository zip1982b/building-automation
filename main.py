import logging

import aiohttp_jinja2
import jinja2
from aiohttp import web

from ba.settings import get_config, BASE_DIR, config_path
from ba.routes import setup_routes
from ba.db import init_pg, close_pg
from ba.middlewares import setup_middlewares

from aiohttp_security import authorized_userid, SessionIdentityPolicy
from aiohttp_security import setup as setup_security
from aiohttp_session import setup as setup_session
from aiohttp_session.redis_storage import RedisStorage
import aioredis
from ba.db_auth import DBAuthorizationPolicy

log = logging.getLogger(__name__)



async def setup_redis(app):

    pool = await aioredis.create_redis_pool((app['config']['redis']['REDIS_HOST'], app['config']['redis']['REDIS_PORT']))

    async def close_redis(app):
        pool.close()
        await pool.wait_closed()

    app.on_cleanup.append(close_redis)
    app['redis_pool'] = pool
    return pool









async def current_user_ctx_processor(request):
    username = await authorized_userid(request)
    is_anonymous = not bool(username)
    return {'current_user': {'is_anonymous': is_anonymous}}


async def init_app(config):
    app = web.Application()
    app['config'] = config
    setup_routes(app)
    setup_middlewares(app)

    app.on_startup.append(init_pg)
    app.on_cleanup.append(close_pg)
    #db_pool = await init_db(app)

    redis_pool = await setup_redis(app)
    setup_session(app, RedisStorage(redis_pool))

    # needs to be after session setup because of `current_user_ctx_processor`
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(str(BASE_DIR / 'ba' / 'templates')),
        context_processors=[current_user_ctx_processor],
    )

    setup_security(app, SessionIdentityPolicy(), DBAuthorizationPolicy(app))

    log.debug(app['config'])

    return app

def main(configpath):
    config = get_config(configpath)
    logging.basicConfig(level=logging.DEBUG)
    app = init_app(config)
    web.run_app(app)


if __name__ == '__main__':
        main(config_path)
