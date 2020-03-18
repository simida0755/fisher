from django.urls import path
from django.views.decorators.cache import cache_page

from fisher.photos.views import (
    PhotoListView,
    PhotoUserView,
    PhotoCreateView,
    PhotoDetailView,
)

app_name = "photos"
urlpatterns = [
    path('', PhotoListView.as_view(), name='list'),
    path('upload/', PhotoCreateView.as_view(),name= 'upload'),
    path('user/<str:pk>',PhotoUserView.as_view(),name='user'),
    path('<str:pk>', PhotoDetailView.as_view(), name = 'detail'),
]
