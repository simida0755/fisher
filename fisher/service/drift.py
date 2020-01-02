# _*_ coding: utf-8 _*_
from django.template import loader

from fisher.books.view_models.book import BookViewModel
from fisher.drift.models import Drift


from fisher.libs.email import send_template_email

__author__ = 'john'


class DriftService:
    """
        Wish服务层
    """

    @classmethod
    def save_a_drift(cls, drift_form, gift,user):

        book = BookViewModel(gift.book)

        drift = Drift()
        # drift_form.populate_obj(drift)
        drift.recipient_name = user.username
        drift.address = drift_form.cleaned_data['address']
        drift.mobile = drift_form.cleaned_data['mobile']
        drift.pending = 1
        drift.gift_id = gift.id
        drift.requester_id = user.id
        drift.requester_nickname = user.username
        drift.gifter_nickname = gift.user.username
        drift.gifter_id = gift.user.id
        drift.book_title = book.title
        drift.book_author = book.author
        drift.book_img = book.image
        drift.isbn = book.isbn
        # 当请求生成时，不需要让这个礼物处于锁定状态
        # 这样赠送者是可以收到多个索取请求的，由赠送者选择送给谁
        # current_gift.launched = True
        # 请求者鱼豆-1
        user.beans -= 1
        # 但是赠送者鱼豆不会立刻+1
        # current_gift.user.beans += 1
        drift.save()
        html_content = loader.render_to_string(
            'email/get_gift.html',  # 需要渲染的html模板
            {
        'wisher':user,
        'gift':gift # 参数
        }
        )
        send_template_email(gift.user.email, '有人想要一本书', html_content)
