# -*- coding: utf-8 -*-
from datetime import datetime

from six.moves.urllib.parse import urlencode

from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.serializers import (
    VerificationBaseSerializer, JSONWebTokenSerializer,
    VerifyJSONWebTokenSerializer, RefreshJSONWebTokenSerializer
)
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import (
    JSONWebTokenAPIView as _JSONWebTokenAPIView,
    jwt_response_payload_handler
)

from rest_framework_jwt_oauth2.utils.serializers import serializer_factory
from . import app_settings
from .serializers import OAuth2JSONWebTokenSerializer


class JSONWebTokenAPIView(_JSONWebTokenAPIView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = serializer.object.get('user') or request.user
        token = serializer.object.get('token')
        response_data = jwt_response_payload_handler(token, user, request)
        response = Response(response_data)
        if api_settings.JWT_AUTH_COOKIE:
            expiration = datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
            response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                token,
                                expires=expiration,
                                httponly=True)
        return response


@method_decorator(name='get', decorator=swagger_auto_schema(
    query_serializer=serializer_factory('QueryParams',
                                        redirect_uri=serializers.CharField(
                                            label="Ссылка для редиректа",
                                            help_text="При успешной авторизации. "
                                                      "Например ratelook://complete",
                                            required=False,
                                        )),
    responses={
        200: serializer_factory('Response',
                                url=serializers.URLField(help_text="Ссылка на начало авторизации"))
    }))
class OAuth2InitialView(APIView):
    """
    Получение ссылки для начала авторизации по oauth2
    """

    def get(self, request, **kwargs):
        provider_name = kwargs.get('provider')
        redirect_uri = request.query_params.get('redirect_uri')

        if not redirect_uri:
            redirect_uri = app_settings.DEFAULT_REDIRECT_URL
            if callable(redirect_uri):
                redirect_uri = redirect_uri(request, provider_name)
            redirect_uri = request.build_absolute_uri(redirect_uri.format(provider=provider_name))

        extra_params = {
            "response_type": "code",
        }

        # TODO action add social to user
        # action = kwargs.get('action', AuthAction.AUTHENTICATE)

        auth_params = dict(filter(lambda v: v[1], dict(
            redirect_uri=redirect_uri,
            **extra_params
        ).items()))

        qs = ''
        if auth_params:
            qs = urlencode({'auth_params': urlencode(auth_params)})

        auth_url = app_settings.DEFAULT_AUTH_URL
        if callable(redirect_uri):
            auth_url = redirect_uri(request, provider_name)
        auth_url = request.build_absolute_uri(auth_url.format(provider=provider_name, qs=qs))

        return Response({'url': auth_url})


@method_decorator(name='post', decorator=swagger_auto_schema(
    responses={200: VerificationBaseSerializer()}))
class OAuth2LoginView(JSONWebTokenAPIView):
    """
    Окончание авторизации, возвращает JWT token
    """
    serializer_class = OAuth2JSONWebTokenSerializer


@method_decorator(name='post', decorator=swagger_auto_schema(
    responses={200: VerificationBaseSerializer()}
))
class ObtainJSONWebToken(JSONWebTokenAPIView):
    """
    Авторизация используя username и password.

    """
    serializer_class = JSONWebTokenSerializer


@method_decorator(name='post', decorator=swagger_auto_schema(
    responses={200: VerificationBaseSerializer()}
))
class VerifyJSONWebToken(JSONWebTokenAPIView):
    """
    Проверка токена
    """
    serializer_class = VerifyJSONWebTokenSerializer


@method_decorator(name='post', decorator=swagger_auto_schema(
    responses={200: VerificationBaseSerializer()}
))
class RefreshJSONWebToken(JSONWebTokenAPIView):
    """
    Обновление токена
    """
    serializer_class = RefreshJSONWebTokenSerializer


obtain_jwt_token = ObtainJSONWebToken.as_view()
refresh_jwt_token = RefreshJSONWebToken.as_view()
verify_jwt_token = VerifyJSONWebToken.as_view()
