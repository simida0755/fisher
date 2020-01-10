
#mailer.py
# -*- coding: utf-8 -*-
from django.core.mail import EmailMessage
from django.template import loader
from django.conf import settings


def send_html_mail(subject, template_name, content, recipient_list):
    html_content = loader.render_to_string(
        template_name,  # 需要渲染的html模板
        content
    )
    msg = EmailMessage(subject, html_content, settings.EMAIL_HOST_USER, recipient_list)
    msg.content_subtype = "html" # Main content is now text/html
    msg.send()




# def test_send_html_mail():
#
#     send_html_mail('有一本书可以赠送给你','email/test.html',['simida027@163.com'],name='杨鹏',gifter_name='姐姐',book_title='fme')
#
