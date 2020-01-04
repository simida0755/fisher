# _*_ coding: utf-8 _*_

from django.conf import settings

from fisher.books.models import Book
from fisher.libs.httper import HTTP, Http

__author__ = 'john'

class YuShuBook:
    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    keyword_url = 'https://api.douban.com/v2/book/search?apikey={}&q={}&count={}&start={}'
    #https://api.douban.com/v2/book/search?apikey=0df993c66c0c636e29ecbb5344252a4a&q=村上春树

    def __init__(self):
        self.total = 0
        self.books = []

    def search_by_isbn(self,isbn):
        #先查询数据库是否有该数据
        result = Book.objects.filter(isbn = isbn).first()
        if result:
            self.__fill_single(result)
        else:
            url = self.isbn_url.format(isbn)
            result = HTTP.get(url)
            if result:
                self.__fill_single(result)
                #接口获取图书后，保存
                book = Book()
                dict_book = self.get_book(isbn)
                book.set_attrs(dict_book)
                book.summary = (dict_book['summary'][:1000])
                book.auther_save(dict_book)
                book.save()


    def __fill_single(self,data):
        if data:
            self.total = 1
            self.books.append(data)

    def __fill_collection(self,data):
        if 'books' in data:
            for book in data['books']:
                if 'isbn13' in book:
                    self.search_by_isbn(book['isbn13'])
        self.total = data['total']

    def search_by_keyword(self,keyword, page=1):
        url = self.keyword_url.format(settings.DOUBAN_APIKEY,keyword,settings.PER_PAGE,self.calulate_start(page))
        result = HTTP.get(url)
        if result:
            self.__fill_collection(result)


    def calulate_start(self,page):
        return (page - 1) * settings.PER_PAGE


    @property
    def first(self):
        return self.books[0] if self.total >= 1 else None


    def get_book(self,isbn):
        for book in self.books:
            if isinstance(book, dict):
                if isbn == book['isbn']:
                    return book

