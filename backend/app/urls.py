from django.conf.urls import include, url
from django.contrib import admin
from users.api import urlpatterns as users_api_urls
from tasks.api import urlpatterns as tasks_api_urls
from pns.api import urlpatterns as pns_api_urls
from core.api import urlpatterns as core_api_urls

urlpatterns = [

    # Core API endpoints
    url(r'^api/core/', include(core_api_urls)),

    # Admin endpoints
    url(r'^admin/', include(admin.site.urls)),
    # Users endpoints
    url(r'^api/v1/', include(users_api_urls)),
    # Tasks endpoints
    url(r'^api/v1/', include(tasks_api_urls)),
    # Payment Endpoints
    url(r'^api/v1/payments/', include('payments.api.urls')),
    # Auth endpoints
    url(r'^api/v1/auth/', include('djoser.urls')),
    # PUSH notifications
    url(r"^api/v1/", include(pns_api_urls)),
    # custom password reset and activate views
    url(r'^', include('users.urls')),
]
