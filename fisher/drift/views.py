from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView
from django.views.generic.base import View

from fisher.drift.forms import DriftForm, MailDriftForm
from fisher.drift.models import Drift
from fisher.gift.models import Gift
from fisher.service.drift import DriftService


class send_drift(LoginRequiredMixin, View):
    def get(self, request, pk):
        gift = Gift.objects.get(id=pk)
        user = request.user
        if gift.launched:
            messages.error(self.request, f'{gift.user.username}的这本书正处于交易状态，暂时不可以索要')
            return redirect(reverse('books:book_detail', kwargs={"isbn = gift.isbn"}))
        if gift.is_yourself_gift(user):
            messages.error(self.request, '这本书是你自己的，不可以索要')
            return redirect(reverse('books:book_detail', kwargs={"isbn = gift.isbn"}))
        can = user.can_satisfied_wish()
        if not can:  # 如果返回False,则是鱼豆不足，返回鱼豆不足页面
            return render('not_enough_beans.html', {'beans': user.beans})
        gifter = gift.user
        drift_form = DriftForm()
        return render(request, 'drift.html',
                      {'user_beans': user.beans, 'gift': gift, 'gifter': gifter, 'for': drift_form})

    def post(self, request, pk):
        drift_form = DriftForm(request.POST)
        gift = Gift.objects.get(id=pk)
        user = request.user
        if drift_form.is_valid():
            DriftService.save_a_drift(drift_form, gift, user)
            messages.success(self.request, f'已发送邮件{gift.user.username}')
        return redirect(reverse('books:book_detail', kwargs={'isbn': gift.isbn}))


class my_pending(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        drift_list = Drift.objects.filter(Q(requester_id=user.id) | Q(gifter_id=user.id)).all().order_by('-create_time')

        return render(request, 'pending.html', {'drift_list': drift_list})


class redraw_drift(LoginRequiredMixin, View):
    def get(self, request, pk):
        drift = Drift.objects.get(requester_id=request.user.id, pk=pk)
        drift.pending = 4
        drift.save()
        return redirect(reverse('drift:pending'))


class mailed_drift(LoginRequiredMixin, View):
    def get(self, request, pk):
        drift = Drift.objects.get(gifter_id=request.user.id, pk=pk)
        # 2对应success
        drift.pending = 2
        drift.save()
        return redirect(reverse('drift:pending'))

    def post(self, request):
        form = MailDriftForm(request.POST)
        user = request.user
        drift_list = Drift.objects.filter(Q(requester_id=user.id) | Q(gifter_id=user.id)).all().order_by(
            '-create_time')
        if form.is_valid():
            drift_pk = form.cleaned_data['drift_pk']
            drift = Drift.objects.get(id=drift_pk)
            # 2对应success
            drift.pending = 2
            drift.save()
        # return redirect(reverse('drift:pending',{'drift_list': drift_list,'form':form}))
        # return reverse_lazy('drift:pending',{'drift_list': drift_list,'form':form})
        return render(request, 'pending.html', {'drift_list': drift_list, 'form': form})


class reject_drift(LoginRequiredMixin, View):
    def get(self, request, pk):
        drift = Drift.objects.get(gifter_id=request.user.id, pk=pk)
        drift.pending = 3
        drift.save()
        return redirect(reverse('drift:pending'))
