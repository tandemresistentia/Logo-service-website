from django import forms

class NameForm(forms.Form):
    your_name = forms.CharField(label='test', max_length=600)