# -*- coding: utf-8 -*-
import datetime

import pytest


def test_jwt_auth_by_username(jwt_api_client):
    pwd = 'example123'
    user = jwt_api_client.user_factory(username='test', password=pwd)
    jwt_api_client.jwt_login(user)
    data = jwt_api_client.post('/api/auth/',
                               {
                                   'username': user.username,
                                   'password': pwd
                               },
                               accept_code=200).json()
    assert data['token']



def test_jwt_token(jwt_api_client):
    jwt_api_client.jwt_login()
    token = jwt_api_client._token
    data = jwt_api_client.post('/api/verify/', {'token': token}, accept_code=200).json()
    assert data['token'] == token


def test_refresh_jwt_token(jwt_api_client, settings):
    settings.JWT_AUTH = {
        'JWT_ALLOW_REFRESH': True,
        'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
        'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=30),
    }

    jwt_api_client.jwt_login()
    token = jwt_api_client._token
    data = jwt_api_client.post('/api/refresh/', {'token': token}, accept_code=200).json()
    assert data['token']


