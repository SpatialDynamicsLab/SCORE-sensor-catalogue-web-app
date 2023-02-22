from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=50, required=True, 
        widget=forms.TextInput(
        attrs={'placeholder': 'John'}
    ))
    last_name = forms.CharField(max_length=50, required=True, 
        widget=forms.TextInput(
        attrs={'placeholder': 'Doe'}
    ))
    street_address  = forms.CharField(required=True,
                                          widget=forms.TextInput(
        attrs={'placeholder': '1234 Main St'}
    ))
    apartment_address = forms.CharField(required=False,
                                        widget=forms.TextInput(
        attrs={'placeholder': 'Apartment or suite'}
    ))
    country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    
    zip_code = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control'
    }))
    save_info = forms.BooleanField(widget=forms.CheckboxInput())

