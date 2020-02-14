import json
from jose import jwt
from flask import request
from functools import wraps
from urllib.request import urlopen

AUTH0_DOMAIN = 'lihr.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'api-coffee-shop'

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

    def to_dict(self):
        rv = dict(())
        rv['status_code'] = self.status_code
        rv['message'] = self.error['code']
        return rv


# Auth Header
def get_token_auth_header():
    authorization = request.headers.get("Authorization")
    if not authorization:
        raise AuthError(
            {
                'code': 'no_header',
                'description': 'There is no authoriztion header.'
            }, 401)
    token = authorization[7:]
    return token


def check_permissions(permission, payload):
    permissions = payload['permissions']
    if permission in permissions:
        return True
    else:
        raise AuthError(
            {
                'code': 'no_permission',
                'description': 'This action has no perssion.'
            }, 401)


def verify_decode_jwt(token):
    print(token)
    # GET KEY DATA FROM AUTH0
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    # GET THE DATA IN THE HEADER
    unverified_header = jwt.get_unverified_header(token)

    # CHOOSE OUR KEY
    rsa_key = {}
    # VERIFY TOKEN HEADER IS VALID OR NOT
    if 'kid' not in unverified_header:
        raise AuthError(
            {
                'code': 'invalid_header',
                'description': 'Authorization malformed.'
            }, 401)

    # VERIFY DECODED HEADER AND MAKE RSA KEY
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            # USE THE KEY TO VALIDATE THE JWT AND GET PAYLOAD
            payload = jwt.decode(token,
                                 rsa_key,
                                 algorithms=ALGORITHMS,
                                 audience=API_AUDIENCE,
                                 issuer='https://' + AUTH0_DOMAIN + '/')

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError(
                {
                    'code': 'token_expired',
                    'description': 'Token expired.'
                }, 401)

        except jwt.JWTClaimsError:
            raise AuthError(
                {
                    'code':
                    'invalid_claims',
                    'description':
                    'Incorrect claims. Please, check the audience and issuer.'
                }, 401)
        except Exception:
            raise AuthError(
                {
                    'code': 'invalid_header',
                    'description': 'Unable to parse authentication token.'
                }, 400)
    raise AuthError(
        {
            'code': 'invalid_header',
            'description': 'Unable to find the appropriate key.'
        }, 400)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(*args, **kwargs)

        return wrapper

    return requires_auth_decorator
