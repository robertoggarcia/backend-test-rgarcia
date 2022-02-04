from django import forms
from menus.models import Menu, MenuOption


class CreateMenuForm(forms.ModelForm):
    """
    Create a new :model:`menus.MenuOption` form.
    """
    description = forms.CharField(
        label='Menu description',
        widget=forms.Textarea(attrs={'maxlength': '300'})
    )
    options = forms.ModelMultipleChoiceField(
        queryset=MenuOption.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    date = forms.DateField(
        label='Menu date',
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={'type': 'date'}
        )
    )

    class Meta:
        model = Menu
        fields = ['description', 'options', 'date']
