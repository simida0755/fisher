# Generated by Django 2.2.4 on 2020-01-18 07:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import markdownx.models
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BookArticle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('title', models.CharField(max_length=50, verbose_name='书名')),
                ('image', models.ImageField(upload_to='book_articles_pictures/%Y/%m/%d/', verbose_name='文章图片')),
                ('isbn', models.CharField(max_length=15, unique=True, verbose_name='isbn')),
                ('status', models.CharField(choices=[('D', 'Draft'), ('P', 'Published')], default='D', max_length=1, verbose_name='状态')),
                ('content', markdownx.models.MarkdownxField(verbose_name='内容')),
                ('edited', models.BooleanField(default=False, verbose_name='是否可编辑')),
                ('tags', taggit.managers.TaggableManager(help_text='多个标签使用,(英文)隔开', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='标签')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='author', to=settings.AUTH_USER_MODEL, verbose_name='作者')),
            ],
            options={
                'verbose_name': '书语',
                'verbose_name_plural': '书语',
                'ordering': ('create_time',),
            },
        ),
    ]