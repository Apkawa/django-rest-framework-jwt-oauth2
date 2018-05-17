from django.apps import AppConfig as BaseConfig
from django.utils.translation import ugettext_lazy as _


class RestFrameworkJwtOauth2Config(BaseConfig):
    name = 'rest_framework_jwt_oauth2'
    verbose_name = _('Rest Framework Jwt Oauth2')
