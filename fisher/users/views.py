from allauth.account.views import SignupView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, UpdateView, ListView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import View

from fisher.gift.models import Gift
from fisher.taskapp.celery import send_verify_email
from fisher.users.forms import CaptchaSignupForm

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    fields = ["name"]

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.INFO, _("Infos successfully updated")
        )
        return super().form_valid(form)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


class UserSingupView(SignupView):
    template_name = 'users/signup.html'
    form_class = CaptchaSignupForm

user_signup_view = UserSingupView.as_view()

class user_email_view(LoginRequiredMixin,View):
    def get(self,request):
        send_verify_email.delay('测试邮件','测试邮件的内容','simida0755@sina.com',['simida027@163.com'])
        return render(request,'users/user_email.html')
