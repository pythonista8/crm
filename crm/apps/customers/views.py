from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from apps.customers.models import Customer, Amount
from apps.customers.forms import CustomerForm, AmountFormSet


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


class CustomerCreate(CustomerContextMixin, SuccessMessageMixin, CreateView):
    form_class = CustomerForm
    success_message = "Successfully created"

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        amount_form = AmountFormSet(request.POST)
        if form.is_valid() and amount_form.is_valid():
            return self.form_valid(form, amount_form)
        else:
            return self.form_invalid(form, amount_form)

    def form_valid(self, form, amount_form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        amount_form.instance = self.object
        amount_form.save()
        return super(CustomerCreate, self).form_valid(form)

    def form_invalid(self, form, amount_form):
        if not form.is_valid():
            messages.error(self.request, form.errors)
        if not amount_form.is_valid():
            messages.error(self.request, amount_form.errors)
        return self.render_to_response(
            self.get_context_data(form=form, amount_form=amount_form))

    def get_context_data(self, **kwargs):
        ctx = super(CustomerCreate, self).get_context_data(**kwargs)
        ctx['amount_form'] = AmountFormSet()
        ctx['title'] = "Create new {}".format(Customer._meta.verbose_name)
        return ctx


class CustomerUpdate(CustomerContextMixin, SuccessMessageMixin, UpdateView):
    form_class = CustomerForm
    success_message = "Successfully updated"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        amount_form = AmountFormSet(request.POST)
        if form.is_valid() and amount_form.is_valid():
            return self.form_valid(form, amount_form)
        else:
            return self.form_invalid(form, amount_form)

    def form_valid(self, form, amount_form):
        self.object = self.get_object()
        amount_form.instance = self.object
        amount_form.save()
        return super(CustomerUpdate, self).form_valid(form)

    def form_invalid(self, form, amount_form):
        if not form.is_valid():
            messages.error(self.request, form.errors)
        if not amount_form.is_valid():
            messages.error(self.request, amount_form.errors)
        return self.render_to_response(
            self.get_context_data(form=form, amount_form=amount_form))

    def get_context_data(self, **kwargs):
        ctx = super(CustomerUpdate, self).get_context_data(**kwargs)
        ctx['amount_form'] = AmountFormSet()
        ctx['title'] = "Edit {}".format(Customer._meta.verbose_name)
        return ctx

    def get_success_url(self):
        object_ = self.get_object()
        return reverse('customers:edit', kwargs={'pk': object_.pk})


class AmountList(ListView):
    model = Amount
    paginate_by = 16

    def get_context_data(self, **kwargs):
        ctx = super(AmountList, self).get_context_data(**kwargs)
        ctx['customer'] = Customer.objects.get(pk=self.kwargs['pk'])
        ctx['title'] = Amount._meta.verbose_name_plural.title()
        ctx['title_icon'] = 'money'
        ctx['verbose_name'] = Amount._meta.verbose_name
        return ctx
