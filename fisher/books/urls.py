from django.urls import path
from django.views.decorators.cache import cache_page

from fisher.books.views import (
    book_search_view,
    book_detail_view
)

app_name = "books"
urlpatterns = [
    path("search", view=book_search_view.as_view(), name="search"),
    path("<str:isbn>/detail", book_detail_view.as_view(), name="book_detail"),
]
