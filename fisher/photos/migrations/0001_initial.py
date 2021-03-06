# Generated by Django 2.2.4 on 2020-03-14 05:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import fisher.photos.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('status', models.SmallIntegerField(default=1, verbose_name='删除状态')),
                ('title', models.CharField(blank=True, max_length=50, null=True, verbose_name='照片标题')),
                ('image', models.ImageField(upload_to=fisher.photos.models.upload_photo_name, verbose_name='地址')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photo_author', to=settings.AUTH_USER_MODEL, verbose_name='作者')),
            ],
            options={
                'verbose_name': '相片',
                'verbose_name_plural': '相片',
                'ordering': ('-create_time',),
            },
        ),
    ]
