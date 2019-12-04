from django.conf import settings
from django.db import models


from fisher.base.model import Base
from fisher.books.spider.yushu_book import YuShuBook


class Drift(Base):
    gender_choices = (
        ('wating' , 1),
        ('success' ,2),
        ('reject', 3),
        ('redraw', 4)
    )

    recipient_name = models.CharField(max_length=20, null=False)
    address = models.CharField(max_length=100, null=False)
    message = models.CharField(max_length=200)
    mobile = models.CharField(max_length=20, null=False)
    isbn = models.CharField(max_length=13)
    book_title = models.CharField(max_length=50)
    book_author = models.CharField(max_length=30)
    book_img = models.CharField(max_length=50, null=False)
    # requester_id = Column(Integer, ForeignKey('user.id'))
    # requester = relationship('User')
    requester_id = models.IntegerField()
    requester_nickname = models.IntegerField()
    gifter_id = models.IntegerField()
    gift_id = models.IntegerField()
    gifter_nickname = models.CharField(max_length=20)
    _pending = Column('pending', SmallInteger, default=1)

    # gift_id = Column(Integer, ForeignKey('gift.id'))
    # gift = relationship('Gift')

    @property
    def pending(self):
        return PendingStatus(self._pending)

    @pending.setter
    def pending(self, status):
        self._pending = status.value

