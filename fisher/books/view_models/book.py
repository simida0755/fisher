# _*_ coding: utf-8 _*_
__author__ = 'john'

class BookViewModel:
    def __init__(self,book):
        self.title = book['title']
        self.publisher = book['publisher']
        self.binding = book['binding']
        self.author = book['author']
        self.image = book['image']
        self.price = book['price']
        self.pubdate = book['pubdate']
        self.summary = book['summary']
        self.isbn = book['isbn']
        self.pages = book['pages']

    @property
    def intor(self):
        intors = filter(lambda x: True if x else False,
                        [self.author, self.publisher, self.price])
        return '/'.join(intors)

class BookCollection:
    def __init__(self):
        self.total = 0
        self.book = []
        self.keyword = ''

    def fill(self,yushu_book,keyword):
        self.total = yushu_book.total
        self.keyword = keyword
        self.books = [BookViewModel(book) for book in yushu_book.books]



