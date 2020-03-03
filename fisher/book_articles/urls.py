from django.urls import path
from django.views.decorators.cache import cache_page

from fisher.book_articles.views import (
    Book_ArticleCreateView,
    Book_ArticleDetailView,
    Book_ArticlesListView,
    DraftsListView,
    EditBookArticleView
)


app_name = "book_articles"
urlpatterns = [
    path('', cache_page(60 * 5)(Book_ArticlesListView.as_view()), name='list'),
    path("book_articles/<str:isbn>",  Book_ArticleCreateView.as_view(), name="write_new"),
    path('drafts/', view = DraftsListView.as_view(), name='drafts'),
    path('edit/<int:pk>/',view =EditBookArticleView.as_view(), name ='edit_article'),
    path('<str:pk>/', view=Book_ArticleDetailView.as_view(), name='article')
]
