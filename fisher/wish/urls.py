from django.urls import path
from fisher.wish.views import (
    save_to_wish,
    user_wish_view,
    redraw_wish_view,
)


app_name = "wish"
urlpatterns = [
    path("book/<str:isbn>", view=save_to_wish.as_view(), name="create"),
    path("user/", view=user_wish_view.as_view(), name="user"),
    path("<str:wid>/redraw/", view=redraw_wish_view.as_view(), name="redraw"),
]
