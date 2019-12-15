from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^auth/$', views.obtain_jwt_token, name='auth'),
    url(r'^oauth2/(?P<provider>\w+)/get_url/$',
        views.OAuth2InitialView.as_view(), name='oauth2-get-url'),
    url(r'^oauth2/(?P<provider>\w+)/$',
        views.OAuth2LoginView.as_view(), name='oauth2-complete'),
    url(r'^refresh/$', views.refresh_jwt_token, name='token-refresh'),
    url(r'^verify/$', views.verify_jwt_token, name='token-verify')
]
