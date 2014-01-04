from django import forms
from lib.format import format_phone
from apps.companies.models import Company


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ('date_created', 'date_modified', 'user')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone is not None:
            return format_phone(phone)
