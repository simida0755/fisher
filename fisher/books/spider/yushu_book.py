# _*_ coding: utf-8 _*_

from django.conf import settings

from fisher.books.models import Book
from fisher.libs.httper import HTTP

__author__ = 'john'

class YuShuBook:
    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    def __init__(self):
        self.total = 0
        self.books = []

    def search_by_isbn(self,isbn):
        #先查询数据库是否有该数据
        result = Book.objects.filter(isbn = isbn).first()
        if result:
            self.__fill_single(result)
            return result
        url = self.isbn_url.format(isbn)
        result = HTTP.get(url)
        self.__fill_single(result)
        #接口获取图书后，保存
        book = Book()
        book.set_attrs(self.books[0])
        book.auther_save(self.books[0])
        book.save()
        # dict
        return result

    def __fill_single(self,data):
        if data:
            self.total = 1
            self.books.append(data)

    def __fill_collection(self,data):
        self.total = data['total']
        self.books = data['books']

    def search_by_keyword(self,keyword, page=1):
        url = self.keyword_url.format(keyword,settings.PER_PAGE,self.calulate_start(page))
        result = HTTP.get(url)
        self.__fill_collection(result)


    def calulate_start(self,page):
        return (page - 1) * settings.PER_PAGE


    @property
    def first(self):
        return self.books[0] if self.total >= 1 else None
