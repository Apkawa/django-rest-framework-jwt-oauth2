# -*- coding: utf-8 -*-
from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin
from rest_framework.request import Request
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.middleware import get_user
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.exceptions import AuthenticationFailed


def get_user_jwt(request):
    """
    Приоритет, если есть пользователь в JWT - вытаскиваем его.
    :param request:
    :return:
    """
    auth = JSONWebTokenAuthentication()
    try:
        jwt_value = auth.get_jwt_value(request)
        if jwt_value:
            user_jwt = auth.authenticate(Request(request))
            if user_jwt is not None:
                return user_jwt[0]
    except AuthenticationFailed:
        # Тут был jwt токен
        return AnonymousUser()

    user = get_user(request)
    if user.is_authenticated():
        return user
    return AnonymousUser()


class AuthenticationMiddlewareJWT(MiddlewareMixin):
    def process_request(self, request):
        request.user = SimpleLazyObject(lambda: get_user_jwt(request))
