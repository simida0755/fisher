from django.conf import settings
from django.db import models

from fisher.base.model import Base
from fisher.books.spider.yushu_book import YuShuBook


class Wish(Base):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name = 'user_wish',verbose_name='用户',null=True,blank=True,on_delete=models.CASCADE)
    isbn = models.CharField('isbn',max_length=15,null=False)
    launched = models.BooleanField('送出',default=False)

    @property
    def get_gift_counts(self):
        from fisher.gift.models import Gift
        counts =Gift.objects.filter(isbn = self.isbn).all().count()
        return counts

    @property
    def get_gift(self):
        from fisher.gift.models import Gift
        gifts =Gift.objects.filter(isbn = self.isbn).all().order_by('-create_time')
        return gifts

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first
