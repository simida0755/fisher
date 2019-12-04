from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.base import View

from fisher.books.forms import SearchForm
from fisher.books.spider.yushu_book import YuShuBook
from fisher.books.view_models.book import BookCollection, BookViewModel
from fisher.gift.models import Gift
from fisher.libs.helper import is_isbn_or_key
from fisher.wish.models import Wish


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

class book_detail_view(View):

    def get(self,request,isbn):
        has_in_gifts = False
        has_in_wishes = False
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(isbn)
        book = BookViewModel(yushu_book.first)
        user = request.user
        trade_gifts = Gift.objects.filter(isbn=isbn,
                            launched=False).all().order_by('-create_time')[:10]
        trade_wishes = Wish.objects.filter(isbn=isbn,
                            launched=False).all().order_by('-create_time')[:10]
        if user.is_authenticated:
            if Gift.objects.filter(user=request.user, isbn=isbn,
                                    launched=False).first():
                has_in_gifts = True

            if Wish.objects.filter(user=request.user, isbn=isbn,
                                    launched=False).first():
                has_in_wishes = True


        return render(request,'book_detail.html', {'book':book,'trade_wishes':trade_wishes,'trade_gifts':trade_gifts,'has_in_wishes':has_in_wishes,
                                                   'has_in_gifts':has_in_gifts})

class IndexView(ListView):

    template_name = 'index.html'

    def get_queryset(self):
        #按时间倒序，按isbn分组，返回不重复的isbn的gift列表
        isbn_dict = Gift.objects.values('isbn').distinct().order_by('-create_time').all()[:30]
        gift_list = []
        for isbn in isbn_dict:
            print(isbn)
            gift = Gift.objects.filter(isbn = isbn.values() ).first()
            if gift:
                list.append(gift)
        return gift_list
