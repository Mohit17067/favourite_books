import jwt

from datetime import datetime, timedelta
from flask import request


def decode_client_token(client, token):

    verify_claims = ['sig', 'aud', 'exp', 'nbf', 'iat']
    required_claims = ['exp', 'iat', 'nbf', 'aud']

    options = {
        'verify_' + claim: True
        for claim in verify_claims
    }

    options.update({
        'require_' + claim: True
        for claim in required_claims
    })

    try:
        return jwt.decode(
            token,
            str(client.secret_key),
            options=options,
            algorithms=['HS256'],
            audience=str(client.id),
            leeway=0
        )
    except jwt.ExpiredSignatureError:
        msg = 'Signature has expired.'
        raise exceptions.AuthenticationFailed(msg)
        return False
    except jwt.InvalidTokenError:
        return False


def encode_client_token(client, user_id=None):
    iat = datetime.utcnow()
    exp = iat + timedelta(minutes=30)
    nbf = iat
    payload = {
        'exp': exp,
        'iat': iat,
        'nbf': nbf,
        'aud': str(client.id)
    }
    if user_id:
        payload['sub'] = user_id

    return jwt.encode(
        payload,
        str(client.secret_key),
        algorithm='HS256',
        headers=None
    ).decode('utf-8')


def get_token_from_request():

    auth_header_value = request.headers.get('Authorization', None)

    if not auth_header_value:
        return False

    parts = auth_header_value.split()

    if parts[0].lower() != 'bearer':
        return False
    elif len(parts) == 1:
        return False
    elif len(parts) > 2:
        return False

    return parts[1]