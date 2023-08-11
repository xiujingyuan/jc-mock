from datetime import datetime, timedelta
from functools import wraps

import jwt
from flask import current_app, request


def generate_access_token(username, algorithm='HS256', exp=2):
    now = datetime.utcnow()
    exp_datetime = now + timedelta(hours=exp)
    access_payload = {
        'exp': exp_datetime,
        'flag': 0,
        'iat': now,
        'iss': 'leon',
        'username': username
    }
    access_token = jwt.encode(access_payload, current_app.config['JWT_CSRF_SECRET_KEY'], algorithm=algorithm)
    return access_token


def decode_auth_token(token):
    try:
        payload = jwt.decode(token, current_app.config["JWT_CSRF_SECRET_KEY"], algorithms='HS256')
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, jwt.InvalidSignatureError):
        return ''
    else:
        return payload


def identify(auth_header):

    if auth_header:
        payload = decode_auth_token(auth_header)
        if not payload:
            return False
        if 'username' in payload and 'flag' in payload:
            if payload['flag'] == 0:
                return payload['username']
            else:
                return False
    return False


def login_required(f):

    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization", default=None)
        if not token:
            return 'not Login', '403 Permission Denied'
        username = identify(token)
        if not username:
            return 'not Login', '403 Permission Denied'
        return f(*args, **kwargs)
    return wrapper
