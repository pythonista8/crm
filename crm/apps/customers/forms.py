from django import forms
from lib.format import format_phone
from apps.customers.models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ('date_created', 'date_modified')

    def clean_cell_phone(self):
        phone = self.cleaned_data.get('cell_phone')
        if phone is not None:
            return format_phone(phone)

    def clean_main_phone(self):
        phone = self.cleaned_data.get('main_phone')
        if phone is not None:
            return format_phone(phone)
