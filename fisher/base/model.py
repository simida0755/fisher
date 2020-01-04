# _*_ coding: utf-8 _*_
__author__ = 'john'
from django.db import models

class Base(models.Model):
    create_time = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    status = models.SmallIntegerField('删除状态', default=1)

    class Meta:
        abstract = True

    def set_attrs(self, attrs_dict):
        for key,value in attrs_dict.items():
            if hasattr(self, key) and key != 'id' and key != 'summary':
                setattr(self,key,value)
