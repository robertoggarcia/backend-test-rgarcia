from django import forms

from orders.models import Order


class CreateOrderForm(forms.ModelForm):
    """
    Create a new :model:`orders.Order` form.
    """
    customization = forms.CharField(required=False)

    class Meta:
        model = Order
        fields = ['menu', 'option', 'customization', 'order_by']
        widgets = {
            'menu': forms.HiddenInput(),
            'order_by': forms.HiddenInput()
        }
