from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider
from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter
from django.utils.module_loading import import_string
from allauth.socialaccount.providers import registry


def get_oauth2_adapter_class(provider_id):
    provider: OAuth2Provider = registry.by_id(provider_id)
    provider_app = '.'.join(provider.__module__.split('.')[:-1])
    module = import_string(provider_app + '.views')
    return [c for c in module.__dict__.values() if
            type(c) == type and issubclass(c, OAuth2Adapter) and c != OAuth2Adapter][0]
