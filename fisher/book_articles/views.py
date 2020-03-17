from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.views.generic.base import View
from django_comments.signals import comment_was_posted

from fisher.book_articles.forms import BookArticleForm
from fisher.book_articles.models import BookArticle
from fisher.books.models import Book
from fisher.drift.forms import DriftForm, MailDriftForm
from fisher.drift.models import Drift
from fisher.gift.models import Gift
from fisher.helpers import AuthorRequiredMixin
from fisher.notifications.views import notification_handler
from fisher.service.drift import DriftService

class Book_ArticlesListView(LoginRequiredMixin,ListView):
    '''书语列表'''
    model = BookArticle
    paginate_by = 20
    context_object_name = "book_articles"
    template_name = 'book_articles/book_article_list.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(Book_ArticlesListView, self).get_context_data(*args, **kwargs)
        context['popular_tags'] = BookArticle.objects.get_counted_tags()
        return context

    def get_queryset(self, **kwargs):
        return BookArticle.objects.get_published().select_related('user',)

class DraftsListView(Book_ArticlesListView):
    """草稿箱文章列表"""

    def get_queryset(self, **kwargs):
        # 当前用户的草稿
        return BookArticle.objects.filter(user=self.request.user).get_drafts()


@method_decorator(cache_page(60 * 60), name='get')  # get是小写
class Book_ArticleCreateView(LoginRequiredMixin, CreateView):
    '''发表书语'''
    model = BookArticle
    form_class = BookArticleForm
    template_name = 'book_articles/book_article_create.html'
    messages = '您的书评已创建成功'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['book'] = Book.objects.get(isbn = self.kwargs['isbn'])
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(Book_ArticleCreateView,self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.messages)
        return reverse('index')

class EditBookArticleView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):  # 注意类的继承顺序
    """编辑文章"""
    model = BookArticle
    message = "您的文章编辑成功！"
    form_class = BookArticleForm
    template_name = 'book_articles/book_article_update.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(EditBookArticleView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse('book_articles:list')

class Book_ArticleDetailView(LoginRequiredMixin, DetailView):
    '''查看书语'''
    model = BookArticle
    template_name = 'book_articles/book_article_detail.html'

    def get_queryset(self):
        return BookArticle.objects.select_related('user').filter(pk=self.kwargs['pk'])  #url里定义的
    #为什么这里要用filter，用get就报错

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        isbn = BookArticle.objects.get(id = self.kwargs['pk']).isbn
        context['book'] = Book.get_or_create(isbn = isbn)
        return context

def notify_comment(**kwargs):
    '''文章有评论时通知作者'''
    actor = kwargs['request'].user
    obj = kwargs['comment'].content_object

    notification_handler(actor, obj.user, 'C' , obj)

#观察者模式 = 订阅[列表] +通知（同步）
comment_was_posted.connect(receiver = notify_comment)

