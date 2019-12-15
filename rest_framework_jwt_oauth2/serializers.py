# -*- coding: utf-8 -*-

from allauth.socialaccount.helpers import complete_social_login
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from allauth.socialaccount.providers.oauth2.views import OAuth2View
from django.utils.translation import ugettext as _
from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework_jwt.compat import Serializer
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from rest_framework_jwt_oauth2.utils.adapter import get_oauth2_adapter_class


def oauth2_authorize(request, provider, code=None, access_token=None, redirect_uri=None):
    if access_token:
        access_token = {'access_token': access_token}

    adapter = get_oauth2_adapter_class(provider)(request)

    adapter.request_token_url = None
    oauth_view = OAuth2View()
    oauth_view.request = request
    oauth_view.adapter = adapter
    if redirect_uri:
        adapter.get_callback_url = (
            lambda _redirect_url:
            lambda request, app: _redirect_url)(
            redirect_uri)
    else:
        adapter.get_callback_url = lambda request, app: reverse('%s_complete' % provider,
                                                                request=request)
    app = adapter.get_provider().get_app(request)
    client = oauth_view.get_client(request, app)

    if not access_token:
        access_token = client.get_access_token(code)

    token = adapter.parse_token(access_token)
    token.app = app
    login = adapter.complete_login(
        request,
        app,
        token,
        response=access_token
    )
    login.token = token

    # if state:
    #     if adapter.supports_state:
    #         login.state = SocialLogin.verify_and_unstash_state(
    #             request,
    #             state)
    #     else:
    #         login.state = SocialLogin.unstash_state(request)
    complete_social_login(request, login)
    return login


class OAuth2JSONWebTokenSerializer(Serializer):
    """
    """
    code = serializers.CharField(required=False)
    access_token = serializers.CharField(required=False)

    redirect_uri = serializers.CharField(required=False)

    def validate(self, attrs):
        request = self.context['request']
        provider = self.context['view'].kwargs['provider']
        access_token = attrs.get('access_token')
        code = attrs.get('code')
        if not access_token and not code:
            raise serializers.ValidationError("`code` is required!")
        try:
            login = oauth2_authorize(request, provider=provider, **attrs)
            user = login.user
        except OAuth2Error as e:
            raise serializers.ValidationError(e, code='oauth2_error')

        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise serializers.ValidationError(msg, code='auth_error')

            payload = jwt_payload_handler(user)

            return {
                'token': jwt_encode_handler(payload),
                'user': user,
            }
        else:
            msg = _('Unable to log in with provided credentials.')
            raise serializers.ValidationError(msg)
