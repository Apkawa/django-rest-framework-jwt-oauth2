from django.conf.urls import url, include

urlpatterns = [
    url(r'^api/', include('rest_framework_jwt_oauth2.urls')),
]
