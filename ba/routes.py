import pathlib
from .views import index, login

PROJECT_ROOT = pathlib.Path(__file__).parent


def setup_routes(app):
    app.router.add_get('/', index, name='index')
    #app.router.add_get('/index', index)
    app.router.add_get('/login', login, name='login')
    app.router.add_post('/login', login, name='login')
    setup_static_routes(app)



def setup_static_routes(app):
    app.router.add_static('/static/',
                          path=PROJECT_ROOT / 'static',
                          name='static')