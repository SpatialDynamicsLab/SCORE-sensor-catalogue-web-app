
from django import forms

class CartAddProductForm(forms.Form):
    QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 30)]
    quantity = forms.TypedChoiceField(
                                choices=QUANTITY_CHOICES,
                                coerce=int,
                                label = ('Quantity'))
    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)