import re

from django import forms
from django.core.exceptions import ValidationError

from fisher.drift.models import Drift


def mobile_check(value):
    res = re.match('^1[356789]\d{9}$', value)
    if not res:
        # 自定义规则不抛异常表示通过
        raise ValidationError('手机号码格式错误')


def drift_pk_check(value):
    if int(value) not in list(Drift.objects.values_list('id',flat=True)):
        print(value)
        print(list(Drift.objects.values_list('id',flat=True)))
        # 自定义规则，不抛出异常表示通过
        raise ValidationError('鱼漂id错误')

class DriftForm(forms.Form):


    recipient_name = forms.CharField(max_length=20)
    mobile = forms.CharField(required=True,
        # 使用自定义验证规则
        validators=[mobile_check],
        error_messages={
            'required': '手机号为必填项',
        })
    message = forms.CharField()
    address = forms.CharField(min_length=10,max_length=100,error_messages={
        'min_length': '最短不能小于10个字符',
        'max_length': '最大不能大于100个字符'
    })


class MailDriftForm(forms.Form):
    expressnumber = forms.CharField(required=False, min_length=8,max_length=20)
    drift_pk = forms.CharField(required=True,
                               #使用自定义验证规则
                               validators=[drift_pk_check],
                               )
