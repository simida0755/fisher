from django.conf import settings
from django.db import models


from fisher.base.model import Base
from fisher.books.spider.yushu_book import YuShuBook


class Gift(Base):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name = 'user_gift',verbose_name='用户',null=True,blank=True,on_delete=models.CASCADE)
    isbn = models.CharField('isbn',max_length=15,null=False)
    launched = models.BooleanField('送出',default=False)

    class Meta:
        verbose_name = '礼物'
        verbose_name_plural = verbose_name
        unique_together = ('user', 'isbn')  # 联合唯一键

    @classmethod
    def get_user_gift(cls, user):
        gift = user.user__gift.all()
        return gift

    # @classmethod
    # def get_wish_counts(cls,isbn_list):
    #     from fisher.wish.models import Wish
    #     # 条件表达式
    #     count_list = db.session.query(func.count(Wish.id),Wish.isbn).filter(
    #         Wish.launched == False,
    #         Wish.isbn.in_(isbn_list),
    #         Wish.status==1).group_by(
    #         Wish.isbn).all()
    #     count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
    #     return count_list


    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    @classmethod
    def recent(cls):
        recent_gift = Gift.objects.filter_by(
            launched=False).group_by(
            Gift.isbn).order_by(
            Gift.create_time).limit(
            settings.RECENT_BOOK_COUNT).distinct().all()
        return recent_gift