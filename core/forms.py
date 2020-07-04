from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


class CheckOutForm(forms.Form):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    phone_number = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder':'0712345678'}))
    email_address = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder':'youremail@example.com',
        'class':'form-control'
    }))
    country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={
        'class':'custom-select d-block w-100'
    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Langata Nairobi',
        'class':'form-control'
    }))

