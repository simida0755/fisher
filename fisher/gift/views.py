from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.base import View


from fisher.gift.models import Gift


class save_to_gift(LoginRequiredMixin,View):

    def get(self, request, isbn):
        user = request.user
        if user.can_save_to_list(isbn):
            gift = Gift()
            gift.user = user
            gift.isbn = isbn
            gift.save()
            user.beans += settings.BEANS_UPLOAD_ONE_BOOK
        else:
            messages.error(self.request, '这本书已添加至你的赠送清单或者已存在与你的心愿清单，请不要重复添加')
        # return reverse('books:book_detail',kwargs = {"isbn":isbn})
        return redirect(reverse('books:book_detail',kwargs = {"isbn":isbn}))

class user_gift_view(LoginRequiredMixin,ListView):

    template_name = 'my_gifts.html'

    def get_queryset(self):
        queryset = Gift.objects.filter(user=self.request.user)
        return queryset


class redraw_gift_view(LoginRequiredMixin,View):

    def get(self,request,gid):
        gift = Gift.objects.get(id = gid,user = request.user)
        gift.delete()
        request.user.beans -= settings.BEANS_UPLOAD_ONE_BOOK
        return redirect(reverse('gift:user'))

