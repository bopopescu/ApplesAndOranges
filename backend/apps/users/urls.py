from django.conf.urls import url
from django.views.generic import TemplateView
from users.views import activate_view, ResetPasswordView


urlpatterns = [
    url(r'^password/reset/confirm/(?P<uid>[A-Za-z:0-9-]*)/(?P<token>[A-Za-z:0-9-]*)/$',
        ResetPasswordView.as_view(),
        name='password_reset_confirm'),
    url(r'^password/reset/success/$',
        TemplateView.as_view(template_name='auth/reset_password_success.html'),
        name='password_reset_success'),
    url(r'^activate/(?P<uid>[A-Za-z:0-9-]*)/(?P<token>[A-Za-z:0-9-]*)/$',
        activate_view, name='activate_account'),
]
