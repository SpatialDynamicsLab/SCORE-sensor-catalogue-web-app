from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=50, required=True, 
        widget=forms.TextInput(
        attrs={'placeholder': 'First Name'}
    ))
    last_name = forms.CharField(max_length=50, required=True, 
        widget=forms.TextInput(
        attrs={'placeholder': 'Last Name'}
    ))
    street_address  = forms.CharField(required=True,
                                          widget=forms.TextInput(
        attrs={'placeholder': '1234 Main St'}
    ))
    postal_code = forms.CharField(required=True,
                                        widget=forms.TextInput(
        attrs={'placeholder': 'Dublin 4'}
    ))

    city = forms.CharField(required=True,
                                        widget=forms.TextInput(
        attrs={'placeholder': 'Dublin'}
    ))

    country = CountryField(blank_label='(select country)').formfield(
        required=True,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    save_info = forms.BooleanField(widget=forms.CheckboxInput())



