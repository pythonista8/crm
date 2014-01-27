from django import http
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from apps.customers.models import Customer, Amount
from apps.customers.forms import CustomerForm, AmountFormSet


class CustomerContextMixin(object):
    model = Customer

    def get_context_data(self, **kwargs):
        ctx = super(CustomerContextMixin, self).get_context_data(**kwargs)
        ctx['title_icon'] = 'users'
        return ctx


class CustomerList(CustomerContextMixin, ListView):
    paginate_by = 16

    def get_queryset(self):
        qs = super(CustomerList, self).get_queryset()
        company = self.request.user.company
        return qs.filter(user__company=company)

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

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user.company == self.object.user.company:
            return super(CustomerUpdate, self).get(request, *args, **kwargs)
        else:
            raise http.Http404

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Users cannot update customers that do not belong to them.
        if request.user != self.object.user:
            raise http.HttpResponseForbidden("Permission denied")

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        amount_form = AmountFormSet(request.POST)
        if form.is_valid() and amount_form.is_valid():
            return self.form_valid(form, amount_form)
        else:
            return self.form_invalid(form, amount_form)

    def form_valid(self, form, amount_form):
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
        vname = Customer._meta.verbose_name
        if self.request.user == self.object.user:
            ctx['title'] = "Edit {}".format(vname)
        else:
            ctx['title'] = "View {}".format(vname)
        return ctx

    def get_template_names(self):
        tmpl = super(CustomerUpdate, self).get_template_names()
        if self.request.user != self.object.user:
            tmpl = 'customers/customer_view.html'
        return tmpl

    def get_success_url(self):
        return reverse('customers:edit', kwargs={'pk': self.object.pk})


class AmountList(ListView):
    model = Amount
    paginate_by = 16

    def get_customer(self):
        customer = get_object_or_404(Customer, pk=self.kwargs['pk'],
                                     user=self.request.user)
        return customer

    def get_queryset(self):
        qs = super(AmountList, self).get_queryset()
        return qs.filter(customer=self.get_customer())

    def get_context_data(self, **kwargs):
        ctx = super(AmountList, self).get_context_data(**kwargs)
        ctx['customer'] = self.get_customer()
        ctx['title'] = Amount._meta.verbose_name_plural.title()
        ctx['title_icon'] = 'money'
        ctx['verbose_name'] = Amount._meta.verbose_name
        return ctx
