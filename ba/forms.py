from ba import db
from ba.security import check_password_hash


async def validate_login_form(conn, form):

    username = form['username']
    password = form['password']


    if not username:
        return 'username is required'
    if not password:
        return 'password is required'

    user = await db.get_user_by_name(conn, username)
    if not user:
        print('Invalid username')
        return 'Invalid username'
    if not check_password_hash(password, user[2]):
        print('Invalid password')
        return 'Invalid password'
    else:
        print('its ok')
        return None

    return 'error'