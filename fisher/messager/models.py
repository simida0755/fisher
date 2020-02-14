import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class MessageQuerySet(models.query.QuerySet):
    def get_conversation(self, sender, recipient):
        """用户间的私信会话"""
        qs_one = self.filter(sender=sender, recipient=recipient).select_related('sender', 'recipient')  # A发送给B的消息
        qs_two = self.filter(sender=recipient, recipient=sender).select_related('sender', 'recipient')  # B发送给A的消息
        return qs_one.union(qs_two).order_by('create_time')  # 取并集后按时间排序

    def get_most_recent_conversation(self, recipient):
        """获取最近一次私信互动的用户"""
        try:
            qs_sent = self.filter(sender=recipient).select_related('sender', 'recipient')  # 当前登录用户发送的消息
            qs_received = self.filter(recipient=recipient).select_related('sender', 'recipient')  # 当前登录用户接收的消息
            qs = qs_sent.union(qs_received).latest("create_time")  # 最后一条消息
            if qs.sender == recipient:
                # 如果登录用户有发送消息，返回消息的接收者
                return qs.recipient
            # 否则返回消息的发送者
            return qs.sender
        except self.model.DoesNotExist:
            # 如果模型实例不存在，则返回当前用户
            return get_user_model().objects.get(username=recipient.username)


from fisher.base.model import Base
from fisher.books.spider.yushu_book import YuShuBook


class Message(Base):
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages',
                               blank=True, null=True, on_delete=models.SET_NULL, verbose_name='发送者')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_messages',
                                  blank=True, null=True, on_delete=models.SET_NULL, verbose_name='接受者')
    message = models.TextField(blank=True, null=True, verbose_name='内容')
    unread = models.BooleanField(default=True, verbose_name='是否未读')

    objects = MessageQuerySet.as_manager()

    class Meta:
        verbose_name = '私信'
        verbose_name_plural = verbose_name
        ordering = ('-create_time',)


    def __str__(self):
        return self.message

    def mark_as_read(self):
        if self.unread:
            self.unread = False
            self.save()

