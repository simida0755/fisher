from django.urls import path
from django.views.decorators.cache import cache_page

from fisher.users.views import (
    user_redirect_view,
    user_update_view,
    user_detail_view,
    user_signup_view,
    user_email_view,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", cache_page(60 * 5)(user_detail_view), name="detail"),
    path("captcha_signup", view = user_signup_view, name = 'captcha_signup'),
    path("email", view=user_email_view.as_view(), name='email')
]
