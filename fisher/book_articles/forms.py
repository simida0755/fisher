from django import forms
from markdownx.fields import MarkdownxFormField

from fisher.book_articles.models import BookArticle


class BookArticleForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput()) #隐藏
    isbn = forms.CharField(widget=forms.HiddenInput()) #隐藏
    edited = forms.BooleanField(widget=forms.HiddenInput(),initial=False, required=False)
    content = MarkdownxFormField()
    class Meta:
        model = BookArticle
        fields = ["title", "content", "image", "tags", "status", "edited"]
