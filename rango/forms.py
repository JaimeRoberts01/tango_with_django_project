from django import forms # Created by JNR 23.01.2018
from rango.models import Page, Category

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to provide addtional information on the form.

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Category
        fields = ('name',)

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Page

        # What fields do we want to in our form? This way we don't need every field in the model.
        # Some fields may allow NULL values, so we may not want to include them.
        # Here, we are hiding the foreign key. We can exclude the category field from the form.
        # Or specify the fields to include (i.e. not include the category field)
        #fields = ('title', 'url', 'views')

        exclude = ('category',)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        # If the url is not empty and doesn't start with 'http://' add it.

        if url and not url.startswith('http://'):
            url = 'http://' + urls

            return cleaned_data
