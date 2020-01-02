from django.urls import path
from fisher.gift.views import (
    save_to_gift,
    user_gift_view,
    redraw_gift_view,
)


app_name = "gift"
urlpatterns = [
    path("book/<str:isbn>", view=save_to_gift.as_view(), name="create"),
    path("user/", view=user_gift_view.as_view(), name="user"),
    path("<str:gid>/redraw/", view=redraw_gift_view.as_view(), name="redraw"),

]
