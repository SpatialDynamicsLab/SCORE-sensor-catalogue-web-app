from django import forms
from orders.models import Order, OrderItem
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

class OrderCreateForm(forms.ModelForm):
    # country = CountryField()
    class Meta:
        model = Order
        fields = ('first_name','second_name','address',
            'postal_code', 'city','country'
        )
        country = CountryField
        widgets  ={
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'second_name':forms.TextInput(attrs={'class':'form-control'}),
            'address':forms.TextInput(attrs={'class':'form-control'}),
            'postal_code':forms.TextInput(attrs={'class':'form-control'}),
            'city':forms.TextInput(attrs={'class':'form-control'}),
            'country':CountrySelectWidget(attrs={'class': 'custom-select d-block w-100'})

        }


