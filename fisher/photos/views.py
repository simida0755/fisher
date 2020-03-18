from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse

from django.views.generic import ListView, CreateView, DetailView

from fisher.photos.forms import PhotoForm
from fisher.photos.models import Photo

user = get_user_model()

class PhotoListView(ListView):
    queryset = Photo.objects.get_most_recent()
    template_name = 'photos/photo_list.html'

class PhotoUserView(LoginRequiredMixin,ListView):
    model = Photo
    template_name = 'photos/user_photo.html'


    def get_queryset(self):
        photos = Photo.objects.filter(author = self.kwargs['pk'])
        return photos

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['fisher'] = get_object_or_404(get_user_model(), pk = self.kwargs['pk'])
        return context


class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'photos/upload_photo.html'
    messages = '您的照片上传成功'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PhotoCreateView,self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.messages)
        return reverse('index')


class PhotoDetailView(DetailView):
    model = Photo
    template_name = 'photos/photo_detail.html'

    def get_queryset(self):
        return Photo.objects.filter(pk=self.kwargs['pk'])  #url里定义的

