# Generated by Django 2.2.4 on 2019-12-01 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drift', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drift',
            name='recipient_name',
            field=models.CharField(max_length=20, verbose_name='接受者邮寄姓名'),
        ),
        migrations.AlterField(
            model_name='drift',
            name='requester_id',
            field=models.IntegerField(verbose_name='请求者'),
        ),
        migrations.AlterField(
            model_name='drift',
            name='requester_nickname',
            field=models.CharField(max_length=20, verbose_name='发送者昵称'),
        ),
    ]
