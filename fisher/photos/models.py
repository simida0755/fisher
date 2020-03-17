from django.conf import settings
from django.db import models


from fisher.base.model import Base

from uuid import uuid4
from datetime import datetime


def upload_photo_name(instance,filename):
    ext = filename.split('.')[-1]
    #日期目录和 随机文件名
    filename = '{}.{}'.format(uuid4().hex, ext)
    year = datetime.now().year
    month =datetime.now().month
    day = datetime.now().day
    # instance 可使用instance.user.id

    return "photos/{0}/{1}/{2}/{3}".format(year,month,day,filename)


class PhotoQuerySet(models.query.QuerySet):

    def get_most_recent(self):
        """获取最近20张照片 """
        phtots = self.all()[:20]
        return phtots

    def get_my_photo(self,user):
        phtots = self.filter(author = user)
        return phtots

class Photo(Base):
    title = models.CharField('照片标题', max_length=50,null=True,blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, blank=False,
                                  related_name="photo_author", on_delete=models.CASCADE, verbose_name='作者')
    image = models.ImageField('地址', upload_to=upload_photo_name,null=False, max_length=100)

    objects = PhotoQuerySet.as_manager()

    class Meta:
        verbose_name = "相片"
        verbose_name_plural = verbose_name
        ordering = ("-create_time",)

