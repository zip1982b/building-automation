# aiohttpdemo_polls/views.py
import aiohttp_jinja2
from aiohttp import web
import ba.db


@aiohttp_jinja2.template('index.html')
async def index(request):
    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(ba.db.users.select())
        records = await cursor.fetchall()
        users = [dict(q) for q in records]
        return {'users': users}


@aiohttp_jinja2.template('login.html')
async def login(request):
        data = await request.post()
        print(data)
        if(data):
            login = data['login']
            password = data['password']
            return {'login': login, 'password': password}


