# aiohttpdemo_polls/views.py
from aiohttp import web

async def index(request):
    return web.Response(text='Hello, i am a Aiohttp server!')