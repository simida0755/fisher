from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.db import models


from fisher.base.model import Base
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from taggit.managers import TaggableManager

from fisher.books.models import Book


class BookArticleQuerySet(models.query.QuerySet):
    """自定义QuerySet，提高模型类的可用性"""

    def get_published(self):
        """返回已发表的书评"""
        return self.filter(status="P")

    def get_drafts(self):
        """返回未发表的草稿"""
        return self.filter(status="D")

    def get_counted_tags(self):
        """统计所有已发布的文章中，每一个标签的数量(大于0的)"""
        tag_dict = {}
        for obj in self.get_published():
            for tag in obj.tags.names():
                if tag not in tag_dict:
                    tag_dict[tag] = 1

                else:
                    tag_dict[tag] += 1
        return tag_dict.items()

class BookArticle(Base):
    STATUS = (("D", "Draft"), ("P", "Published"))

    title = models.CharField('书语标题', max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name="author", on_delete=models.SET_NULL, verbose_name='作者')
    image = models.ImageField(upload_to='book_articles_pictures/%Y/%m/%d/', verbose_name='文章图片')
    isbn = models.CharField('isbn',max_length=15,null=False,unique=True)
    status = models.CharField(max_length=1, choices=STATUS, default='D', verbose_name='状态')  # 默认存入草稿箱
    content = MarkdownxField(verbose_name='内容')
    edited = models.BooleanField(default=False, verbose_name='是否可编辑')
    tags = TaggableManager(help_text='多个标签使用,(英文)隔开', verbose_name='标签')
    objects = BookArticleQuerySet.as_manager()



    class Meta:
        verbose_name = '书语'
        verbose_name_plural = verbose_name
        ordering = ("create_time",)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(BookArticle, self).save(*args, **kwargs)

        if not self.reply:
            channel_layer = get_channel_layer()
            payload = {
                "type": "receive",
                "key": "additional_news",
                "actor_name": self.user.username
            }
            async_to_sync(channel_layer.group_send)('notifications', payload)

    def get_markdown(self):
        # 将Markdown文本转换成HTML
        return markdownify(self.content)

    @property
    def book(self):
        return Book.get_or_create(self.isbn)
