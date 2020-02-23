from django.urls import path
from fisher.book_articles.views import (
    Book_ArticleCreateView,
    Book_ArticleDetailView,
    Book_ArticlesListView,
    DraftsListView,
    EditBookArticleView
)


app_name = "book_articles"
urlpatterns = [
    path('', view=Book_ArticlesListView.as_view(), name='list'),
    path("book_articles/<str:isbn>", view=Book_ArticleCreateView.as_view(), name="write_new"),
    path('drafts/', view = DraftsListView.as_view(), name='drafts'),
    path('edit/<int:pk>/',view =EditBookArticleView.as_view(), name ='edit_article'),
    path('<str:pk>/', view=Book_ArticleDetailView.as_view(), name='article')
]
