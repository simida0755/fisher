# Generated by Django 2.2.4 on 2019-12-20 02:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gift', '0002_auto_20191129_2052'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gift',
            options={'ordering': ('-create_time',), 'verbose_name': '礼物', 'verbose_name_plural': '礼物'},
        ),
    ]
