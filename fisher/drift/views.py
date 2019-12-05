from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.base import View

from fisher.drift.forms import DriftForm
from fisher.gift.models import Gift
from fisher.service.drift import DriftService


class send_drift(LoginRequiredMixin, View):
    def get(self,request,pk):
        gift = Gift.objects.get(id = pk)
        user = request.user
        if gift.launched:
            messages.error(self.request, f'{gift.user.username}的这本书正处于交易状态，暂时不可以索要')
            return redirect(reverse('books:book_detail', kwargs={"isbn = gift.isbn"}))
        if gift.is_yourself_gift(user):
            messages.error(self.request, '这本书是你自己的，不可以索要')
            return redirect(reverse('books:book_detail', kwargs={"isbn = gift.isbn"}))
        can = user.can_satisfied_wish()
        if not can:#如果返回False,则是鱼豆不足，返回鱼豆不足页面
            return render('not_enough_beans.html', {'beans':user.beans})
        gifter = gift.user.summary
        drift_form = DriftForm()
        return render(request, 'drift.html',{'user_beans':user.beans,'gift':gift,'gifter':gifter,'for':drift_form})

    def post(self,request,pk):
        drift_form = DriftForm(request.form)
        gift = Gift.objects.get(id = pk)
        user = request.user
        if drift_form.is_valid():
            DriftService.save_a_drift(drift_form, gift,user)


class my_pending(View):
    def get(self,request):
        return render(request,'pending.html')
