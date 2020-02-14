from django.conf import settings
from django.db import models


from fisher.base.model import Base
from fisher.books.spider.yushu_book import YuShuBook


class Gift(Base):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name = 'user_gift',verbose_name='用户',null=True,blank=True,on_delete=models.CASCADE)
    isbn = models.CharField('isbn',max_length=15,null=False)
    launched = models.BooleanField('送出', default=False)

    class Meta:
        verbose_name = '礼物'
        verbose_name_plural = verbose_name
        ordering = ('-create_time',)
        unique_together = ('user', 'isbn')  # 联合唯一键

    def is_yourself_gift(self,user):
        if self.user == user:
            return True


    @property
    def get_wish_counts(self):
        from fisher.wish.models import Wish
        counts =Wish.objects.filter(isbn = self.isbn).all().count()
        return counts

    @property
    def get_wish(self):
        from fisher.wish.models import Wish
        wishes =Wish.objects.filter(isbn = self.isbn).all().order_by('-create_time')
        return wishes

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    @classmethod
    def recent(cls):
        recent_gift = Gift.objects.raw('select * from (select * from gift_gift order by create_time desc) tt group by isbn')
        print(recent_gift)
        return recent_gift


