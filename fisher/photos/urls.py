from django.urls import path
from django.views.decorators.cache import cache_page

from fisher.photos.views import (
    PhotoListView,
    MyPhotoView,
    PhotoCreateView,
    PhotoDetailView,
)

app_name = "photos"
urlpatterns = [
    path('', PhotoListView.as_view(), name='list'),
    path('upload/', PhotoCreateView.as_view(),name='upload'),
    path('<str:pk>', PhotoDetailView.as_view(), name = 'detail'),
]
