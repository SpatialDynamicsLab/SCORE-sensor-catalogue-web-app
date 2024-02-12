from django import forms
from django.core.validators import MinValueValidator
from django.forms import widgets


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(
        widget=widgets.NumberInput(
            attrs={'type': 'number', 'min': 0, 'default': 0,
                   'class': 'custom-quantity'}),
        validators=[MinValueValidator(0)]
    )
    override = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )
    

