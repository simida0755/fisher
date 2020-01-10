

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse

from django.views.generic import ListView
from django.views.generic.base import View

from fisher.books.models import Book
from fisher.gift.models import Gift
from fisher.libs.template_mail import send_html_mail
from fisher.taskapp.celery import send_asyn_html_mail
from fisher.wish.models import Wish


class save_to_wish(LoginRequiredMixin,View):

    def get(self, request, isbn):
        user = request.user
        if user.can_save_to_list(isbn):
            wish = Wish()
            wish.user = user
            wish.isbn = isbn
            wish.save()
        else:
            messages.success(self.request, '这本书已添加至你的赠送清单或者已存在与你的心愿清单，请不要重复添加')
        # return reverse('books:book_detail',kwargs = {"isbn":isbn})
        return redirect(reverse('books:book_detail',kwargs = {"isbn":isbn}))

class user_wish_view(LoginRequiredMixin,ListView):

    template_name = 'my_wish.html'

    def get_queryset(self):
        queryset = Wish.objects.filter(user=self.request.user)
        return queryset


class redraw_wish_view(LoginRequiredMixin,View):

    def get(self,request,wid):
        wish = Wish.objects.get(id = wid,user = request.user)
        wish.delete()
        return redirect(reverse('wish:user'))

class satisfy_wish_view(LoginRequiredMixin,View):

    def get(self,request,wid):
        user = request.user
        wish = Wish.objects.get(id=wid)
        gift = Gift.objects.get(user = user,isbn=wish.isbn,launched=False)
        book = Book.objects.get(isbn=wish.isbn)
        if not gift:
            messages.error(self.request,'你还没有上传此书，请点击"添加到赠送清单"，添加前，请确保自己可以赠送此书')
            return redirect(reverse('books:book_detail',kwargs={'isbn':wish.isbn}))
        content = {
            'wish':wish,
            'gift':gift,
            'book':book,
        }
        html_content = loader.render_to_string(
            'email/satisify_wish.html',  # 需要渲染的html模板
            content
        )

        send_asyn_html_mail.delay('有一本书要送给你',html_content,[wish.user.email])

        messages.success(self.request, f'已向{wish.user.username}发送邮件')
        return redirect(reverse('books:book_detail', kwargs={'isbn': wish.isbn}))
