from django import forms


class Authentication(forms.Form):
    username = forms.CharField(label="Name", max_length=40)
    password = forms.CharField(label='Text', min_length=10, max_length=20)