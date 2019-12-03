from django.conf import settings
from django.db import models

from fisher.base.model import Base

class Wish(Base):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name = 'user_wish',verbose_name='用户',null=True,blank=True,on_delete=models.CASCADE)
    isbn = models.CharField('isbn',max_length=15,null=False)
    launched = models.BooleanField('送出',default=False)
