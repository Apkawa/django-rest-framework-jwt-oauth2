# -*- coding: utf-8 -*-
import json

import pytest
import six
from django.contrib.auth.models import User
from django.test.client import Client, MULTIPART_CONTENT
from django.urls import reverse, NoReverseMatch
from django.utils.encoding import smart_text, smart_str
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler, \
    jwt_decode_handler


def default_user_factory(**kwargs):
    pwd = kwargs.pop('password', None)
    kwargs.setdefault('username', 'example')
    user = User.objects.get_or_create(**kwargs)[0]
    if pwd:
        user.set_password(pwd)
        user.save()
    return user


class JWTApiTestClient(Client):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('HTTP_HOST', 'localhost')
        self.user_factory = kwargs.pop('user_factory', default_user_factory)
        super(JWTApiTestClient, self).__init__(*args, **kwargs)
        self.frontend_site = None
        self.user = None

    @property
    def host(self):
        return self.defaults['HTTP_HOST']

    def _base_environ(self, **request):
        env = super(JWTApiTestClient, self)._base_environ(**request)
        if env.get('force_https'):
            env['wsgi.url_scheme'] = 'https'
        return env

    def post(self, path, data=None, content_type=None,
             secure=False, **extra):
        "Construct a POST request."
        # Maybe create
        extra.setdefault('accept_code', 201)
        data = {} if data is None else data
        content_type = content_type or 'application/json'

        return self.generic('POST', path, data, content_type,
                            secure=secure, **extra)

    def put(self, path, data='', content_type=None,
            secure=False, **extra):
        """ Construct a PUT request. """
        return self.generic('PUT', path, data, content_type,
                            secure=secure, **extra)

    def patch(self, path, data='', content_type=None,
              secure=False, **extra):
        """ Construct a PATCH request. """
        return self.generic('PATCH', path, data, content_type,
                            secure=secure, **extra)

    def delete(self, path, data='', content_type=None,
               secure=False, **extra):
        """ Construct a DELETE request. """
        extra.setdefault('accept_code', 204)
        return self.generic('DELETE', path, data, content_type,
                            secure=secure, **extra)

    def generic(self, method, path, data='',
                content_type=None, secure=False,
                **extra):

        "Try get by name"
        try:
            path = reverse(path, kwargs=extra.pop('kwargs', None))
        except NoReverseMatch:
            pass
        content_type = content_type or 'application/json'

        if method in ['POST', 'PUT', 'PATCH']:
            if (content_type == 'application/json'
                and not isinstance(data, (six.text_type, six.binary_type))
            ):
                data = json.dumps(data)

            if content_type.startswith('multipart/form-data'):
                content_type = MULTIPART_CONTENT

        data = self._encode_data(data, content_type)

        return super(JWTApiTestClient, self).generic(method, path, data, content_type, secure,
                                                     **extra)

    def request(self, **request):
        assert_code = request.pop('accept_code', 200)
        update_token = request.pop('update_token', False)
        response = super(JWTApiTestClient, self).request(**request)
        if assert_code:
            assert assert_code == response.status_code, smart_text(response.content)
        response.json = lambda: json.loads(smart_str(response.content))
        response.token = lambda: response.get('Access-Token')
        if update_token and response.token():
            self.set_jwt_token(response.token())
        return response

    def get_jwt_token(self, user=None, **extra_data):
        payload = jwt_payload_handler(user)
        return jwt_encode_handler(payload)

    def jwt_login(self, user=None):
        if not user:
            user = self.user_factory()
        if getattr(self, '_token', None):
            payload = jwt_decode_handler(self._token)
        else:
            payload = {}
        self.set_jwt_token(self.get_jwt_token(user, **payload))
        self.user = user
        return user

    def set_jwt_token(self, token):
        self._token = token
        self.defaults['HTTP_AUTHORIZATION'] = 'JWT ' + self._token

    def delete_jwt_token(self):
        self._token = None
        del self.defaults['HTTP_AUTHORIZATION']

    def jwt_logout(self):
        self.delete_jwt_token()


@pytest.fixture(scope='function')
def jwt_api_client_user_factory():
    return default_user_factory


@pytest.fixture(scope='function')
def jwt_api_client_kwargs(jwt_api_client_user_factory):
    return {
        'HTTP_HOST': 'localhost',
        'user_factory': jwt_api_client_user_factory,

    }


@pytest.fixture(scope='function')
def jwt_api_client(jwt_api_client_kwargs, settings):
    """A Django test client instance."""

    client = JWTApiTestClient(**jwt_api_client_kwargs)
    settings.ALLOWED_HOSTS.append(client.host)
    return client
