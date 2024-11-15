from django import forms

class UrlForm(forms.Form):
    long_url = forms.URLField(label='Enter a URL', max_length=2000)

    def clean_long_url(self):
        long_url = self.cleaned_data['long_url']
        if '://' not in long_url:
            long_url = 'http://' + long_url
        return long_url
