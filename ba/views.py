# aiohttpdemo_polls/views.py
import aiohttp_jinja2
from aiohttp import web
import ba.db
from aiohttp_security import remember, forget, authorized_userid
from ba.forms import validate_login_form


def redirect(router, route_name):
    location = router[route_name].url_for()
    return web.HTTPFound(location)

@aiohttp_jinja2.template('index.html')
async def index(request):
    username = await authorized_userid(request)
    if not username:
        raise redirect(request.app.router, 'login')

    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(ba.db.users.select())
        records = await cursor.fetchall()
        users = [dict(q) for q in records]
        return {'users': users}


@aiohttp_jinja2.template('login.html')
async def login(request):
    username = await authorized_userid(request)
    if username:
        raise redirect(request.app.router, 'index')

    if request.method == 'POST':
        form = await request.post()

        async with request.app['db'].acquire() as conn:
            error = await validate_login_form(conn, form)

            if error:
                return {'error': error}
            else:
                response = redirect(request.app.router, 'index')

                async with request.app['db'].acquire() as conn:
                    cursor = await conn.execute(ba.db.users.select())
                    records = await cursor.fetchall()
                    users = [dict(q) for q in records]
                    print(users)

                if form['username'] == users:
                    await remember(request, response, users['username'])
                #user = await ba.db.get_user_by_name(conn, form['username'])
                await remember(request, response, user['username'])

                raise response

    return {}





"""
        data = await request.post()
        print(data)
        if(data):
            login = data['login']
            password = data['password']
            return {'login': login, 'password': password}

"""
