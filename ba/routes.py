import pathlib
from .views import index, light, heating, ventilation, security, login, logout

PROJECT_ROOT = pathlib.Path(__file__).parent


def setup_routes(app):
    app.router.add_get('/', index, name='index')
    app.router.add_get('/light', light, name='light')
    app.router.add_get('/heating', heating, name='heating')
    app.router.add_get('/ventilation', ventilation, name='ventilation')
    app.router.add_get('/security', security, name='security')
    app.router.add_get('/login', login, name='login')
    app.router.add_post('/login', login, name='login')
    app.router.add_get('/logout', logout, name='logout')
    setup_static_routes(app)



def setup_static_routes(app):
    app.router.add_static('/static/',
                          path=PROJECT_ROOT / 'static',
                          name='static')