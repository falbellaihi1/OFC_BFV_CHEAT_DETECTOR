import http.client
import mimetypes
import http.client
import mimetypes

import flask
from flask import request, abort


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

# # Auth Header
# def get_token_auth_header():
#     if 'Authorization' not in request.headers:
#         raise AuthError({
#             'code': 'autorization_header_messing',
#             'description': 'Authorization header is expected.'
#         }, 401)
#     auth_headers = request.headers['Authorization']
#     header_parts = auth_headers.split(' ')
#     if len(header_parts) != 2:
#         raise AuthError({
#             'code': 'invalid_header',
#             'description': 'Auth header must be bearer token.'
#         }, 401)
#     if len(header_parts) > 2:
#         raise AuthError({
#             'code': 'invalid_header',
#             'description': 'Token not found.'
#         }, 401)
#     if header_parts[0].lower() != 'bearer':
#         raise AuthError({
#             'code': 'invalid_header',
#             'description': 'Authorization header must start withh "Bearer".'
#         }, 401)
#     return header_parts[1]




def get_headers():
    headers = flask.request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1]
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
    }

    return headers