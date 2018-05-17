from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter
from django.utils.module_loading import import_string


def get_oauth2_adapter_class(provider):
    module = import_string(f'allauth.socialaccount.providers.{provider}.views')
    return [c for c in module.__dict__.values() if
            type(c) == type and issubclass(c, OAuth2Adapter) and c != OAuth2Adapter][0]
