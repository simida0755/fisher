from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from django.views.generic import ListView, CreateView, DetailView

from fisher.photos.forms import PhotoForm
from fisher.photos.models import Photo



class PhotoListView(ListView):
    queryset = Photo.objects.get_most_recent()
    template_name = 'photos/photo_list.html'

class MyPhotoView(LoginRequiredMixin,ListView):
    template_name = 'photos/my_photo.html'

    def get_queryset(self):
        photos = Photo.objects.filter(user =  self.request.user)
        return photos



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
        return Photo.objects.select_related('author').filter(pk=self.kwargs['pk'])  #url里定义的

