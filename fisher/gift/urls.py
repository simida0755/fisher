from django.urls import path
from fisher.gift.views import (
    save_to_gift,
)


app_name = "gift"
urlpatterns = [
    path("book/<str:isbn>", view=save_to_gift.as_view(), name="gift"),

]
