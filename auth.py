from typing import Optional, Dict
from settings import *
from flask import Request, Response
from models import *


sessions: Dict[str, 'Session'] = {}


class Session(object):
    id: str
    user: User
    expire_after: float
    data: dict

    def __init__(self, user: User, max_age: float = 72000):
        from time import time
        from uuid import uuid4
        self.id = uuid4().hex
        self.user = user
        self.expire_after = time() + max_age
        self.data = {}

    @property
    def is_expired(self):
        from time import time
        return time() > self.expire_after


def encode_password(password: str) -> str:
    import hashlib
    import base64
    data: bytes = base64.b64encode(hashlib.sha1(password.encode()).digest())
    data = base64.b64encode(hashlib.sha1(data + secret.encode()).digest())
    return data.decode()


def authenticate(email: str, password: str) -> Optional[User]:
    password = encode_password(password)
    cursor = db.cursor()
    cursor.execute('select * from users where email = ? and password = ?', [email, password])
    data = cursor.fetchone()
    if data is None:
        return None
    else:
        return User(data)


def login(response: Response, user: User):
    session = Session(user)
    sessions[session.id] = session
    response.set_cookie('session', session.id, expires=session.expire_after)


def logout(request: Request, response: Response):
    response.delete_cookie('session')
    session = request.cookies.get('session', None)
    if session is not None:
        del sessions[session]


def get_session(request: Request) -> Optional[Session]:
    sid = request.cookies.get('session', None)
    if sid is None:
        return None

    session = sessions.get(sid, None)
    if session is None:
        return None

    if session.is_expired:
        del sessions[session.id]
        return None

    return session


def is_authenticated(request: Request):
    return get_session(request) is not None
