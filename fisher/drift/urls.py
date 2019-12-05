from django.urls import path
from fisher.drift.views import (
    my_pending,
    send_drift)


app_name = "drift"
urlpatterns = [
    # path("book/<str:isbn>", view=save_to_gift.as_view(), name="create"),
    path('pending/',view=my_pending.as_view(),name = 'pending'),
    path('<int:pk>', view = send_drift.as_view(),name = 'send_drift')
]
