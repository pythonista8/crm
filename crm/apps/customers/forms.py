from django import forms
from django.forms.models import inlineformset_factory
from lib.format import format_phone
from apps.customers.models import Customer, Amount


class CustomerForm(forms.ModelForm):
    website = forms.URLField(widget=forms.TextInput, required=False)
    facebook = forms.URLField(widget=forms.TextInput, required=False)
    twitter = forms.URLField(widget=forms.TextInput, required=False)
    linkedin = forms.URLField(widget=forms.TextInput, required=False)

    class Meta:
        model = Customer
        exclude = ('date_created', 'date_modified', 'user')

    def clean_cell_phone(self):
        phone = self.cleaned_data.get('cell_phone')
        if phone is not None:
            return format_phone(phone)

    def clean_main_phone(self):
        phone = self.cleaned_data.get('main_phone')
        if phone is not None:
            return format_phone(phone)


class AmountForm(forms.ModelForm):
    class Meta:
        model = Amount
        exclude = ('customer', 'date')


AmountFormSet = inlineformset_factory(
    Customer, Amount, extra=1, can_delete=False, max_num=1)
