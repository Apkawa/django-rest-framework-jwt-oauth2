from django.conf import settings

DEFAULT_REDIRECT_URL = getattr(settings, 'JWT_OAUTH2_DEFAULT_REDIRECT_URL',
                               '/accounts/{provider}/complete/')

DEFAULT_AUTH_URL = getattr(
    settings,
    'JWT_OAUTH2_DEFAULT_AUTH_URL',
    "/accounts/{provider}/login/?{qs}"
)
