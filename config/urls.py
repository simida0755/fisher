from django.conf import settings
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView
from django.views import defaults as default_views
from allauth.account import urls
from django.views.static import serve

from config.settings.base import MEDIA_ROOT
from fisher.books.views import IndexView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
    # User management
    path("users/", include("fisher.users.urls", namespace="users")),
    path("books/", include("fisher.books.urls", namespace="books")),
    path("book_articles/", include("fisher.book_articles.urls", namespace="book_articles")),
    path("gift/", include("fisher.gift.urls", namespace="gift")),
    path("wish/", include("fisher.wish.urls", namespace="wish")),
    path("drift/", include("fisher.drift.urls", namespace="drift")),
    path("photos/", include("fisher.photos.urls", namespace="photos")),
    path("messages/", include("fisher.messager.urls", namespace="messages")),
    path("notifications/", include("fisher.notifications.urls", namespace="notifications")),

    re_path('^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    path("accounts/", include("allauth.urls")),
    path('captcha/',include('captcha.urls')),
    path('markdownx/', include('markdownx.urls')),
    path('comments/', include('django_comments.urls')),
    # Your stuff: custom urls includes go here
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
