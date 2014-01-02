from django.core.urlresolvers import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from apps.customers.models import Customer
from apps.customers.forms import CustomerForm


class CustomerContextMixin(object):
    model = Customer

    def get_context_data(self, **kwargs):
        ctx = super(CustomerContextMixin, self).get_context_data(**kwargs)
        ctx['title_icon'] = 'user'
        return ctx


class CustomerList(CustomerContextMixin, ListView):
    paginate_by = 16

    def get_context_data(self, **kwargs):
        ctx = super(CustomerList, self).get_context_data(**kwargs)
        ctx['title'] = Customer._meta.verbose_name_plural.title()
        ctx['verbose_name'] = Customer._meta.verbose_name
        return ctx

    def get_success_url(self):
        return reverse('customers:list')


class CustomerCreate(CustomerContextMixin, SuccessMessageMixin, CreateView):
    form_class = CustomerForm
    success_message = "Successfully created"

    def get_context_data(self, **kwargs):
        ctx = super(CustomerCreate, self).get_context_data(**kwargs)
        ctx['title'] = "Create new {}".format(Customer._meta.verbose_name)
        return ctx


class CustomerUpdate(CustomerContextMixin, SuccessMessageMixin, UpdateView):
    form_class = CustomerForm
    success_message = "Successfully updated"

    def get_context_data(self, **kwargs):
        ctx = super(CustomerUpdate, self).get_context_data(**kwargs)
        ctx['title'] = "Edit {}".format(Customer._meta.verbose_name)
        return ctx

    def get_success_url(self):
        object_ = self.get_object()
        return reverse('customers:edit', kwargs={'pk': object_.pk})
