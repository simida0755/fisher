from django import forms

from fisher.photos.models import Photo



class PhotoForm(forms.ModelForm):
    title = forms.CharField(max_length=10,required=False)

    class Meta:
        model = Photo
        fields = ['title',"image",]
