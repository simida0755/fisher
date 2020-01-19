from django.urls import path
from fisher.book_articles.views import (
    Book_ArticleCreateView,
BookArticleDetailView
)


app_name = "book_articles"
urlpatterns = [
    path("book_articles/<str:isbn>", view=Book_ArticleCreateView.as_view(), name="write_new"),
    path('<str:pk>/', view=BookArticleDetailView.as_view(), name='article')
]
