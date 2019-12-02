from django import forms


class SearchForm(forms.Form):

    q = forms.CharField(required=True, min_length=1,max_length=30)
    page = forms.IntegerField(required=False,initial=1,min_value=1,max_value=99)

    def clean_page(self):
        page = self.cleaned_data.get('page', None)
        if page is None:
            return self.initial.get('page', 1)
        return page

