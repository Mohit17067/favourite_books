import json

from flask import current_app, request, g
from werkzeug.wrappers import Response
from werkzeug.exceptions import HTTPException

from favourite_books.models import Client

from .utils import  decode_client_token, get_token_from_request

def check_auth(auth):
    un = current_app.config['BASIC_AUTH_USERNAME']
    pw = current_app.config['BASIC_AUTH_PASSWORD']
    return auth.username == un and auth.password == pw


def basic_auth(endpoint):

    auth = request.authorization
    if not auth or not check_auth(auth):
        resp = Response(
            response=json.dumps({'message': 'Not Authorized', 'error': True}),
            headers = {
                'WWW-Authenticate': 'Basic realm="Login Required"'
            },
            mimetype='application/json',
            status=401
        )
        raise HTTPException('Api Error', response=resp)

def get_api_client_from_request(endpoint):
    api_key = request.args.get('api_key', None)
    if not api_key:
        payload = {'message': 'Missing required ?api_key param'}
        endpoint.return_error(422, payload=payload)

    client = Client.query.filter_by(client_id=api_key).one_or_none()
    if client is None:
        payload = {'message': 'API Client not found'}
        endpoint.return_error(404, payload=payload)

    g.api_client = client

def get_client_token(endpoint):
    token = get_token_from_request()
    if not token:
        payload = {'message': 'Request does not contain token'}
        endpoint.return_error(
            401,
            payload=payload
        )

    payload = decode_client_token(g.api_client, token)
    if not payload:
        payload = {'message': 'Invalid token'}
        endpoint.return_error(
            401,
            payload=payload,
        )
    
    g.token = payload