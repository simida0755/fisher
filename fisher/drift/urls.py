from django.urls import path
from fisher.drift.views import (
    my_pending,
    send_drift,
    redraw_drift,
    mailed_drift,
    reject_drift

)


app_name = "drift"
urlpatterns = [
    # path("book/<str:isbn>", view=save_to_gift.as_view(), name="create"),
    path('pending/',view=my_pending.as_view(),name = 'pending'),
    path('<int:pk>', view = send_drift.as_view(),name = 'send_drift'),
    path('redraw/<str:pk>', view=redraw_drift.as_view(), name='redraw'),
    path('mailed/', view=mailed_drift.as_view(), name='mailed'),
    path('reject/<str:pk>', view=reject_drift.as_view(), name='reject'),

]
