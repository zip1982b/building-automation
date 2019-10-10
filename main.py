from aiohttp import web
from ba.settings import config

from ba.routes import setup_routes


app = web.Application()
setup_routes(app)
app['config'] = config
web.run_app(app)





