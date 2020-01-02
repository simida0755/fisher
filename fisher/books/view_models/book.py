# _*_ coding: utf-8 _*_
__author__ = 'john'

class BookViewModel:
    def __init__(self,book):
        is_dict = isinstance(book, dict)
        self.title = book['title'] if is_dict else book.title
        self.publisher = book['publisher'] if is_dict else book.publisher
        self.binding = book['binding'] if is_dict else book.binding
        self.author = book['author'] if is_dict else book.author
        self.image = book['image'] if is_dict else book.image
        self.price = book['price'] if is_dict else book.price
        self.pubdate = book['pubdate'] if is_dict else book.pubdate
        self.summary = book['summary'] if is_dict else book.summary
        self.isbn = book['isbn'] if is_dict else book.isbn
        self.pages = book['pages'] if is_dict else book.pages

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



