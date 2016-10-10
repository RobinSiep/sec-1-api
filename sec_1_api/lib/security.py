import bcrypt
from pyramid.httpexceptions import HTTPBadRequest


def hash_password(password):
    salt = bcrypt.gensalt()
    return (bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8'),
            salt.decode('utf-8'))


def check_password(password, hashed_password=None, salt=None):
    """
    Checks the password against the hashed bytes of the user. Even if
    the user is not found we hash the password with a generated hash. This
    is to prevent an attacker from differentiating between a password and
    a username error.
    """

    if not salt:
        salt = bcrypt.gensalt().decode('utf-8')

    new_hashed_password = bcrypt.hashpw(password.encode('utf-8'),
                                        salt.encode('utf-8'))

    try:
        if not new_hashed_password == hashed_password.encode('utf-8'):
            raise HTTPBadRequest(
                json={"message": "Username or password incorrect"})
    except AttributeError:
        # This means the user isn't found. We don't care because this should
        # throw the same exception as a wrong password.
        pass
