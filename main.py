import aiohttp_jinja2
import jinja2
from aiohttp import web

from ba.settings import config, BASE_DIR
from ba.routes import setup_routes
from ba.db import init_pg, close_pg
from ba.middlewares import setup_middlewares

app = web.Application()
app['config'] = config
aiohttp_jinja2.setup(app,
    loader=jinja2.FileSystemLoader(str(BASE_DIR / 'ba' / 'templates')))
setup_routes(app)
setup_middlewares(app)



app.on_startup.append(init_pg)
app.on_cleanup.append(close_pg)

web.run_app(app)





