from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View

from fisher.books.forms import SearchForm
from fisher.books.spider.yushu_book import YuShuBook
from fisher.books.view_models.book import BookCollection
from fisher.libs.helper import is_isbn_or_key



class book_search_view(View):

    def get(self,request):
        form = SearchForm(request.GET)
        books = BookCollection()
        if form.is_valid():
            q = form.cleaned_data['q']
            page = form.cleaned_data['page']
            isbn_or_key = is_isbn_or_key(q)
            yushu_book = YuShuBook()
            if isbn_or_key == 'isbn':
                    yushu_book.search_by_isbn(q)
            else:
                yushu_book.search_by_keyword(q, page)

            books.fill(yushu_book, q)
        else:
            # flash('搜索的关键字不符合要求，请重新输入关键字')
            messages.success(self.request, '搜索的关键字不符合要求，请重新输入关键字')
            return render(request,'search_result.html')
        return render(request,'search_result.html', {'books':books})

# class book_search_view(View):
#
#     def get(self,request):
#         form = SearchForm(request.GET)
#         return HttpResponse('hehe')

