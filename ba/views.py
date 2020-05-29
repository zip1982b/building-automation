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
        #cursor = await conn.execute(ba.db.users.select())
        #records = await cursor.fetchall()
        #users = [dict(q) for q in records]
        user = await ba.db.get_user_by_name(conn, username)
        return {'user': user}




@aiohttp_jinja2.template('light.html')
async def light(request):
    username = await authorized_userid(request)
    if not username:
        raise redirect(request.app.router, 'login')

    async with request.app['db'].acquire() as conn:
        user = await ba.db.get_user_by_name(conn, username)
        return {'user': user}


@aiohttp_jinja2.template('heating.html')
async def heating(request):
    username = await authorized_userid(request)
    if not username:
        raise redirect(request.app.router, 'login')

    async with request.app['db'].acquire() as conn:
        user = await ba.db.get_user_by_name(conn, username)
        return {'user': user}


@aiohttp_jinja2.template('ventilation.html')
async def ventilation(request):
    username = await authorized_userid(request)
    if not username:
        raise redirect(request.app.router, 'login')

    async with request.app['db'].acquire() as conn:
        user = await ba.db.get_user_by_name(conn, username)
        return {'user': user}


@aiohttp_jinja2.template('security.html')
async def security(request):
    username = await authorized_userid(request)
    if not username:
        raise redirect(request.app.router, 'login')

    async with request.app['db'].acquire() as conn:
        user = await ba.db.get_user_by_name(conn, username)
        return {'user': user}




@aiohttp_jinja2.template('login.html')
async def login(request):
    print(request)
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

                user = await ba.db.get_user_by_name(conn, form['username'])
                await remember(request, response, user[1])

                raise response

    return {}



async def logout(request):
    response = redirect(request.app.router, 'login')
    await forget(request, response)
    return response


