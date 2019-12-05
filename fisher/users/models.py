from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

# nickname = Column(String(24), nullable=False)
# phone_number = Column(String(18), unique=True)
# email = Column(String(50), unique=True, nullable=False)
# _password = Column('password', String(128), nullable=False)
# confirmed = Column(Boolean, default=False)
# beans = Column(Float, default=0)
# send_counter = Column(Integer, default=0)
# receive_counter = Column(Integer, default=0)
from fisher.books.spider.yushu_book import YuShuBook
from fisher.drift.models import Drift
from fisher.gift.models import Gift
from fisher.libs.helper import is_isbn_or_key
from fisher.wish.models import Wish


class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    gender_choices = (
        ('male','男'),
        ('female','女')
    )

    name = CharField(_("Name of User"), blank=True, max_length=255)

    nick_name = models.CharField('昵称', max_length=50,default='')
    birthday = models.DateField('生日', null=True,blank=True)
    gender = models.CharField('性别', max_length=10,choices=gender_choices,default='female')
    adress = models.CharField('地址', max_length=100,default='')
    mobile = models.CharField('手机号', max_length=11,null=True,blank=True)
    beans = models.FloatField('豆子', default=1)
    send_counter = models.IntegerField('送出', default=0)
    receive_counter = models.IntegerField('收到', default=0)
    image = models.ImageField('头像', upload_to='image/%Y%m', default='image/default.png',max_length=100)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})


    def can_save_to_list(self,isbn):
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(isbn)
        if not yushu_book.first:
            return False
        # 不允许一个用户同时赠送多本相同的图书
        # 一个用户不可能同时成为赠送这和索要者
        gifting = Gift.objects.filter(user = self, isbn = isbn,
                                       launched = False).first()
        wishing = Wish.objects.filter(user = self.id, isbn = isbn,
                                       launched = False).first()
        if not gifting and not wishing:
            return True
        else:
            return False

    def is_gift_or_wish(self,isbn):
        #未判断isbn，需在传入之前判断
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(isbn)
        gift = Gift.objects.filter(user = self,isbn=isbn).first()
        wish = Wish.objects.filter(user = self,isbn = isbn).first()
        if gift:
            return gift
        if wish:
            return wish
        return False

    def can_satisfied_wish(self,gid = None):
        if gid:
            gift = Gift.objects.get(id = gid)
            if gift.user == self:
                return False
        if self.beans < 1:
            return False
        success_gifts = Drift.objects.filter(pending = 2,gifter = self.id).count()
        success_receive = Drift.objects.filter(pending = 2, requester_id =self).count()
        return False if success_gifts <= success_receive-2 else True

    @property
    def summary(self):
        return dict(
            nickname=self.username,
            beans=self.beans,
            email=self.email,
            send_receive=str(self.send_counter) + '/' + str(self.receive_counter)
        )
