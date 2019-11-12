from aiohttp_security.abc import AbstractAuthorizationPolicy

from ba import db


class DBAuthorizationPolicy(AbstractAuthorizationPolicy):

    def __init__(self, app):
        self.req = app

    async def authorized_userid(self, identity):
        async with self.req['db'].acquire() as conn:
            user = await db.get_user_by_name(conn, identity)
            if user:
                return identity

        return None

    async def permits(self, identity, permission, context=None):
        if identity is None:
            return False
        return True