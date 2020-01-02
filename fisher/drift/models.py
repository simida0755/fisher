from django.conf import settings
from django.db import models


from fisher.base.model import Base
from fisher.books.spider.yushu_book import YuShuBook


class Drift(Base):
    pending_choices = (
        (1, 'wating'),
        (2, 'success'),
        (3, 'reject'),
        (4, 'redraw')
    )

    recipient_name = models.CharField(max_length=20, null=False, verbose_name='接受者邮寄姓名')
    address = models.CharField(max_length=100, null=False, verbose_name='地址')
    message = models.CharField(max_length=200, verbose_name='留言')
    mobile = models.CharField(max_length=20, null=False, verbose_name='手机')
    isbn = models.CharField(max_length=13, verbose_name='isbn')
    book_title = models.CharField(max_length=50, verbose_name='图书名')
    book_author = models.CharField(max_length=30, verbose_name='图书书作者')
    book_img = models.CharField(max_length=50, null=False, verbose_name='图书封面')
    # requester_id = Column(Integer, ForeignKey('user.id'))
    # requester = relationship('User')
    requester_id = models.IntegerField(verbose_name='请求者')
    requester_nickname = models.CharField(max_length=20,verbose_name='发送者昵称')
    gifter_id = models.IntegerField(verbose_name='送礼物人_id')
    gift_id = models.IntegerField(verbose_name='礼物_id')
    gifter_nickname = models.CharField(max_length=20, verbose_name='礼物者_昵称')
    pending = models.SmallIntegerField(choices=pending_choices,default=1, verbose_name='鱼漂状态')

    # gift_id = Column(Integer, ForeignKey('gift.id'))
    # gift = relationship('Gift')


    def pending_str(self, key):
        key_map = {
            'wating': {
                'requester': '等待对方邮寄',
                'gifter': '等待你邮寄'
            },
            'reject': {
                'requester': '对方已拒绝',
                'gifter': '你已拒绝'
            },
            'redraw': {
                'requester': '你已撤销',
                'gifter': '对方已撤销'
            },
            'success': {
                'requester': '对方已邮寄',
                'gifter': '你已邮寄，交易完成'
            }
        }
        return key_map[self.pending][key]


