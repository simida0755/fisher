# _*_ coding: utf-8 _*_
from django.conf import settings

__author__ = 'john'
# apps/utils/email_send.py

from random import Random
from django.core.mail import send_mail




# 生成时间+随机字符串
def random_str(random_length=8):
    str = ''
    # 生成字符串的可选字符串
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        str += chars[random.randint(0, length)]
    return str

# 发送注册邮件
def send_register_eamil_dj(email,token):
    # 发送之前先保存到数据库，到时候查询链接是否存在
    # 实例化一个EmailVerifyRecord对象

    # 定义邮件内容:
    email_title = ""
    email_body = ""

    if email :
        email_title = "天天注册激活链接"
        email_body = "请点击下面的链接激活你的账号: http://127.0.0.1:8000/active/{0}".format(token)

        # 使用Django内置函数完成邮件发送。四个参数：主题，邮件内容，从哪里发，接受者list
        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
        # 如果发送成功
        if send_status:
            pass

def send_template_email(email_address,email_title, template):
    # 发送之前先保存到数据库，到时候查询链接是否存在
    # 实例化一个EmailVerifyRecord对象



    # 使用Django内置函数完成邮件发送。四个参数：主题，邮件内容，从哪里发，接受者list
    send_status = send_mail(email_title, template, settings.EMAIL_FROM, [email_address])
    # 如果发送成功
    if send_status:
        pass
