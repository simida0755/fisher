from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from django.views.generic.base import View

from fisher.book_articles.forms import BookArticleForm
from fisher.book_articles.models import BookArticle
from fisher.books.models import Book
from fisher.drift.forms import DriftForm, MailDriftForm
from fisher.drift.models import Drift
from fisher.gift.models import Gift
from fisher.service.drift import DriftService


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


class BookArticleDetailView(LoginRequiredMixin, DetailView):
    '''查看书语'''
    model = BookArticle
    template_name = 'book_articles/book_article_detail.html'

    def get_queryset(self):
        return BookArticle.objects.select_related('user').filter(pk=self.kwargs['pk'])  #url里定义的

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        isbn = BookArticle.objects.get(id = self.kwargs['pk']).isbn
        context['book'] = Book.get_or_create(isbn = isbn)
        return context
